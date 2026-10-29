"""Import an extracted private skill's assets, keeping them outside Git."""
from pathlib import Path
import argparse,hashlib,json,shutil

ROOT=Path(__file__).resolve().parents[1]
def contained(base,relative):
 p=(base/relative).resolve()
 if not p.is_relative_to(base.resolve()) or not p.is_file():raise ValueError('Invalid or missing asset: '+str(relative))
 return p
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--from',dest='source',required=True)
 args=p.parse_args();source=Path(args.source).resolve()/'assets';target=ROOT/'assets/local'
 if target.exists():p.error('An import already exists; choose a clean checkout or review it manually. Nothing overwritten.')
 records=json.loads((source/'library/catalog.json').read_text(encoding='utf-8'))
 for a in records:
  f=contained(source/'library',a['local_path'])
  if hashlib.sha256(f.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('Source hash mismatch: '+a['id'])
  for key in ['reconstruction','editable_native','source_preview','trace_preview','native_preview']:
   if a.get(key):contained(source/'library',a[key])
 prepared=json.loads((source/'prepared/catalog.json').read_text(encoding='utf-8'))
 for a in prepared:contained(source/'prepared',a['id']+'.svg')
 fonts=source/'fonts/manifest.json'
 if fonts.exists():
  for a in json.loads(fonts.read_text(encoding='utf-8'))['fonts']:
   f=contained(source/'fonts',a['file'])
   if hashlib.sha256(f.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('Font hash mismatch: '+a['file'])
 # Reject directory symlinks before copying, including unreferenced files.
 for folder in ['library','prepared','fonts']:
  base=source/folder
  if base.is_symlink() or (base.exists() and any(x.is_symlink() for x in base.rglob('*'))):raise ValueError('Symlink assets require explicit manual review')
 target.mkdir(parents=True)
 for folder in ['library','prepared','fonts']:
  if (source/folder).is_dir():shutil.copytree(source/folder,target/folder)
 print(json.dumps({'imported_records':len(records),'prepared':len(prepared),'local_directory':str(target),'third_party_licenses_unchanged':True},ensure_ascii=False))
if __name__=='__main__':main()
