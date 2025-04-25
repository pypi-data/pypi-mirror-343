import platform
import logging
import os
import shutil
import subprocess
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)

def update_fields(docx_path):
    """
    Update fields in a Word document using the best available method based on platform.
    
    Args:
        docx_path (str): Path to the Word document
        
    Returns:
        bool: True if fields were updated successfully, False otherwise
    """
    system = platform.system()
    
    # Try Windows COM automation first if available
    if system == "Windows":
        try:
            return _update_fields_windows(docx_path)
        except ImportError:
            logger.info("pywin32 nicht installiert. Versuche LibreOffice Methode.")
            return _update_fields_libreoffice(docx_path)
    
    # Für nicht-Windows Systeme, versuche LibreOffice
    return _update_fields_libreoffice(docx_path)

def _update_fields_windows(docx_path):
    """Windows-spezifische Implementierung mit pywin32"""
    try:
        import win32com.client
        
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))
        
        # Alle Felder im Dokument aktualisieren
        for i in range(doc.Fields.Count):
            doc.Fields(i+1).Update()
            
        # Speichern und schließen
        doc.Save()
        doc.Close()
        word.Quit()
        
        logger.info(f"Felder erfolgreich mit Windows COM in {docx_path} aktualisiert")
        return True
        
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren der Felder mit Windows COM: {str(e)}")
        return False

def _update_fields_libreoffice(docx_path):
    """Cross-platform Implementierung mit LibreOffice"""
    # LibreOffice ausführbare Datei je nach Plattform bestimmen
    if platform.system() == "Windows":
        libreoffice_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]
        soffice = next((path for path in libreoffice_paths if os.path.exists(path)), None)
    elif platform.system() == "Darwin":  # macOS
        soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    else:  # Linux
        soffice = shutil.which("soffice")  # Sucht nach soffice im PATH
    
    if not soffice:
        logger.error("LibreOffice nicht gefunden. Bitte installieren, um Felder zu aktualisieren.")
        return False
    
    # Temporäres Verzeichnis erstellen
    with tempfile.TemporaryDirectory() as temp_dir:
        # Absoluter Pfad zum Dokument
        abs_docx_path = os.path.abspath(docx_path)
        
        # Backup des Originaldokuments erstellen
        backup_path = abs_docx_path + ".backup"
        shutil.copy2(abs_docx_path, backup_path)
        
        try:
            # Felder mit LibreOffice aktualisieren
            cmd = [
                soffice,
                "--headless",
                "--convert-to", "docx",
                "--outdir", temp_dir,
                abs_docx_path
            ]
            
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Name der Ausgabedatei (könnte sich die Erweiterung geändert haben)
            base_name = os.path.basename(docx_path)
            output_file = os.path.join(temp_dir, os.path.splitext(base_name)[0] + ".docx")
            
            # Originaldatei mit der aktualisierten ersetzen
            if os.path.exists(output_file):
                shutil.copy2(output_file, abs_docx_path)
                # Backup löschen bei Erfolg
                os.remove(backup_path)
                logger.info(f"Felder erfolgreich mit LibreOffice in {docx_path} aktualisiert")
                return True
            else:
                # Bei Fehlschlag das Backup wiederherstellen
                shutil.copy2(backup_path, abs_docx_path)
                os.remove(backup_path)
                logger.error("LibreOffice hat keine Ausgabedatei erstellt")
                return False
                
        except Exception as e:
            # Bei Fehler das Backup wiederherstellen
            shutil.copy2(backup_path, abs_docx_path)
            os.remove(backup_path)
            logger.error(f"Fehler mit LibreOffice: {e}")
            return False

def simple_field_update(docx_path):
    """
    Einfache Textfelderaktualisierung für Datum und Zeit.
    Funktioniert auf allen Plattformen ohne externe Abhängigkeiten.
    """
    try:
        from docx import Document
        
        doc = Document(docx_path)
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Felder in Paragraphen suchen und ersetzen
        for para in doc.paragraphs:
            if "DATE" in para.text:
                para.text = para.text.replace("DATE", current_date)
            if "TIME" in para.text:
                para.text = para.text.replace("TIME", current_time)
        
        # Dokument speichern
        doc.save(docx_path)
        logger.info(f"Einfache Felder in {docx_path} aktualisiert")
        return True
    except Exception as e:
        logger.error(f"Fehler bei einfacher Feldaktualisierung: {e}")
        return False