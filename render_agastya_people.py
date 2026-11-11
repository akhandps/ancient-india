"""Generate a source-linked dossier for every person-like graph node."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'research' / 'agastya'
graph = json.loads((ROOT / 'graph.json').read_text())
nodes = {n['id']: n for n in graph['nodes']}
sources = {s['id']: s for s in graph['sources']}
facet_ids = {n['id'] for n in graph['nodes'] if n['type'] == 'agastya_facet'}
person_types = {'person', 'deity', 'deity_collective', 'celestial', 'asura', 'commentator', 'poet', 'bodhisattva', 'people_collective', 'person_collective', 'person_or_entity', 'person_or_king', 'person_or_prince'}
notes = {}
logs = []
for name in ('vedic', 'epic', 'tamil', 'reception', 'vedic_three_hops', 'epic_three_hops', 'tamil_puranic_three_hops', 'epic_scale', 'puranic_scale', 'vedic_tamil_scale', 'tamil_scale_review', 'genealogy_scale', 'genealogy_scale_more', 'genealogy_scale_kuru', 'genealogy_vedic_solar', 'genealogy_scale_kaurava', 'genealogy_anu', 'genealogy_ayus', 'rama_descendants', 'tamil_further', 'tamil_later', 'genealogy_future_kuru', 'tamil_final', 'genealogy_future_dynasties', 'genealogy_solar_middle', 'genealogy_yadu_middle', 'mb_sabha_people', 'mb_adi_genealogies', 'mb_sabha_earlier', 'mb_adi_incarnations', 'mb_adi_royal_lineages', 'mb_sabha_first', 'mb_adi_next', 'mb_other_roster', 'mb_war_roster', 'mb_adi_pandava_early', 'ramayana_war_roster', 'mb_battle_new_people', 'mb_vana_roster', 'bhagavata_lineages_more', 'mb_adi_later', 'bhagavata_9_24_new', 'bhagavata_canto8_people', 'mb_adi_later_more', 'bhagavata_canto4_people'):
    batch = json.loads((ROOT / 'expansion' / (name + '.json')).read_text())
    logs.append({'batch': name, 'search_log': batch.get('search_log', [])})
    for item in batch.get('person_notes', []):
        notes.setdefault(item['person_id'], []).append(item)

def sortkey(n):
    return n['label'].casefold()

people = []
for n in sorted((n for n in graph['nodes'] if n['type'] in person_types), key=sortkey):
    direct, context = [], []
    for c in graph['claims']:
        if n['id'] not in (c['subject'], c['object']):
            continue
        item = {
            'claim_id': c['id'], 'facet': c['facet'], 'subject': c['subject'],
            'predicate': c['predicate'], 'object': c['object'],
            'source': c['source'], 'locator': c['locator'],
            'summary': c['summary'], 'status': c['status'], 'note': c.get('note', ''),
            'speaker': c.get('speaker'),
        }
        if c['subject'] in facet_ids or c['object'] in facet_ids:
            direct.append(item)
        else:
            context.append(item)
    findings, questions = [], []
    for item in notes.get(n['id'], []):
        findings += item.get('findings', [])
        questions += item.get('open_questions', [])
    people.append({
        'id': n['id'], 'label': n['label'], 'type': n['type'],
        'direct_claims': direct, 'context_claims': context,
        'research_notes': list(dict.fromkeys(findings)),
        'open_questions': list(dict.fromkeys(questions)),
    })

(ROOT / 'people.json').write_text(json.dumps({'as_of': graph['as_of'], 'scope': 'Every person-like node in graph.json. Direct means a claim endpoint is a source-local Agastya facet; context is a link between other figures.', 'people': people, 'search_log': logs}, ensure_ascii=False, indent=2) + '\n')

lines = ['# People around Agastya', '', f'{len(people)} person-like nodes in {len(graph["claims"])} passage claims. A direct claim names a source-local Agastya facet as an endpoint. Context claims connect other figures in the same source tradition. Neither kind proves a historical meeting.', '', 'Claim status is a review level: `translation_checked` concerns a translated text, `source_text_checked` concerns the Sanskrit text, `editorial_attribution` marks assigned speakers or authors, `scholarly_report` is second-hand, and `identity_hypothesis` is a proposed identification.', '', '## Index', '']
for p in people:
    lines.append(f'- [{p["label"]}](#{p["id"]}) — {len(p["direct_claims"])} direct, {len(p["context_claims"])} contextual')

for p in people:
    lines += ['', f'<a id="{p["id"]}"></a>', f'## {p["label"]}', '', f'Type: {p["type"]}. Direct links: {len(p["direct_claims"])}. Context links: {len(p["context_claims"])}.', '']
    for title, key in [('Direct Agastya links', 'direct_claims'), ('Context in the same passages', 'context_claims')]:
        if not p[key]:
            continue
        lines += [f'### {title}', '']
        for c in p[key]:
            source = sources[c['source']]
            triple = f'{nodes[c["subject"]]["label"]} → {c["predicate"].replace("_", " ")} → {nodes[c["object"]]["label"]}'
            lines.append(f'- **{c["claim_id"]}** {triple}. [{source["title"]}, {c["locator"]}]({source["url"]}). {c["status"]}. {c["summary"]}' + (f' {c["note"]}' if c['note'] else ''))
        lines.append('')
    if p['research_notes']:
        lines += ['### Review notes', ''] + [f'- {v}' for v in p['research_notes']] + ['']
    if p['open_questions']:
        lines += ['### Questions', ''] + [f'- {v}' for v in p['open_questions']] + ['']

lines += ['## Search log', '', 'A search log records checked leads. It is not a claim of exhaustive coverage.', '']
for batch in logs:
    lines.append(f'### {batch["batch"].title()}')
    lines.append('')
    for item in batch['search_log']:
        subject = item.get('query', item.get('scope', item.get('source', 'Source review')))
        result = item.get('outcome', item.get('result', item.get('method', 'No result recorded.')))
        lines.append(f'- **{subject}**: {result}')
    lines.append('')
(ROOT / 'people.md').write_text('\n'.join(lines))
print(f'{len(people)} people dossiers')
