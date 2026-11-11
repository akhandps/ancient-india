"""Make a review queue from Sörensen's Mahābhārata name index.

An index headword is a candidate, never a verified individual or relationship.
The classifier is intentionally conservative and its decisions are auditable.
"""
import csv
import json
import re
from bisect import bisect_right
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'research' / 'agastya' / 'expansion'
SOURCE = ROOT / 'inm.txt'
if not SOURCE.exists():
    raise FileNotFoundError(f'Download the upstream INM transcription to {SOURCE}; see {ROOT / "INM-SOURCE.md"}')
text = SOURCE.read_text()
opening = re.compile(r'^<L>(\d+)<pc>([^<]+)<k1>([^<]+)<k2>([^\n]+)$', re.M)
matches = list(opening.finditer(text))
newline_offsets = [m.start() for m in re.finditer('\n', text)]
person = re.compile(r'\b(?:son|daughter|wife|husband|father|mother|brother|sister|king|queen|prince|princess|rṣi|ṛṣi|sage|minister|warrior|chieftain|asura|demon|gandharva|nāga|serpent|apsaras|brahman|brahmin|disciple|pupil)\b', re.I)
nonperson = re.compile(r'\b(?:river|lake|mountain|forest|town|city|village|country|island|star|asterism|constellation|month|day|hour|weapon|arrow|sword|parva|chapter|section|festival|sacrifice|rite|tree|plant|herb|horse|elephant|bird|colour|color|meter|metre|hymn|mantra|hell|heaven|palace|dwelling|path|road|garment|ornament)\b', re.I)
collective = re.compile(r'\b(?:plural|pl\.|class of|race of|tribe|people|clan|group of|troop|host of|sons of|daughters of|wives of|warriors|ascetics|gods|demons|serpents|kings|sages|rṣis|ṛṣis)\b', re.I)

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\{[@%#]|[@%#]\}', '', s)
    s = re.sub(r'\[Page[^]]+\]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

rows = []
for i, match in enumerate(matches):
    end = text.find('<LEND>', match.end())
    if end < 0 or (i + 1 < len(matches) and end > matches[i + 1].start()):
        continue
    body = text[match.end():end]
    plain = clean(body)
    display_match = re.search(r'\{@([^@]+)@\}', body)
    display = clean(display_match.group(1)) if display_match else match.group(3)
    lead = plain.split('§', 1)[0][:300]
    alias = bool(re.search(r'\s=\s|\bidentical with\b|\bepithet of\b|\banother name of\b', lead, re.I))
    is_collective = bool(collective.search(lead))
    is_nonperson = bool(nonperson.search(lead))
    signal = person.search(lead)
    if alias:
        category = 'alias_or_equivalence'
    elif is_collective:
        category = 'collective_or_class'
    elif is_nonperson:
        category = 'nonperson_or_mixed'
    elif signal:
        category = 'likely_individual_candidate'
    else:
        category = 'unclassified_name'
    line = bisect_right(newline_offsets, match.start()) + 1
    rows.append({
        'record_id': match.group(1), 'page_column': match.group(2),
        'headword_slp1': match.group(3), 'headword_display': display,
        'classification': category, 'person_signal': signal.group(0) if signal else '',
        'lead_definition': lead[:240], 'entry_excerpt': plain[:500],
        'source_line': line,
        'source_url': f'https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/inm/inm.txt#L{line}',
    })

with (ROOT / 'inm-candidates.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)

summary = {
    'source_title': 'Sörensen, Index to the Names in the Mahābhārata (CDSL digitization)',
    'source_url': 'https://sanskrit-lexicon.github.io/INM/',
    'source_file_url': 'https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/inm/inm.txt',
    'license': 'CC BY-SA 4.0 per CDSL INM project page; preserve attribution and check repository exceptions before redistribution',
    'method': 'Index-headword candidates only. Pattern classification on the leading definition; no primary passage or entity identity verification. Same headword can represent multiple people or an alias.',
    'entries_parsed': len(rows),
    'unique_headword_spellings': len({r['headword_slp1'] for r in rows}),
    'classification_counts': dict(Counter(r['classification'] for r in rows)),
    'goal': 3000,
    'counted_as_verified_individuals': 0,
}
(ROOT / 'inm-candidates-summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary['classification_counts'], ensure_ascii=False))
