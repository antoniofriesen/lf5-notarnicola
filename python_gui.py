from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
# Ein sicherer Schlüssel für Sitzungen (wichtig für die DSGVO-Sicherheit)
app.secret_key = 'dein_super_geheimes_session_passwort_fuer_den_pi'

def check_db_credentials(username, password):
    """
    Versucht eine Verbindung zur MariaDB auf 'localhost' herzustellen.
    Nutzt die vom User eingegebenen SQL-Zugangsdaten.
    """
    try:
        verbindung = mysql.connector.connect(
            host='localhost',        # Da DB und Webserver auf demselben Pi laufen
            database='BS14',         # Deine Projektdatenbank
            user=username,
            password=password
        )
        if verbindung.is_connected():
            verbindung.close()
            return True
    except Error as e:
        print(f"Login-Fehler auf Datenbankebene: {e}")
        return False
    return False

def hole_daten_aus_datenbank(username, password, query):
    """Führt eine Abfrage mit den Rechten des angemeldeten Benutzers aus."""
    verbindung = None
    ergebnisse = []
    try:
        verbindung = mysql.connector.connect(
            host='localhost',
            database='BS14',
            user=username,
            password=password
        )
        cursor = verbindung.cursor()
        cursor.execute(query)
        ergebnisse = cursor.fetchall()
        cursor.close()
    except Error as e:
        flash(f"Fehler beim Laden der Daten (Möglicherweise fehlende Rechte): {e}", "danger")
    finally:
        if verbindung and verbindung.is_connected():
            verbindung.close()
    return ergebnisse

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Überprüfe die Zugangsdaten direkt über das MariaDB-Berechtigungssystem
        if check_db_credentials(username, password):
            session['db_user'] = username
            session['db_password'] = password  # In einer Produktiv-Webapp verschlüsselt im Speicher halten
            flash("Erfolgreich angemeldet!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Ungültige Zugangsdaten oder Zugriff verweigert!", "danger")
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Schutz der Route: Nur angemeldete User dürfen das Dashboard sehen
    if 'db_user' not in session:
        flash("Bitte melde dich zuerst an.", "warning")
        return redirect(url_for('login'))
    
    # Beispielabfrage: Artikel aus der 3NF-Datenbank laden
    # Falls z.B. ein 'lager_user' eingeloggt ist und SELECT-Rechte hat, klappt es.
    artikel_liste = hole_daten_aus_datenbank(
        session['db_user'], 
        session['db_password'], 
        "SELECT Artikel_ID, ArtikelName, Preis FROM artikel;"
    )
    
    return render_template('dashboard.html', user=session['db_user'], artikel=artikel_liste)

@app.route('/logout')
def logout():
    session.clear()
    flash("Erfolgreich abgemeldet.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Startet den Server. Erreichbar im Pi-Netzwerk über http://<IP-DES-PI>:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
