"""Create a portable starter from actual curated SVGs and user-supplied fonts."""
from pathlib import Path
import argparse,json,shutil,hashlib
from catalog import records

ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--out',required=True);p.add_argument('--title',default='Make room\nfor wonder.');p.add_argument('--subtitle',default='给好奇心，留一点空间。');p.add_argument('--asset',default='STUDIO-thinking');p.add_argument('--motion',choices=['none','gentle','expressive'],default='gentle')
 args=p.parse_args();out=Path(args.out).resolve()
 if out.exists():p.error('Output already exists; choose a new directory. Existing projects must be edited in place.')
 curated=[]
 for base in [ROOT/'assets',ROOT/'assets/local']:
  manifest=base/'prepared/catalog.json'
  if manifest.is_file():
   for a in json.loads(manifest.read_text(encoding='utf-8')):
    a['_base']=str(base);curated.append(a)
 selected=next((a for a in curated if a['id']==args.asset),None)
 if selected is None:p.error('--asset must be an available prepared ID. Use catalog.py to discover; use other archive assets manually after inspection.')
 ids=list(dict.fromkeys([args.asset,'STUDIO-thinking','STUDIO-connection','STUDIO-growth','STUDIO-thought','STUDIO-reading','STUDIO-dialogue']))
 archive=records()
 out.mkdir(parents=True);(out/'sources').mkdir();(out/'fonts').mkdir()
 for name in ['index.html','styles.css','app.js']:shutil.copy2(ROOT/'assets/starter'/name,out/name)
 font_dir=ROOT/'assets/local/fonts'
 families={'AnthropicSerif':'AnthropicSerifWebText.ttf','AnthropicSans':'AnthropicSansWebText.ttf','AnthropicMono':'AnthropicMonoVariable.ttf'}
 bundled=all((font_dir/name).is_file() for name in families.values())
 css=[]
 if bundled:
  for family,name in families.items():
   shutil.copy2(font_dir/name,out/'fonts'/name)
   css.append("@font-face{font-family:"+family+";src:url('fonts/"+name+"') format('truetype');font-weight:400;font-display:swap}")
  if (font_dir/'manifest.json').is_file():shutil.copy2(font_dir/'manifest.json',out/'fonts/manifest.json')
 (out/'fonts.css').write_text('\n'.join(css) or '/* Uses installed system fonts. */',encoding='utf-8')
 display=[];provenance=[]
 for aid in ids:
  a=next(x for x in curated if x['id']==aid);record=next(x for x in archive if x['id']==aid)
  original=Path(record['_base'])/'library'/record['local_path'];data=original.read_bytes()
  assert hashlib.sha256(data).hexdigest()==record['sha256'],aid
  name=aid+original.suffix;shutil.copy2(original,out/'sources'/name)
  svg=(Path(a['_base'])/'prepared'/(aid+'.svg')).read_text(encoding='utf-8')
  display.append({'id':aid,'label':a['label'],'idea':a['idea'],'svg':svg,'kind':a['kind'],'original':'sources/'+name,'source_url':a['source_url'],'source_page':a['source_page']})
  provenance.append({'id':aid,'prepared_derivative':True,'original':'sources/'+name,'original_sha256':record['sha256'],'source_url':record['url'],'source_page':record.get('source_page'),'license':record.get('license'),'historical_version_verified':record.get('historical_version_verified',False),'processing':a['kind']})
 payload={'title':args.title,'subtitle':args.subtitle,'motion':args.motion,'hasBundledFonts':bundled,'artworks':display}
 (out/'content.js').write_text('window.VISUAL_STUDIO='+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+';\n',encoding='utf-8')
 (out/'sources.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
 (out/'README.md').write_text('# 可离线运行的视觉起步页\n\n双击 index.html。无需安装字体或依赖。\n\n修改 content.js 的内容和 styles.css 的布局；业务交互位于 app.js。此页是独立风格演绎与功能起点，不是 Anthropic 官方网页。sources/ 内是真实原图，sources.json 记录处理方式及出处。默认提供的配色/插画切换、动效开关和 SVG 导出均在浏览器本地执行。\n\n公开版默认使用系统字体和 MIT 原创示例；如导入本地素材或字体，其授权独立于技能代码。\n',encoding='utf-8')
 print(json.dumps({'output':str(out),'entry':str(out/'index.html'),'selected_assets':ids,'motion':args.motion},ensure_ascii=False))
if __name__=='__main__':main()
