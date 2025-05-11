import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def generate_article_xml(preamble, titre, auteur, abstract, biblio, output_path):
    article = ET.Element("article")

    ET.SubElement(article, "preamble").text = preamble
    ET.SubElement(article, "titre").text = titre
    ET.SubElement(article, "auteur").text = auteur
    ET.SubElement(article, "abstract").text = abstract
    ET.SubElement(article, "biblio").text = biblio

    # Convertir en string puis le reformater avec minidom pour pretty-print, chaque ligne seule, pas d'encombrement
    rough_string = ET.tostring(article, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Écrire dans le fichier
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Fichier XML bien formaté généré : {output_path}")

"""
if __name__ == "__main__":
    # Exemple d'exécution sur les variables déjà récupérées de vos codes
    preamble = "sample_paper.pdf"
    titre = "An Introduction to Scientific Parsing"
    auteur = "Alice Dupuis, Université de Bordeaux\nalice.dupuis@u-bordeaux.fr"
    abstract = "This paper presents a parser for scientific articles..."
    biblio = "[1] J. Smith, 'Parsing Basics', 2021.\n[2] A. Dupuis, 'XML for NLP', 2023."
    output_path = "article_sample.xml"

    generate_article_xml(preamble, titre, auteur, abstract, biblio, output_path)
"""
