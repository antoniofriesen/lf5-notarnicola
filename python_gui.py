# ==============================================================================
# IMPORTE & BIBLIOTHEKEN
# ==============================================================================
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk

# ==============================================================================
# 1. FUNKTION: DYNAMISCHER VERBINDUNGSAUFBAU
# ==============================================================================
def db_verbindung_herstellen(user, password):
    try:
        verbindung = mysql.connector.connect(
            host='localhost',  
            user=user,              # Der aktuell eingegebene Benutzer
            password=db123,      # Das dazugehörige Passwort
            database='LF5'         # Name deiner Projektdatenbank
        )
        if verbindung.is_connected():
            return verbindung
    except Error as e:
        messagebox.showerror("Datenbank-Fehler", f"Zugriff verweigert oder Verbindung gesperrt!\n\nDetails: {e}")
        return None

# ==============================================================================
# 2. GUI-ANWENDUNGSKLASSE
# ==============================================================================
class PiDatenbankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zwei-Pi-Datenbank-Steuerung (BS14)")
        self.root.geometry("500x600")
        
        # Aktuelle Sitzungsdaten
        self.current_user = ""
        self.current_password = ""
        
        # Temporärer Speicher für die aktuelle Bestellung (Bestellpositionen-Schleife)
        self.aktuelle_bestellung_id = None
        self.temporaere_positionen = []

        # Startbildschirm (Login) anzeigen
        self.zeige_login_ansicht()

    def clear_root(self):
        """Leert das aktuelle Fenster, um eine neue Ansicht zu laden."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- ANSICHT: LOGIN ---
    def zeige_login_ansicht(self):
        self.clear_root()
        
        # Titel
        tk.Label(self.root, text="Zwei-Pi-Datenbank-Steuerung", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.root, text="Bitte mit DB-User von Pi 1 anmelden", font=("Arial", 10, "italic")).pack(pady=5)
        
        # Frame für Eingabemaske
        login_frame = tk.LabelFrame(self.root, text=" Login ", padx=20, pady=20)
        login_frame.pack(pady=20, fill="both", expand=True, padx=40)
        
        tk.Label(login_frame, text="Benutzername:").pack(anchor="w", pady=5)
        self.entry_user = tk.Entry(login_frame, font=("Arial", 11))
        self.entry_user.pack(fill="x", pady=5)
        
        tk.Label(login_frame, text="Passwort:").pack(anchor="w", pady=5)
        self.entry_password = tk.Entry(login_frame, show="*", font=("Arial", 11))
        self.entry_password.pack(fill="x", pady=5)
        
        # Login Button
        tk.Button(login_frame, text="Verbindung herstellen", bg="#4CAF50", fg="white", 
                  font=("Arial", 11, "bold"), command=self.verarbeite_login).pack(fill="x", pady=20)

    def verarbeite_login(self):
        user = self.entry_user.get().strip()
        password = self.entry_password.get()
        
        if not user:
            messagebox.showwarning("Eingabe fehlt", "Bitte einen Benutzernamen eingeben.")
            return

        # Testverbindung aufbauen
        test_verbindung = db_verbindung_herstellen(user, password)
        if test_verbindung:
            test_verbindung.close()
            self.current_user = user
            self.current_password = password
            # Wechsel ins Hauptmenü
            self.zeige_hauptmenue_ansicht()

    # --- ANSICHT: HAUPTMENÜ ---
    def zeige_hauptmenue_ansicht(self):
        self.clear_root()
        
        # Status-Kopfzeile
        status_frame = tk.Frame(self.root, bg="#eee", pady=10)
        status_frame.pack(fill="x")
        tk.Label(status_frame, text=f"Angemeldet als: {self.current_user.upper()}", 
                 font=("Arial", 10, "bold"), bg="#eee").pack(side="left", padx=15)
        tk.Button(status_frame, text="Ausloggen", command=self.zeige_login_ansicht, font=("Arial", 8)).pack(side="right", padx=15)

        tk.Label(self.root, text="Hauptmenü", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Menü-Buttons
        btn_style = {"font": ("Arial", 11), "pady": 10, "padx": 10}
        
        tk.Button(self.root, text="[1] Neuen Kunden anlegen (3NF)", command=self.zeige_kunde_ansicht, **btn_style).pack(fill="x", padx=50, pady=10)
        tk.Button(self.root, text="[2] Neue Bestellung erstellen", command=self.zeige_bestellung_ansicht, **btn_style).pack(fill="x", padx=50, pady=10)
        tk.Button(self.root, text="[3] Artikelbestand ändern", command=self.zeige_bestand_ansicht, **btn_style).pack(fill="x", padx=50, pady=10)
        
        # Beenden Button
        tk.Button(self.root, text="Programm beenden", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=self.root.quit).pack(side="bottom", fill="x", pady=20, padx=50)

    # --- FORMULAR: KUNDE ANLEGEN ---
    def zeige_kunde_ansicht(self):
        self.clear_root()
        tk.Label(self.root, text="Neuen Kunden anlegen (3NF)", font=("Arial", 14, "bold")).pack(pady=15)
        
        form_frame = tk.Frame(self.root)
        form_frame.pack(fill="both", expand=True, padx=40)
        
        # Eingabefelder definieren
        felder = ["Vorname", "Nachname", "Straße", "Hausnummer", "PLZ (5-stellig)", "Ort"]
        self.kunde_entries = {}
        
        for feld in felder:
            tk.Label(form_frame, text=f"{feld}:").pack(anchor="w", pady=2)
            entry = tk.Entry(form_frame, font=("Arial", 10))
            entry.pack(fill="x", pady=2)
            self.kunde_entries[feld] = entry
            
        tk.Button(form_frame, text="Kunde in DB speichern", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), 
                  command=self.speichere_kunde).pack(fill="x", pady=15)
        tk.Button(form_frame, text="Zurück", command=self.zeige_hauptmenue_ansicht).pack(fill="x")

    def speichere_kunde(self):
        # Daten aus GUI auslesen
        v = self.kunde_entries["Vorname"].get().strip()
        n = self.kunde_entries["Nachname"].get().strip()
        s = self.kunde_entries["Straße"].get().strip()
        h = self.kunde_entries["Hausnummer"].get().strip()
        plz = self.kunde_entries["PLZ (5-stellig)"].get().strip()
        ort = self.kunde_entries["Ort"].get().strip()
        
        if not (v and n and s and h and plz and ort):
            messagebox.showwarning("Eingabe unvollständig", "Bitte alle Felder ausfüllen!")
            return

        verbindung = db_verbindung_herstellen(self.current_user, self.current_password)
        if not verbindung: return
        cursor = verbindung.cursor()
        
        try:
            # Schritt 1: 3NF-Abfrage für den Ort
            cursor.execute("SELECT PLZ FROM orte WHERE PLZ = %s;", (plz,))
            if not cursor.fetchone():
                query_ort = "INSERT INTO orte (PLZ, Ort) VALUES (%s, %s);"
                cursor.execute(query_ort, (plz, ort))
            
            # Schritt 2: Kunde eintragen
            query_kunde = "INSERT INTO kunden (Vorname, Nachname, Strasse, Hausnummer, PLZ) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query_kunde, (v, n, s, h, plz))
            neue_id = cursor.lastrowid
            
            verbindung.commit()
            messagebox.showinfo("Erfolg", f"Kunde erfolgreich angelegt!\nGenerierte Kunden-ID: {neue_id}")
            self.zeige_hauptmenue_ansicht()
            
        except Error as e:
            verbindung.rollback()
            messagebox.showerror("Fehler", f"Datenbank-Fehler beim Anlegen:\n{e}")
        finally:
            cursor.close()
            verbindung.close()

    # --- FORMULAR: BESTELLUNG ERSTELLEN ---
    def zeige_bestellung_ansicht(self):
        self.clear_root()
        tk.Label(self.root, text="Neue Bestellung erstellen", font=("Arial", 14, "bold")).pack(pady=15)
        
        # Schritt 1: Kunden-ID
        kunden_frame = tk.LabelFrame(self.root, text=" 1. Kunde zuweisen ", padx=10, pady=10)
        kunden_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(kunden_frame, text="Kunden-ID:").pack(side="left", padx=5)
        self.entry_bestell_kunde = tk.Entry(kunden_frame, width=10, font=("Arial", 10))
        self.entry_bestell_kunde.pack(side="left", padx=5)
        
        # Schritt 2: Artikel hinzufügen
        artikel_frame = tk.LabelFrame(self.root, text=" 2. Artikel hinzufügen ", padx=10, pady=10)
        artikel_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(artikel_frame, text="Artikel-ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_art_id = tk.Entry(artikel_frame, width=10)
        self.entry_art_id.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(artikel_frame, text="Menge:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_art_menge = tk.Entry(artikel_frame, width=10)
        self.entry_art_menge.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Button(artikel_frame, text="Hinzufügen", bg="#ff9800", command=self.artikel_zur_liste_hinzufuegen).grid(row=0, column=4, padx=10, pady=2)
        
        # Vorschau-Liste der aktuellen Artikel-Positionen (Tkinter Treeview)
        self.tree = ttk.Treeview(self.root, columns=("Artikel", "Menge"), show="headings", height=5)
        self.tree.heading("Artikel", text="Artikel-ID")
        self.tree.heading("Menge", text="Menge")
        self.tree.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Schritt 3: Buchen & Abbrechen
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(btn_frame, text="Bestellung final buchen", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), 
                  command=self.speichere_bestellung).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Abbrechen / Zurück", command=self.zeige_hauptmenue_ansicht).pack(fill="x", pady=2)
        
        # Reset des temporären Speichers bei Ansichts-Aufruf
        self.temporaere_positionen = []

    def artikel_zur_liste_hinzufuegen(self):
        art_id = self.entry_art_id.get().strip()
        menge = self.entry_art_menge.get().strip()
        
        if not (art_id and menge):
            messagebox.showwarning("Eingabe fehlt", "Bitte Artikel-ID und Menge eingeben.")
            return
            
        # Zur Liste hinzufügen und Treeview aktualisieren
        self.temporaere_positionen.append((art_id, menge))
        self.tree.insert("", "end", values=(art_id, menge))
        
        # Felder leeren für nächsten Artikel
        self.entry_art_id.delete(0, tk.END)
        self.entry_art_menge.delete(0, tk.END)

    def speichere_bestellung(self):
        kunden_id = self.entry_bestell_kunde.get().strip()
        if not kunden_id:
            messagebox.showwarning("Kunde fehlt", "Bitte gib eine gültige Kunden-ID an.")
            return
        if not self.temporaere_positionen:
            messagebox.showwarning("Keine Positionen", "Die Bestellung enthält noch keine Artikel.")
            return
            
        verbindung = db_verbindung_herstellen(self.current_user, self.current_password)
        if not verbindung: return
        cursor = verbindung.cursor()
        
        try:
            # 1. Bestellkopf einfügen
            query_bestellung = "INSERT INTO bestellungen (Kunden_ID, Bestelldatum) VALUES (%s, NOW());"
            cursor.execute(query_bestellung, (kunden_id,))
            bestellung_id = cursor.lastrowid
            
            # 2. Artikelschleife (Positionen schreiben)
            for art_id, menge in self.temporaere_positionen:
                query_position = "INSERT INTO bestellpositionen (Bestellung_ID, Artikel_ID, Menge) VALUES (%s, %s, %s);"
                cursor.execute(query_position, (bestellung_id, art_id, menge))
                
            # 3. Transaktion erfolgreich abschließen
            verbindung.commit()
            messagebox.showinfo("Erfolg", f"Bestellung Nr. {bestellung_id} erfolgreich verbucht!")
            self.zeige_hauptmenue_ansicht()
            
        except Error as e:
            # Rollback löscht bei Fehlern (z.B. Fremdschlüsselfehler bei falscher Artikel-ID) das gesamte Paket
            verbindung.rollback()
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der Bestellung:\n{e}\n\nRollback ausgeführt.")
        finally:
            cursor.close()
            verbindung.close()

    # --- FORMULAR: BESTAND ÄNDERN ---
    def zeige_bestand_ansicht(self):
        self.clear_root()
        tk.Label(self.root, text="Artikelbestand aktualisieren", font=("Arial", 14, "bold")).pack(pady=15)
        
        form_frame = tk.LabelFrame(self.root, text=" Bestands-Update (Lager) ", padx=20, pady=20)
        form_frame.pack(pady=20, fill="x", padx=40)
        
        tk.Label(form_frame, text="Artikel-ID:").pack(anchor="w", pady=5)
        self.entry_bestand_art_id = tk.Entry(form_frame, font=("Arial", 11))
        self.entry_bestand_art_id.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Neuer Bestand:").pack(anchor="w", pady=5)
        self.entry_bestand_menge = tk.Entry(form_frame, font=("Arial", 11))
        self.entry_bestand_menge.pack(fill="x", pady=5)
        
        tk.Button(form_frame, text="Bestand aktualisieren", bg="#9C27B0", fg="white", font=("Arial", 11, "bold"), 
                  command=self.speichere_bestand).pack(fill="x", pady=15)
        tk.Button(form_frame, text="Zurück", command=self.zeige_hauptmenue_ansicht).pack(fill="x")

    def speichere_bestand(self):
        art_id = self.entry_bestand_art_id.get().strip()
        neuer_bestand = self.entry_bestand_menge.get().strip()
        
        if not (art_id and neuer_bestand):
            messagebox.showwarning("Eingabe unvollständig", "Bitte fülle beide Felder aus.")
            return
            
        verbindung = db_verbindung_herstellen(self.current_user, self.current_password)
        if not verbindung: return
        cursor = verbindung.cursor()
        
        try:
            query = "UPDATE artikel SET Bestand = %s WHERE Artikel_ID = %s;"
            cursor.execute(query, (neuer_bestand, art_id))
            verbindung.commit()
            
            messagebox.showinfo("Erfolg", f"Bestand für Artikel {art_id} wurde auf {neuer_bestand} gesetzt.")
            self.zeige_hauptmenue_ansicht()
        except Error as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren des Bestands:\n{e}")
        finally:
            cursor.close()
            verbindung.close()

# ==============================================================================
# HAUPTPROGRAMM (STARTPUNKT)
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PiDatenbankApp(root)
    root.mainloop()