import os
import shutil

# Path to the temporary TXT directory used in amel.py
TMP_TXT_DIR = os.path.join("pdf_input", "tmp_txt")

def delete_temp_files():
    if os.path.exists(TMP_TXT_DIR): #if the directory exists
        shutil.rmtree(TMP_TXT_DIR) #delete it
        print(f"[+] Dossier temporaire supprimé : {TMP_TXT_DIR}")
    else: #if it doesn't exist
        print(f"[-] Aucun dossier temporaire à supprimer : {TMP_TXT_DIR}")

if __name__ == "__main__":
    delete_temp_files()