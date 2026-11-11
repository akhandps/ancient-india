"""Build a timeline from the existing research dates; no new historical dates."""
import json
from pathlib import Path

root=Path(__file__).resolve().parent
out=root/'research'/'agastya'
graph=json.loads((out/'graph.json').read_text())
sources={s['id']:s for s in graph['sources']}
times={t['id']:t for t in graph['chronology']}
def astronomical(year):
    return year+1 if year<0 else year
rows=[]
def row(key,label,kind='text'):
    t=times[key];s=sources[t['source']]
    rows.append(dict(id=key,label=label,kind=kind,range=t['range'],start=astronomical(t['start']),end=astronomical(t['end']),note=t['note'],source=s['title'],url=s['url'],status=t['kind'].replace('_',' ')))
s=sources['rvdate']
rows.append(dict(id='person-hypothesis',label='Historical Agastya · conditional activity',kind='hypothesis',range='Somewhere within c. 1500–1000 BCE',start=-1499,end=-999,
    note='Working scenario: a real individual stands behind the Agastya-attributed Vedic hymns, and those attributions reflect his activity. The broad Ṛgvedic composition horizon supplies a provisional activity window only under those additional assumptions. This is neither a 500-year lifespan nor an independently established birth/death range; a historical core could also predate the surviving formulations.',
    source=s['title']+' · corpus date; historical-person placement is our conditional inference',url=s['url'],status='Conditional inference; no dated lifespan'))
row('T01','Ṛgveda · composition horizon')
row('T08','Mahābhārata · formative period')
row('T05','Rāmāyaṇa · formative period')
row('T10','Bhāgavata · older alternative (Ray, 1935)','alternative')
row('T09','Bhāgavata · Holdrege’s dating')
row('T11','Nacciṉārkkiṉiyar · commentary witness')
short_ranges={
 'person-hypothesis':'c. 1500–1000 BCE · possible activity',
 'T01':'c. 1500–1000 BCE',
 'T08':'c. 400 BCE–400 CE',
 'T05':'c. 200 BCE–200 CE',
 'T10':'550–650 CE · older alternative',
 'T09':'9th–early 10th century CE',
 'T11':'14th century CE',
}
for r in rows:r['chartRange']=short_ranges[r['id']]
data=dict(as_of=graph['as_of'],rows=rows,assumption='A historical core behind Vedic Agastya attributions; later texts are witnesses to the tradition, not additions to one lifespan.')
(out/'timeline-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
template=(root/'agastya-timeline.template.html').read_text()
html=template.replace('__TIMELINE_DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
target=Path('/Users/akhand/.codex/visualizations/2026/10/27/01a17c4a-9f77-7af2-bb95-eea7843a9c7f/agastya-timeline.html')
target.write_text(html)
(out/'timeline-fragment.html').write_text(html)
print(target)
