import platform
import logging
import os
import shutil
import subprocess
import tempfile

logger = logging.getLogger(__name__)

def update_fields(docx_path):
    """
    Update fields in a Word document using LibreOffice.
    
    Args:
        docx_path (str): Path to the Word document
        
    Returns:
        bool: True if fields were updated successfully, False otherwise
    """
    return update_fields_libreoffice(docx_path)

def update_fields_libreoffice(docx_path):
    """Cross-platform implementation using LibreOffice"""
    # Find LibreOffice executable
    if platform.system() == "Windows":
        libreoffice_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]
        soffice = next((path for path in libreoffice_paths if os.path.exists(path)), None)
    elif platform.system() == "Darwin":  # macOS
        soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if not os.path.exists(soffice):
            soffice = None
    else:  # Linux
        soffice = shutil.which("soffice")
    
    if not soffice:
        logger.warning("LibreOffice nicht gefunden. Felder können nicht aktualisiert werden.")
        return False
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Absolute path to the document
        abs_docx_path = os.path.abspath(docx_path)
        
        # Backup the original document
        backup_path = abs_docx_path + ".backup"
        shutil.copy2(abs_docx_path, backup_path)
        
        try:
            # Update fields with LibreOffice
            cmd = [
                soffice,
                "--headless",
                "--convert-to", "docx",
                "--outdir", temp_dir,
                abs_docx_path
            ]
            
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Get the output filename
            base_name = os.path.basename(docx_path)
            output_file = os.path.join(temp_dir, os.path.splitext(base_name)[0] + ".docx")
            
            # Replace the original file with the updated one
            if os.path.exists(output_file):
                shutil.copy2(output_file, abs_docx_path)
                os.remove(backup_path)
                logger.info(f"Felder erfolgreich mit LibreOffice in {docx_path} aktualisiert")
                return True
            else:
                # Restore backup if something went wrong
                shutil.copy2(backup_path, abs_docx_path)
                os.remove(backup_path)
                logger.error("LibreOffice hat keine Ausgabedatei erstellt")
                return False
                
        except Exception as e:
            # Restore backup if there was an error
            shutil.copy2(backup_path, abs_docx_path)
            os.remove(backup_path)
            logger.error(f"Fehler mit LibreOffice: {e}")
            return False