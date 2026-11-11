"""Reviewed Viṣṇu Purāṇa 4.4 Rāma-descendant batch from Taylor's translation."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'research' / 'agastya' / 'expansion' / 'rama_descendants.json'
source = {
    'id': 'vp4_4_anu',
    'title': 'Viṣṇu Purāṇa, Book 4, chapter 4: Rāma and his descendants',
    'url': 'https://press-files.anu.edu.au/downloads/press/n8264/html/book04.xhtml?page=9&referer=',
    'kind': 'primary_text_translation',
    'edition': 'McComas Taylor, trans., The Viṣṇu Purāṇa (ANU Press, 2021), Book 4, chapter 4',
    'locator': '4.4.49, 4.4.58–60',
    'accessed': '2026-10-27',
}
new = {
    'vp4_bharata_rama': 'Bharata · Rāma’s brother · Viṣṇu Purāṇa witness',
    'vp4_satrughna': 'Śatrughna · Rāma’s brother · Viṣṇu Purāṇa witness',
    'vp4_kusha': 'Kuśa · Rāma’s son · Viṣṇu Purāṇa witness',
    'vp4_lava': 'Lava · Rāma’s son · Viṣṇu Purāṇa witness',
    'vp4_angada_lakshmana': 'Aṅgada · Lakṣmaṇa’s son · Viṣṇu Purāṇa witness',
    'vp4_candraketu': 'Candraketu · Lakṣmaṇa’s son · Viṣṇu Purāṇa witness',
    'vp4_taksha': 'Takṣa · Bharata’s son · Viṣṇu Purāṇa witness',
    'vp4_pushkara': 'Puṣkara · Bharata’s son · Viṣṇu Purāṇa witness',
    'vp4_subahu_satrughna': 'Subāhu · Śatrughna’s son · Viṣṇu Purāṇa witness',
    'vp4_surasena_satrughna': 'Śūrasena · Śatrughna’s son · Viṣṇu Purāṇa witness',
}
chain = [
    ('vp4_kusha', 'Kuśa'), ('vp4_atithi', 'Atithi'), ('vp4_nishadha', 'Niṣadha'),
    ('vp4_nala', 'Nala'), ('vp4_nabhas', 'Nabhas'), ('vp4_pundarika', 'Puṇḍarīka'),
    ('vp4_kshemadhanvan', 'Kṣemadhanvan'), ('vp4_devanika', 'Devānīka'),
    ('vp4_ahinagu', 'Ahīnagu'), ('vp4_ruru', 'Ruru'), ('vp4_pariyatra', 'Pāriyātra'),
    ('vp4_dala', 'Dala'), ('vp4_chala', 'Chala'), ('vp4_uktha', 'Uktha'),
    ('vp4_vajranabha', 'Vajranābha'), ('vp4_sankhanabha', 'Śaṅkhanābha'),
    ('vp4_vyutthitasva', 'Vyutthitāśva'), ('vp4_visvasaha', 'Viśvasaha'),
    ('vp4_hiranyanabha', 'Hiraṇyanābha'), ('vp4_pushya', 'Puṣya'),
    ('vp4_dhruvasamdhi', 'Dhruvasaṃdhi'), ('vp4_sudarsana', 'Sudarśana'),
    ('vp4_agnivarna', 'Agnivarṇa'), ('vp4_sighraga', 'Śīghraga'),
    ('vp4_maru', 'Maru'), ('vp4_prasusruta', 'Prasuśruta'),
    ('vp4_susandhi', 'Susandhi'), ('vp4_amarsa', 'Amarṣa'),
    ('vp4_mahasvant', 'Mahasvant'), ('vp4_visrutavant', 'Viśrutavant'),
    ('vp4_brihadbala', 'Bṛhadbala'),
]
for person_id, name in chain[1:]:
    new[person_id] = f'{name} · Rāma-line witness in Viṣṇu Purāṇa 4.4'

relationships = [
    ('dasaratha', 'vp4_bharata_rama', '4.4.49'),
    ('dasaratha', 'vp4_satrughna', '4.4.49'),
    ('rama', 'vp4_kusha', '4.4.58'), ('rama', 'vp4_lava', '4.4.58'),
    ('lakshmana', 'vp4_angada_lakshmana', '4.4.58'),
    ('lakshmana', 'vp4_candraketu', '4.4.58'),
    ('vp4_bharata_rama', 'vp4_taksha', '4.4.58'),
    ('vp4_bharata_rama', 'vp4_pushkara', '4.4.58'),
    ('vp4_satrughna', 'vp4_subahu_satrughna', '4.4.58'),
    ('vp4_satrughna', 'vp4_surasena_satrughna', '4.4.58'),
]
for i in range(len(chain) - 1):
    # Taylor's section marks the long succession as 4.4.58, then continues
    # with 4.4.59–60 after Hiraṇyanābha.
    locator = '4.4.58' if i < 17 else '4.4.58–60'
    relationships.append((chain[i][0], chain[i + 1][0], locator))

nodes = [{'id': pid, 'label': label, 'type': 'person'} for pid, label in new.items()]
claims = []
for index, (parent, child, locator) in enumerate(relationships, 1):
    child_label = new[child].split(' · ')[0]
    claims.append({
        'id': f'VRD{index:03d}', 'facet': 'ramayana', 'subject': parent,
        'predicate': 'father_of', 'object': child, 'source': source['id'],
        'locator': locator,
        'summary': f'Taylor’s translation lists {child_label} as a son or successor in this named Rāma-line genealogy.',
        'category': 'relationship', 'status': 'translation_checked',
        'speaker': 'Parāśara',
        'note': 'This is a literary genealogy in the Viṣṇu Purāṇa. The book and verse identify an attestation, not an independently dated lifespan.',
        'original_language_reviewed': False,
    })

batch = {'nodes': nodes, 'sources': [source], 'claims': claims,
         'search_log': [{'query': 'ANU Viṣṇu Purāṇa 4.4.49 and 4.4.58–60',
                         'outcome': 'Checked Taylor’s Rāma and descendant list; retained named sons and successive links.'}],
         'notes': ['Bharata here is Rāma’s brother, separate from the Puru-line Bharata. Similar descendant names are source-local.']}
OUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n')
print(f'{len(nodes)} nodes, {len(claims)} claims: {OUT}')
