"""Find real local assets without loading the entire visual archive into a prompt."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[1]
LIBRARY=ROOT/'assets/library'
ALIASES={
 'thinking':['thinking','think','thought','head','mind','reason','思考','思想','思维'],
 'hand':['hand','手','书写'], 'bird':['bird','flock','鸟','飞鸟'],
 'paper':['paper','document','book','envelope','纸','文档','书'],
 'node':['node','network','connection','节点','连接','网络'],
 'growth':['flower','seedling','grow','plant','生长','萌芽','植物'],
 'collaboration':['two_hands','puzzle','协作','合作','拼合'],
 'human':['human','head','person','人','人物'],
}
EXTRA={
 'PAGE-049':['bird','鸟'], 'PAGE-061':['bird','鸟','thinking','思考'],
 'PAGE-082':['bird','鸟','paper','纸'], 'PAGE-045':['human','thinking','人','思考'],
 'PAGE-048':['thinking','思考'], 'ORIG-012':['human','thinking','人','思考'],
 'PAGE-034':['paper','纸'],
}

def records():
 rows=[]
 for base in [ROOT/'assets',ROOT/'assets/local']:
  manifest=base/'library/catalog.json'
  if manifest.is_file():
   for a in json.loads(manifest.read_text(encoding='utf-8')):
    a['_base']=str(base);rows.append(a)
 return rows
def public(a):
 svg=a.get('reconstruction') or a.get('editable_native')
 prepared=Path(a['_base'])/'prepared'/(a['id']+'.svg')
 def absolute(rel):
  if not rel:return None
  path=Path(a['_base'])/'library'/rel
  if not path.is_file():raise FileNotFoundError(path)
  return str(path)
 return {'id':a['id'],'name':a['name'],'category':a['category'],'status':a.get('lite_status'),'valid_artwork':a.get('source_artwork_valid') is not False,'original':absolute(a['local_path']),'preview':absolute(a.get('source_preview')),'editable_svg':absolute(svg),'prepared_svg':str(prepared) if prepared.is_file() else None,'source_url':a.get('url'),'source_page':a.get('source_page'),'sha256':a.get('sha256'),'historical_version_verified':a.get('historical_version_verified',False),'license':a.get('license')}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--query',default='');p.add_argument('--theme',choices=ALIASES);p.add_argument('--id');p.add_argument('--editable',action='store_true');p.add_argument('--limit',type=int,default=8)
 args=p.parse_args();tokens=[]
 if args.theme:tokens+=ALIASES[args.theme]
 if args.query:
  q=args.query.casefold();tokens.append(q)
  for values in ALIASES.values():
   if q in values:tokens+=values
 rows=[]
 for a in records():
  if args.id and a['id']!=args.id:continue
  if not args.id and a.get('source_artwork_valid') is False:continue
  if args.editable and not (a.get('reconstruction') or a.get('editable_native')):continue
  text=' '.join([a['id'],a['name'],a['category'],*EXTRA.get(a['id'],[])]).casefold()
  if tokens and not any(t.casefold() in text for t in tokens):continue
  rows.append(a)
 rows.sort(key=lambda a:(not (Path(a['_base'])/'prepared'/(a['id']+'.svg')).is_file(),not bool(a.get('editable_native')),a['id']))
 print(json.dumps({'matches':len(rows),'results':[public(a) for a in rows[:max(1,args.limit)]]},ensure_ascii=False,indent=2))
 if args.id and not rows:raise SystemExit(2)
if __name__=='__main__':main()
