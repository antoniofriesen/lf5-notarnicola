-- ==============================================================================
-- BERECHTIGUNGSSYSTEM FÜR DIE DATENBANK "BS14"
-- Ausführung: Auf dem Raspberry Pi (z.B. via HeidiSQL) NACHDEM Tabellen & Daten stehen.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. ALTE BENUTZER LÖSCHEN (Optional, verhindert Fehler bei wiederholter Ausführung)
-- ------------------------------------------------------------------------------
DROP USER IF EXISTS 'vertrieb_user'@'localhost';
DROP USER IF EXISTS 'lager_user'@'localhost';
DROP USER IF EXISTS 'management_user'@'localhost';
DROP USER IF EXISTS 'db_admin'@'localhost';


-- ------------------------------------------------------------------------------
-- 2. BENUTZER NEU ANLEGEN
-- Da GUI und DB auf demselben Pi laufen, nutzen wir 'localhost' statt '%'
-- ------------------------------------------------------------------------------
CREATE USER 'vertrieb_user'@'localhost' IDENTIFIED BY 'VertriebsPasswort2026!';
CREATE USER 'lager_user'@'localhost' IDENTIFIED BY 'LagerPasswort2026!';
CREATE USER 'management_user'@'localhost' IDENTIFIED BY 'ManagementPasswort2026!';
CREATE USER 'db_admin'@'localhost' IDENTIFIED BY 'AdminPasswort2026!';


-- ------------------------------------------------------------------------------
-- 3. RECHTE VERGEBEN (Rollenkonzept nach DSGVO / Zweckbindung)
-- ------------------------------------------------------------------------------

-- >>> RECHTE FÜR DEN VERTRIEB (Einsehen und Bearbeiten von Kunden & Bestellungen)
GRANT SELECT, INSERT, UPDATE ON BS14.kunden TO 'vertrieb_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON BS14.bestellungen TO 'vertrieb_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON BS14.bestellpositionen TO 'vertrieb_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON BS14.artikel TO 'vertrieb_user'@'localhost';

-- >>> RECHTE FÜR DAS LAGER (Bestellungen einsehen, aber nur Artikelbestände/Daten ändern)
GRANT SELECT ON BS14.kunden TO 'lager_user'@'localhost';
GRANT SELECT ON BS14.bestellungen TO 'lager_user'@'localhost';
GRANT SELECT ON BS14.bestellpositionen TO 'lager_user'@'localhost';
GRANT SELECT, UPDATE ON BS14.artikel TO 'lager_user'@'localhost';

-- >>> RECHTE FÜR DAS MANAGEMENT (Reine Lese-Rechte für Analysen und Berichte)
GRANT SELECT ON BS14.kunden TO 'management_user'@'localhost';
GRANT SELECT ON BS14.bestellungen TO 'management_user'@'localhost';
GRANT SELECT ON BS14.bestellpositionen TO 'management_user'@'localhost';
GRANT SELECT ON BS14.artikel TO 'management_user'@'localhost';

-- >>> RECHTE FÜR DEN DATENBANK-ADMINISTRATOR (Vollzugriff auf die gesamte Datenbank)
GRANT ALL PRIVILEGES ON BS14.* TO 'db_admin'@'localhost';


-- ------------------------------------------------------------------------------
-- 4. RECHTE IM SYSTEM AKTIVIEREN
-- ------------------------------------------------------------------------------
FLUSH PRIVILEGES;