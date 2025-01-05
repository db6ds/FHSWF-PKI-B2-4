# Bildverarbeitungs- und Steganographie-Tool
** Gruppe: PKI-B2-4 **

## Überblick
Diese Anwendung ist ein vielseitiges Bildverarbeitungstool mit integrierter [Steganographie-Funktionalität](docs/README-StegoTool). Es ermöglicht Benutzern, Bilder auf verschiedene Arten zu bearbeiten und zu analysieren sowie versteckte Informationen in Bildern zu speichern.

## Hauptfunktionen

### Bildbearbeitung
- **Grundlegende Transformationen**
  - Drehen (90° im Uhrzeigersinn)
  - Horizontales Spiegeln
  - Helligkeitsanpassung (Aufhellen/Abdunkeln)

- **Filter und Effekte**
  - Schwarz-Weiß-Konvertierung
  - Sepia-Effekt
  - Verpixelung
  - Bildschärfung

- **Bereichsbasierte Bearbeitung**
  - Selektive Filteranwendung auf ausgewählte Bildbereiche
  - Unterstützt alle verfügbaren Filter für Teilbereiche

### Gesichtserkennung
- Automatische Erkennung von Gesichtern im Bild
- Markierung erkannter Gesichter
- Basiert auf OpenCV's Haar-Cascade-Klassifikator

### Steganographie
- **LSB (Least Significant Bit) Steganographie**
  - Verstecken von Text oder Dateien in Bildern
  - Extraktion versteckter Daten
  - LSB-Analysefunktion zur Erkennung versteckter Daten
- Unterstützt PNG-Format für verlustfreie Steganographie

## Benutzeroberfläche
- Übersichtliche grafische Benutzeroberfläche
- Zwei-Fenster-Ansicht (Original und bearbeitetes Bild)
- Informationsbereich für Bilddetails und Statusmeldungen
- Intuitive Bereichsauswahl mittels Mausinteraktion

## Technische Features
- Unterstützt gängige Bildformate (PNG, JPG, JPEG, BMP)
- Effiziente Bildverarbeitung durch NumPy und OpenCV
- Robuste Fehlerbehandlung
- Nicht-destruktive Bearbeitung mit Zurücksetzfunktion

## Systemanforderungen
- Python 3.x
- Tkinter für die GUI
- OpenCV für Bildverarbeitung und Gesichtserkennung
- PIL/Pillow für Bildmanipulation
- NumPy für numerische Operationen

# Installation
Diese Anleitung beschreibt die Installation der erforderlichen Komponenten für Linux, macOS und Windows.

## Voraussetzungen für alle Systeme

- Python 3.x
- pip (Python Package Manager)
- Git (optional, für das Klonen des Repositories)
- TK

## Projekt herunterladen

### Option 1: Git Repository klonen
```bash
git clone https://github.com/db6ds/FHSWF-PKI-B2-4.git
cd FHSWF-PKI-B2-4
```

### Option 2: ZIP-Datei herunterladen
Alternativ kann das Projekt als ZIP-Datei heruntergeladen und entpackt werden.

## Installation

### 1. Systemabhängigkeiten installieren
#### Linux
Im Terminal:
```bash
sudo apt-get update && sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    x11-apps \
    libgl1-mesa-glx \
    libglib2.0-0
```

#### macOS-Installation
##### a) Homebrew installieren
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
##### b) Python installieren
```bash
brew install python3
```
##### c) Tkinter installieren
###### Option 1: Installation via brew
```bash
brew install python-tk
```
oder 
```bash
brew install tk
```
###### Option 2: Installation via Python
```bash
python -m pip install tk
```

#### Windows-Installation
##### a) Python installieren
1. unter [python.org](https://www.python.org/downloads/)
2. die neueste Python 3.x Version herunterladen
3. den Installer ausführen
4. **Wichtig:** die Option "Add Python to PATH" während der Installation aktivieren
##### b) TK installieren:
```bash
python -m pip install tk
```


### 2. Python-Abhängigkeiten installieren
Im Projektverzeichnis ausführen:
```bash
pip3 install -r requirements.txt
```

### 3. Programm starten
```bash
python3 main.py
```


## Support

Bei Problemen mit der Installation:
1. Überprüfen Sie die Python-Version: `python3 --version`
2. Überprüfen Sie die pip-Version: `pip3 --version`
3. Stellen Sie sicher, dass alle Abhängigkeiten korrekt installiert sind: `pip3 list`
4. Konsultieren Sie die Fehlerbehebungshinweise oben
