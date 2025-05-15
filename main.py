import os  # manipuler les chemins de fichiers et répertoires
import shutil   # opérations sur des fichiers/dossiers
import subprocess   # exécuter des commandes externes (les .exe)

import tkinter as tk  # interface graphique
from tkinter import filedialog  # boîte de dialogue pour sélectionner des fichiers

import argparse
import re

from generation import *
from extraction import *
from deleteTmp import *
from extract_corps import *
from extract_discussion import *

def sanitize_xml_text(text):
    if not text:
        return ""
    return re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u00A0-\uD7FF\uE000-\uFFFD]', '', text)

# ========== CONFIGURATION ==========
PDF_INPUT_DIR = "pdf_input"
TMP_TXT_DIR = os.path.join(PDF_INPUT_DIR, "tmp_txt")
OUTPUT_DIR = "final_output"

# ========== PRÉPARATION DES DOSSIERS ==========
def clean_and_prepare_dirs():
    for folder in [TMP_TXT_DIR, OUTPUT_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
        print(f"[+] Dossier '{folder}' prêt.")

# ========== CONVERSION PDF --> TEXTE ==========
def convert_pdf_to_text():
    # Ouvre une popup pour sélectionner les fichiers PDF
    root = tk.Tk()
    root.withdraw()  # Ne pas afficher la fenêtre principale
    pdf_paths = filedialog.askopenfilenames(
        title="Sélectionnez les fichiers PDF",
        filetypes=[("Fichiers PDF", "*.pdf")]
    )

    if not pdf_paths:
        print("Aucun fichier PDF sélectionné.")
        return []

    for pdf_path in pdf_paths:
        pdf_file = os.path.basename(pdf_path)
        txt_name = os.path.splitext(pdf_file)[0] + ".txt"
        txt_path = os.path.join(TMP_TXT_DIR, txt_name)

        try:
            subprocess.run(["pdftotext", "-raw", pdf_path, txt_path], check=True)
            print(f"Converti : {pdf_file}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur de conversion pour {pdf_file} : {e}")


# ========== VERSIONS FINALES ==========
def final_treatement():
    for fich in os.listdir(TMP_TXT_DIR):
        fichFinal = parse_filename(fich)
        chemin_sortie = os.path.join(OUTPUT_DIR, fichFinal)

        with open(chemin_sortie, "w", encoding="utf-8") as f:
            filename = fich.replace(".txt", ".pdf")
            extracted_title = extract_title_from_file(os.path.join(TMP_TXT_DIR, fich))
            extracted_abstract = extract_abstract_from_file(os.path.join(TMP_TXT_DIR, fich))

            f.write(filename + "\n")
            f.write(extracted_title + "\n")
            f.write(extracted_abstract + "\n")

def txt_parse():
    clean_and_prepare_dirs()
    convert_pdf_to_text()
    final_treatement()
    print("\nTraitement terminé. Fichiers finaux disponibles dans 'sorties/'.")
    delete_temp_files()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action="store_true", help="Convertir les fichiers PDF en texte et extraire les informations.")
    parser.add_argument("-x", action="store_true", help="Convertir les fichiers PDF en XML et extraire les informations.")

    args = parser.parse_args()

    if args.t:
        txt_parse()
    elif args.x:
        from xml_parse import generate_article_xml

        clean_and_prepare_dirs()
        convert_pdf_to_text()

        for fich in os.listdir(TMP_TXT_DIR):
            fichFinal = parse_filename(fich).replace(".txt", ".xml")
            chemin_sortie = os.path.join(OUTPUT_DIR, fichFinal)

            txt_path = os.path.join(TMP_TXT_DIR, fich)
            pdf_filename = fich.replace(".txt", ".pdf")

            with open(txt_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            titre = sanitize_xml_text(extract_title(lines))
            auteur = sanitize_xml_text(extract_authors(lines))
            abstract = sanitize_xml_text(extract_abstract(lines))
            biblio = sanitize_xml_text(extract_references(lines))
            corps= sanitize_xml_text(extract_corps((lines))
            discussion = sanitize_xml_text(extract_discussion((lines))

            generate_article_xml(
                preamble=pdf_filename,
                titre=titre,
                auteur=auteur,
                abstract=abstract,
                biblio=biblio,
                corps=corps,
                discussion=discussion,
                output_path=chemin_sortie
            )

        print("\nExtraction XML terminée. Fichiers disponibles dans 'final_output/'.")
        delete_temp_files()
    else:
        print("Aucune option spécifiée. Utilisez -t pour le traitement texte ou -x pour le traitement XML.")

if __name__ == "__main__":
    main()
