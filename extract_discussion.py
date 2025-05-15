import extraction_v4
import re
from collections import defaultdict

def extract_section(lines, start_keywords, stop_keywords):
    in_section = False
    content = []

    for line in lines:
        raw = line.strip()

        if not in_section and any(re.fullmatch(pat, raw, re.IGNORECASE) for pat in start_keywords):
            in_section = True
            continue

        if in_section:
            if any(re.fullmatch(pat, raw, re.IGNORECASE) for pat in stop_keywords):
                break
            if re.fullmatch(r"\d+", raw):
                continue
            content.append(raw)

    return "\n".join(content).strip()

def extract_discussion(lines):

    discussion_start = [
        r"^DISCUSSION$", r"^Discussion$", r"^13\.?\s*Discussion$", r"^V\.?\s*Discussion$",
        r"^4\s*Discussion and Future Work$", r"^Discussion and Future Work$",
    ]

    discussion_stop = [
        r"^ACKNOWLEDGMENTS?$", r"^Acknowledgements?$", r"^Acknowledgment$", r"^REFERENCES$", r"^References$",r"^Appendix A: SBD Rule Set$"
    ]

    return extract_section(lines, discussion_start, discussion_stop) or "(Discussion non trouvée)"

if __name__ == "__main__":
    with open("mikheev.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    discussion = extract_discussion(lines)
    print("\n----- DISCUSSION -----\n", discussion)
