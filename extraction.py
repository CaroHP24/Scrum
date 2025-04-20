import re
import os
import sys
# Vérifie si une ligne contient une affiliation (université, institut, adresse mail, etc.)
def is_affiliation_line(line):
    line = line.lower()
    return any(keyword in line for keyword in [
        "university", "institute", "department", "school", "college",
        "columbia", "@", "email", "avenue", "street", "parkway", "city"
    ])
# Vérifie si une ligne contient probablement une liste d’auteurs
# Exemple : "Juan-Manuel Torres-Moreno, Horacio Saggion, Iria da Cunha"
def is_likely_author(line):
    if line.count(",") >= 2 and re.search(r"[A-Z][a-z]+", line):
        return True
    if len(re.findall(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+", line)) >= 2:
        return True
    return False

# Extrait le titre à partir des premières lignes du fichier
# Il s'arrête dès qu'une ligne ressemble à une liste d’auteurs ou une affiliation
def extract_title(lines):
    title_lines = []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        lower = clean.lower()
        if "@" in lower or any(word in lower for word in [
            "university", "department", "institute", "school", "college",
            "city", "avenue", "street", "laboratory"
        ]):
            break

        # Stop aussi si ligne semble être une liste de noms
        if re.search(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+", clean) and clean.count(",") >= 1:
            break

        title_lines.append(clean)

    bloc = " ".join(title_lines)
    return bloc if 5 <= len(bloc.split()) <= 30 else "(Titre non trouvé)"

# Extrait le résumé entre "Abstract"/"Résumé" et "Introduction"
# Prend en charge les cas où l'abstract commence sur la même ligne que "Abstract"
def extract_abstract(lines):
    abstract_lines = []
    in_abstract = False

    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()

        if not in_abstract:
            if "abstract" in lower_line or "résumé" in lower_line:
                match = re.search(r"(abstract|résumé)[\s:\-]*", lower_line)
                if match:
                    start_index = match.end()
                    after = clean_line[start_index:].strip()
                    if after:
                        abstract_lines.append(after)
                in_abstract = True
                continue

        elif "introduction" in lower_line:
            break

        elif in_abstract:
            abstract_lines.append(clean_line)

    return " ".join(abstract_lines).strip() if abstract_lines else "(Résumé non trouvé)"


# Fonction pour extraire le titre à partir d'un chemin de fichier
def extract_title_from_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return extract_title(lines)
    except FileNotFoundError:
        return "Fichier non trouvé."
    except Exception as e:
        return f"Erreur lors de la lecture : {e}"
    
# Fonction pour extraire le résumé à partir d'un chemin de fichier

def extract_abstract_from_file(filepath):
    try: 
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return extract_abstract(lines)
    except FileNotFoundError:
        return "Fichier non trouvé."
    except Exception as e:
        return f"Erreur lors de la lecture : {e}"
# Fonction pour extraire le titre et le résumé à partir d'un chemin de fichier