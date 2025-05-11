import os  # manipuler les chemins de fichiers et répertoires
import shutil   # opérations sur des fichiers/dossiers
import subprocess   # exécuter des commandes externes (les .exe)

from generation import *
from extraction import *
from deleteTmp import *

# ========== CONFIGURATION ==========
PDF_INPUT_DIR = "pdf_input"   # Répertoire des fichiers pdf
TMP_TXT_DIR = os.path.join(PDF_INPUT_DIR, "tmp_txt")  # Son ss répertoire contenant les versions .txt temporaires de chaque .pdf
OUTPUT_DIR = "final_output"   #  Répertoire des versions .txt finales (extraction du titre et résumé avec le bon nom)

# ========== PRÉPARATION DES DOSSIERS ==========
def clean_and_prepare_dirs():
    for folder in [TMP_TXT_DIR, OUTPUT_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)  # si un des dossiers de sortie existe déjà, on le supprime entièrement
        os.makedirs(folder)  # les recréer vides à chaque nouvelle exécution
        print(f"[+] Dossier '{folder}' prêt.")

# ========== CONVERSION PDF --> TEXTE ==========
def convert_pdf_to_text():

    # parcourir les fichiers du dossier PDF_INPUT_DIR, et garder uniquement les .pdf
    pdf_files = [
        f for f in os.listdir(PDF_INPUT_DIR)
        if f.lower().endswith(".pdf") and not f.startswith("tmp_txt")
    ]

    if not pdf_files:
        print(" Aucun fichier PDF trouvé.")
        return []

    # Pour chaque fichier PDF trouvé
    for pdf_file in pdf_files:           
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_file)   # Chemin complet vers le fichier PDF
        txt_name = os.path.splitext(pdf_file)[0] + ".txt"  # Nom du fichier .txt correspondant (garder le nom du pdf, sans convertir les espaces en _)
        txt_path = os.path.join(TMP_TXT_DIR, txt_name)     # Chemin complet du fichier texte à créer

        try:
            subprocess.run(["pdftotext", "-raw", pdf_path, txt_path], check=True)  # conversion
            print(f"Converti : {pdf_file}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur de conversion pour {pdf_file} : {e}")


# ========== VERSIONS FINALES ==========

# Executer l'extraction sur les .txt du dossier temporaire, et mettre les versions finales dans le dossier sorties/
def final_treatement():
    # Parcourir les .txt du dossier temporaire
    for fich in os.listdir(TMP_TXT_DIR):
            # Appliquer l'extraction et écrire le nom dans le bon format (une ligne et _ à la place des espaces)
            fichFinal = parse_filename(fich)
            
            # Définir le chemin de sortie dans le dossier 'sorties'
            chemin_sortie = os.path.join(OUTPUT_DIR, fichFinal)

            # Écrire le contenu (j'ai mis une ligne fictive ici)
            with open(chemin_sortie, "w", encoding="utf-8") as f:
                #Extraction et parsage des infos
                filename = fich.replace(".txt", ".pdf") 
                extracted_title = extract_title_from_file(os.path.join(TMP_TXT_DIR, fich))
                extracted_abstract = extract_abstract_from_file(os.path.join(TMP_TXT_DIR, fich))

                # Écrire les informations dans le fichier de sortie
                f.write(filename + "\n")
                f.write(extracted_title + "\n")
                f.write(extracted_abstract + "\n")

def main():
    clean_and_prepare_dirs()
    convert_pdf_to_text()
    final_treatement()
    print("\nTraitement terminé. Fichiers finaux disponibles dans 'final_output/'.")
    delete_temp_files()  # Supprimer les fichiers temporaires après traitement

if __name__ == "__main__":
    main()
