import re
from collections import defaultdict

def clean_author_line(line):
    line = re.sub(r"(\w)\d+\b", r"\1", line)
    return re.sub(r"\s{2,}", " ", line).strip()

def is_email_line(line):
    return '@' in line

def is_affiliation_line(line):
    keywords = [
        "university", "université", "école", "polytechnique","institute", "school", "college", "center", "google", "mountain", "ca", "speech", "technology", "international", "sri","meinajaries","college","park","science", 
        "faculty", "department","laboratoire","laboratory", "city", "france", "canada", "spain", "mexico", "belgium", "leuven", "theresiastraat", "Universiteit", "Linguistics", "street", "chemin", "broken", "land","suite"
    ]
    return any(k in line.lower() for k in keywords)

def extract_authors(lines, title=None):
    author_groups = defaultdict(list)
    affils_by_author = defaultdict(str)

    # Cas 1 : auteurs + index
    author_line = next((l for l in lines[:50] if re.search(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\d\b", l)), "")
    matches = re.findall(r"([A-Z][a-zA-Z.\-]+(?:\s+[A-Z][a-zA-Z.\-]+)*)(\d)", author_line)
    for name, idx in matches:
        author_groups[idx].append(clean_author_line(name))

    if author_groups:
        current_idx = None
        affil_blocks = defaultdict(list)
        for line in lines[:50]:
            line = line.strip()
            if re.match(r"^(abstract|résumé|introduction|keywords)", line.lower()):
                break
            if re.fullmatch(r"\d+", line):
                current_idx = line
                continue
            if is_email_line(line) or not line or current_idx is None:
                continue
            affil_blocks[current_idx].append(line)

        formatted = []
        for idx in sorted(author_groups):
            names = ", ".join(author_groups[idx])
            address = "\n".join(affil_blocks.get(idx, []))
            formatted.append(f"- {names}\n{address}" if address else f"- {names}")
        return "\n\n".join(formatted)

    # Cas 2 : ligne condensée
    for i, line in enumerate(lines[:15]):
        if re.search(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,.* and ", line):
            raw = re.split(r",| and ", line.strip())
            authors = [clean_author_line(a) for a in raw if a.strip()]
            break
    else:
        authors = []

    for line in lines:
        for author in authors:
            if author.split()[-1].lower() in line.lower() and is_affiliation_line(line):
                affils_by_author[author] += " " + line.strip()

    if authors:
        result = []
        for name in authors:
            affil = affils_by_author.get(name, "").strip()
            result.append(f"- {name}" + (f"\n{affil}" if affil else ""))
        return "\n\n".join(result)

    # Cas 3 : lignes auteurs consécutives + bloc affil
    possible_authors = []
    for i, line in enumerate(lines[:20]):
        if title and title.strip().lower() == line.strip().lower():
            continue
        if any(x in line for x in [",", " and "]) and not is_email_line(line) and not is_affiliation_line(line):
            possible_authors.append(line.strip())
        elif possible_authors:
            addr_block = []
            for l in lines[i:]:
                if is_affiliation_line(l):
                    addr_block.append(l.strip())
                elif addr_block:
                    break
            cleaned_block = [re.sub(r"\S+@\S+", "", l).strip() for l in addr_block if not is_email_line(l)]
            full_affil = " ".join(cleaned_block).strip()
            full_names = []
            for line in possible_authors:
                raw = re.split(r",| and ", line)
                full_names.extend([clean_author_line(a) for a in raw if a.strip()])
            return "\n\n".join(f"- {n}\n{full_affil}" for n in full_names)

    # Cas 4 : triplet nom-affil-mail
    authors = []
    for i in range(len(lines) - 2):
        name_line = lines[i].strip()
        if title and title.strip().lower() == name_line.lower():
            continue
        affil_line = lines[i+1].strip()
        email_line = lines[i+2].strip()
        if not name_line or not affil_line or not email_line:
            continue
        if is_email_line(email_line) and is_affiliation_line(affil_line):
            if not is_email_line(name_line) and not is_affiliation_line(name_line):
                name = clean_author_line(name_line)
                authors.append((name, affil_line))
        if "abstract" in name_line.lower():
            break

    if authors:
        return "\n\n".join(f"- {a}\n{b}" for a, b in authors)
    
    authors = []
    email_blocks = []
    affil_map = {
        "umd.edu": "University of Maryland",
        "umiacs.umd.edu": "University of Maryland",
        "bbn.com": "BBN Technologies"
    }

    # Étape 1 : Extraire tous les e-mails
    for line in lines:
        matches = re.findall(r"\b([a-z0-9._%+-]+)@([\w\.-]+)", line, re.I)
        for local, domain in matches:
            email_blocks.append((local.strip(), domain.strip()))

    # Étape 2 : Déduire les auteurs à partir des blocs en haut du document
    for i in range(10):
        parts = re.split(r",| and ", lines[i])
        for part in parts:
            name = clean_author_line(part)
            if re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)+$", name):
                authors.append(name)

    # Étape 3 : Faire correspondre nom → domaine → affiliation
    affil_by_author = defaultdict(str)
    for name in authors:
        name_compact = name.lower().replace(" ", "")
        for local, domain in email_blocks:
            if local in name_compact:
                affil_by_author[name] = affil_map.get(domain.lower(), "")

    # Fallback affiliation
    fallback_affil = next((l.strip() for l in lines if is_affiliation_line(l) and not is_email_line(l)), "")

    results = []
    for name in authors:
        affil = affil_by_author.get(name, fallback_affil)
        results.append(f"- {name}\n{affil}" if affil else f"- {name}")
    return "\n\n".join(results)
    return "(Auteurs non trouvés)"


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
                content = re.sub(r"^(abstract|résumé)\s*[-:—]*\s*", "", line, flags=re.IGNORECASE)
                if content:
                    abstract_lines.append(content.strip())
        else:
            if re.match(r"^(index\s+terms|keywords|introduction|\d+)", line_lower):
                break
            abstract_lines.append(line_clean)

    return " ".join(abstract_lines).strip() if abstract_lines else "(Résumé non trouvé)"


def remove_footers(lines):
    footer_patterns = [
        r"Manuscript received.*",
        r"please cite as.*",
        r"licensed under the creative commons",
        r"some rights reserved",
        r"http[s]?://.*",
        r"\(.*?@.*?\)",  # email
        r"©.*", r"copyright",
        r"document understanding conference",
        r"université.*avignon", r"pompeu fabra", r"polytechnique", r"unam", r"vm labs",
        r"polibits", r"prepared .* version"
    ]
    compiled = [re.compile(pat, re.IGNORECASE) for pat in footer_patterns]

    cleaned = []
    for line in lines:
        if any(p.search(line.strip()) for p in compiled):
            continue
        cleaned.append(line)
    return cleaned

def normalize_line(text: str) -> str:
    """Normalize headings with spaced letters like 'C O N C L U S I O N' or 'C ONCLUS ION'."""
    text = text.strip()
    if len(text) < 4:
        return text
    if re.search(r'(?:[A-Z]\s+){2,}[A-Z]', text):  # pattern: multiple spaced capitals
        return re.sub(r'\s+(?=[A-Z])', '', text)
    return text

def extract_section(lines, start_keywords, stop_keywords):
    in_section = False
    content = []

    for line in lines:
        raw = line.strip()
        norm = normalize_line(raw)

        if not in_section and any(re.fullmatch(pat, norm, re.IGNORECASE) for pat in start_keywords):
            in_section = True
            continue

        if in_section:
            if any(re.fullmatch(pat, norm, re.IGNORECASE) for pat in stop_keywords):
                break
            if re.fullmatch(r"\d+", norm):  # skip standalone page numbers
                continue
            content.append(raw)

    return "\n".join(content).strip()



def extract_introduction(lines):
    lines = remove_footers(lines)

    intro_start = [
        r"^1\s*Introduction",r"^1\.\s*Introduction", r"^I\.\s*Introduction", r"^Introduction", r"^INTRODUCTION"
    ]
    intro_stop = [
        r"^2\.", r"^II\.", r"^2\s*^Related Work", r"^2\s*^Previous Work", r"^1\.\s*^Goals of the paper", r"^2\s*^Method", r"^Approach", r"^System Overview", r"^Previous Work",r"^2\s*From Full Sentence to Compressed",r"^RELATED WORK", r"^Method", r"^Experiments",r"^2\s*Model Architectures",r"^System Overview", r"^Support Vector Machine", r"^THE IMPORTANCE OF LINGUISTIC SEGMENTATION"
    ]
    return extract_section(lines, intro_start, intro_stop) or "(Introduction non trouvée)"


def extract_conclusion(lines):
    lines = remove_footers(lines)

    concl_start = [
        r"^6\.?\s*CONCLUSIONS?$", r"^7\.?\s*CONCLUSIONS?$", r"^VI\.?\s*CONCLUSIONS?$",
        r"^CONCLUSIONS?$", r"^CONCLUSION AND FUTURE WORK$", r"^CONCLUSIONS AND FUTURE WORK$", r"^4\s*Conclusion?$"
    ]

    concl_stop = [
        r"^References", r"^REFERENCES", r"^Bibliography", r"^Acknowledgments?", r"^APPENDIX", r"^Follow-Up Work", r"^5\s*Acknowledgements?$"
    ]
    return extract_section(lines, concl_start, concl_stop) or "(Conclusion non trouvée)"




def extract_references(lines):
    ref_start_keywords = ["references", "références", "bibliographie", "r eferences"]
    noise_keywords = [
        "p-value", "rouge", "table", "figure", "polibits", "acknowledgment",
        "author", "received", "abstract", "measure", "0.", "js", "sm", "index"
    ]

    start_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if any(k in lines[i].lower().replace(" ", "") for k in ref_start_keywords):
            start_index = i + 1
            break
    if start_index == -1:
        return "(Références non trouvées)"

    ref_lines = []
    for line in lines[start_index:]:
        line = line.strip()
        if not line or re.fullmatch(r"\d+", line):
            continue
        if any(noise in line.lower() for noise in noise_keywords):
            continue
        ref_lines.append(line)

    full_text = " ".join(ref_lines)
    is_numbered = bool(re.search(r"(\[\d+\])|(^|\s)\d+\.", full_text))

    references = []
    if is_numbered:
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
        references.sort(key=lambda r: int(re.match(r"\[(\d+)\]", r).group(1)) if re.match(r"\[(\d+)\]", r) else 9999)
    else:
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
    abstract = extract_abstract(lines)
    bibliography = extract_references(lines)

    print("\nTitre extrait :\n", title)
    print("\nAuteurs avec adresses :\n")
    print(extract_authors(lines, title=title))

 #   print("\nRésumé extrait :\n", abstract)
  
    intro = extract_introduction(lines)
    concl = extract_conclusion(lines)

  #  print("----- INTRODUCTION -----\n", intro)
   # print("\n----- CONCLUSION -----\n", concl)
    #print("\nRéférences extraites :\n", bibliography)
