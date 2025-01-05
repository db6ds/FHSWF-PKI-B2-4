# Steganographie Tool
# steganotool.py
### Author: Daniel Stabenau
### Mat.: 71300017
### Gruppe: B2-4

# Technische Dokumentation

## Übersicht
Das Steganographie Tool ist eine Python-Anwendung mit grafischer Benutzeroberfläche, die es ermöglicht, Daten in PNG-Bildern zu verstecken und wieder auszulesen. Die Anwendung nutzt die LSB (Least Significant Bit) Methode zur Steganographie und bietet zusätzlich Analysefunktionen zur Erkennung versteckter Daten.

## Entwicklungsumgebung und Tools

### Technische Anforderungen
- Python 3.x
- Benötigte Bibliotheken:
  - tkinter: Für die grafische Benutzeroberfläche
  - PIL (Python Imaging Library): Zur Bildverarbeitung
  - numpy: Für effiziente Array-Operationen
  - matplotlib: Zur Visualisierung der Analysen

### Entwicklungsunterstützung
Bei der Entwicklung wurden folgende KI-Tools zur Unterstützung eingesetzt:
- Claude.ai: Für die Erstellung von Codefragmenten und Dokumentation
- ChatGPT: Für Debugging-Unterstützung und Code-Optimierung
- Ollama mit Mixtral: Für Code-Review und Problemlösung

Diese KI-Tools wurden verwendet zur Unterstützung bei der:
- Code-Generierung und -Optimierung
- Fehleranalyse und Debugging
- Erstellung der technischen Dokumentation
- Implementierung der LSB-Algorithmen


## Hauptfunktionen

### 1. Steganographie
- **Encoding**: Versteckt Text oder Dateien in PNG-Bildern durch LSB-Manipulation
- **Decoding**: Extrahiert versteckte Daten aus präparierten PNG-Bildern
- **Kapazitätsberechnung**: Automatische Berechnung der verfügbaren Speicherkapazität

### 2. Analyse
- LSB-Verteilungsanalyse
- Differenzbildanalyse
- Visuelle Darstellung der LSB-Ebene

## Klassenstruktur

### Klasse: SteganographyTool
Hauptklasse der Anwendung, die alle Funktionalitäten implementiert.

#### Wichtige Methoden

##### `__init__(self, root)`
- Initialisiert die Hauptanwendung
- Erstellt das Hauptfenster und alle GUI-Elemente
- Setzt initiale Zustände der Steuerelemente

##### `open_file(self, mode)`
- Parameter:
  - mode: 'normal' für Bildauswahl, 'stegofile' für zu versteckende Datei
- Öffnet Dateiauswahldialog
- Prüft Dateigröße und Kompatibilität

##### `encode(self)`
- Versteckt Daten im ausgewählten Bild
- Unterstützt Text- und Datei-Modus
- Fügt Größeninformation am Anfang hinzu
- Erstellt Differenzvisualisierung

##### `decode(self)`
- Extrahiert versteckte Daten aus dem Bild
- Liest Größeninformation
- Konvertiert LSB-Daten zurück in ursprüngliches Format

##### `analyse_image(self)`
- Erstellt detaillierte LSB-Analyse
- Visualisiert LSB-Verteilung
- Vergleicht mit Normalverteilung

## Implementierungsdetails

### LSB-Steganographie
Die Implementierung nutzt den Least Significant Bit (LSB) jedes Farbkanals:
1. Daten werden in Binärform konvertiert
2. Jedes Bit wird im LSB eines Pixels gespeichert
3. Die ersten 32 Bits enthalten die Größeninformation
4. Vektorisierte Operationen mit numpy für bessere Performance

### Sicherheitsaspekte
- Keine Verschlüsselung implementiert
- Versteckte Daten sind durch LSB-Analyse erkennbar
- Geeignet für nicht-kritische Anwendungen

### GUI-Design
- Modularer Aufbau mit separaten Frames
- Responsive Layout
- Statusabhängige Button-Aktivierung
- Integrierte Bildvorschau

## Nutzungsbeispiele

### Text verstecken:
1. "Bild auswählen" klicken und PNG-Datei wählen
2. Text-Modus auswählen
3. Text eingeben
4. "Encodieren" klicken
5. Ausgabedatei speichern

### Datei verstecken:
1. "Bild auswählen" klicken und PNG-Datei wählen
2. Datei-Modus auswählen
3. "Select" klicken und zu versteckende Datei wählen
4. "Encodieren" klicken
5. Ausgabedatei speichern

### Daten extrahieren:
1. Präpariertes Bild öffnen
2. Entsprechenden Modus wählen (Text/Datei)
3. "Decodieren" klicken

## Verbesserungsmöglichkeiten
1. Implementierung von Verschlüsselung
2. Unterstützung weiterer Bildformate
3. Fortschrittsanzeige bei großen Dateien
4. Komprimierung der zu versteckenden Daten
5. Fehlerkorrektur für robustere Datenspeicherung