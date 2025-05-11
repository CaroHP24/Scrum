import re

def extract_authors(lines):
    authors = []
    used_emails = set()
    candidate_names = []
    found_bulk_names = False

    # 1. Extraire ligne avec plusieurs noms séparés par and ou ,
    for line in lines:
        if not found_bulk_names:
            if re.search(r"[A-Z][a-z]+(?:\s+[A-Z][a-z\.-]+)+.*(,|and).*", line):
                names_raw = re.split(r",|\band\b", line)
                candidate_names = [clean_author_line(name.strip()) for name in names_raw if len(name.strip().split()) >= 2]
                found_bulk_names = True
        if found_bulk_names:
            break

    # 2. Extraire tous les emails
    all_emails = []
    for line in lines:
        if '@' in line:
            matches = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", line)
            all_emails.extend([m.strip("<>(){}.,; ") for m in matches])

    # 3. Associer noms ↔ emails si compte égal
    if len(candidate_names) == len(all_emails):
        authors = [f"{name} <{email}>" for name, email in zip(candidate_names, all_emails)]
    else:
        for i, line in enumerate(lines):
            if '@' not in line:
                continue
            emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", line)
            if not emails:
                continue
            for email in emails:
                email_clean = email.strip("<>(){}.,; ")
                if email_clean in used_emails:
                    continue
                name = None
                for j in range(i - 1, max(i - 5, -1), -1):
                    candidate = lines[j].strip()
                    if not candidate or is_email_line(candidate) or is_affiliation(candidate):
                        continue
                    if re.search(r"[0-9]{2,}", candidate):
                        continue
                    name_match = re.findall(r"\b[A-Z][a-z\-]+(?:\s+[A-Z][a-z\-\.]+)+\b", candidate)
                    if name_match:
                        name = clean_author_line(candidate.strip(" ,"))
                        break
                if name:
                    authors.append(f"{name} <{email_clean}>")
                    used_emails.add(email_clean)

    return "\n".join(authors) if authors else "(Auteurs non trouvés)"

def is_email_line(line):
    return '@' in line

def is_affiliation(line):
    keywords = [
        "university", "college", "school", "institute", "laboratory", "computer", "science", "chemin", "france", "canada",
        "faculty", "center", "centre", "department", "street", "avenue", "japan", "JAPAN", "of", "BBN", "technologies", 
        "mountain", "inc.", "city", "park", "maryland", "usa", "germany", "laboratoire", "linguistics", "katholieke", 
        "universiteit", "theresiastraat", "leuven", "belgium", "google", "CA", "speech", "international"
    ]
    return any(k in line.lower() for k in keywords)

def clean_author_line(line):
    line = re.sub(r"(\w)\d+\b", r"\1", line)
    return re.sub(r"\s{2,}", " ", line).strip()
def extract_title(lines):
    title_lines = []
    skip_keywords = [
        "university", "department", "institute", "school", "college", "city",
        "avenue", "street", "laboratory", "@", "abstract", "résumé"
    ]

    def looks_like_author_names(line):
        return bool(re.search(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", line)) and (" and " in line or "," in line)

    started = False
    for line in lines:
        clean = line.strip()
        lower = clean.lower()

        if re.match(r"(arxiv|doi|issn|isbn)", lower):
            continue

        if any(k in lower for k in skip_keywords):
            if started:
                break
            else:
                continue

        if not clean:
            continue

        word_count = len(clean.split())
        if word_count < 2 or word_count > 12:
            if started:
                break
            else:
                continue

        # stop si ligne 2 ressemble à auteur
        if started and looks_like_author_names(clean):
            break

        title_lines.append(line)
        started = True

        if len(title_lines) >= 2:
            break

    title = " ".join(title_lines)
    return title if 3 <= len(title.split()) <= 30 else "(Titre non trouvé)"


def extract_abstract(lines):
    abstract_lines = []
    in_abstract = False

    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()

        if not in_abstract:
            if line_lower.startswith("abstract") or line_lower.startswith("résumé"):
                in_abstract = True
                # Supprime "Abstract—" ou "Résumé—" et garde le reste
                content = re.sub(r"^(abstract|résumé)\s*[-:—]*\s*", "", line, flags=re.IGNORECASE)
                if content:
                    abstract_lines.append(content.strip())
        else:
            if re.match(r"^(index\s+terms|introduction|\d+)", line_lower):
                break
            abstract_lines.append(line_clean)

    return " ".join(abstract_lines).strip() if abstract_lines else "(Résumé non trouvé)"



def extract_references(lines):
    ref_start_keywords = ["references", "références", "bibliographie", "r eferences"]
    noise_keywords = [
        "p-value", "rouge", "table", "figure", "polibits", "acknowledgment",
        "author", "received", "abstract", "measure", "0.", "js", "sm", "index"
    ]

    # Étape 1 : trouver l'index de début des références
    start_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if any(k in lines[i].lower().replace(" ", "") for k in ref_start_keywords):
            start_index = i + 1
            break
    if start_index == -1:
        return "(Références non trouvées)"

    # Étape 2 : nettoyer les lignes
    ref_lines = []
    for line in lines[start_index:]:
        line = line.strip()
        if not line or re.fullmatch(r"\d+", line):  # ignore lignes vides et numéros de page seuls
            continue
        if any(noise in line.lower() for noise in noise_keywords):
            continue
        ref_lines.append(line)

    # Étape 3 : détection du format
    full_text = " ".join(ref_lines)
    is_numbered = bool(re.search(r"(\[\d+\])|(^|\s)\d+\.", full_text))

    references = []
    if is_numbered:
        # Format numéroté [1] ...
        current_ref = ""
        for line in ref_lines:
            if re.match(r"(\[\d+\])|^\d+\.", line):
                if current_ref:
                    references.append(current_ref.strip())
                current_ref = line
            else:
                current_ref += " " + line
        if current_ref:
            references.append(current_ref.strip())
        # Tri par ordre de numérotation
        references.sort(key=lambda r: int(re.match(r"\[(\d+)\]", r).group(1)) if re.match(r"\[(\d+)\]", r) else 9999)
    else:
        # Format non numéroté
        buffer = ""
        for line in ref_lines:
            if re.search(r"\.\s*\d{4}\.", line) or re.match(r"^[A-Z][a-z]+,\s*[A-Z]\.", line):
                if buffer:
                    references.append(buffer.strip())
                buffer = line
            else:
                buffer += " " + line
        if buffer:
            references.append(buffer.strip())

    return "\n\n".join(references) if references else "(Références non trouvées)"


if __name__ == "__main__":
    with open("compression.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    title = extract_title(lines)
    authors = extract_authors(lines)
    abstract = extract_abstract(lines)
    bibliography = extract_references(lines)

    print("\n Titre extrait :\n", title)
    print("\n Auteurs extraits :\n", authors)
    print("\nRésumé extrait :\n", abstract)
    print("\nRéférences extraites :\n", bibliography)
