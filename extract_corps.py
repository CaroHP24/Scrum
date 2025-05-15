import re

def is_section_title(line):
    # Détecte les titres de section : "2 Method", "3.1 Data", etc.
    return re.match(r'^\s*\d+(\.\d+)*\s+[A-Z]', line.strip())

def is_end_section(line):
    # Utilise la même méthode que pour détecter les titres numérotés
    if not is_section_title(line):
        return False
    clean = re.sub(r'^\s*\d+(\.\d+)*\s+', '', line.strip()).lower()
    return any(clean.startswith(k) for k in [
        'conclusion', 'acknowledgment', 'acknowledgments',
        'references', 'bibliography', 'discussion'
    ])
def remove_page_numbers(lines):
    cleaned_lines = []
    for line in lines:
        # On enlève les lignes qui ne contiennent qu’un nombre entier (typiquement un numéro de page)
        if re.fullmatch(r'\s*\d+\s*', line):
            continue
        cleaned_lines.append(line)
    return cleaned_lines

def extract_corps(lines):
    start_index = None
    end_index = None

    # Étape 1 : trouver la section "1 Introduction"
    intro_found = False
    for i, line in enumerate(lines):
        clean = line.strip().lower()
        if re.match(r'^\s*1(\.0+)?\s+introduction', clean):
            intro_found = True
            continue
        if intro_found and is_section_title(line):
            start_index = i
            break

    # Étape 2 : trouver la première section de fin (Conclusion, etc.)
    for i in range(start_index + 1 if start_index else 0, len(lines)):
        if is_end_section(lines[i]):
            end_index = i
            break

    # Étape 3 : extraction des lignes entre start et end
    if start_index is not None:
        end_index = end_index if end_index else len(lines)
        corps_lines = lines[start_index:end_index]
        #corps_lines = remove_footnote(corps_lines)
        corps_lines = remove_page_numbers(corps_lines)
        return "\n".join(corps_lines).strip()
    else:
        return "(Corps non trouvé)"