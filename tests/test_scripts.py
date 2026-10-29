"""Portable standard-library tests: python -m unittest discover -s tests -v."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,unittest,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
def run(script,*args):return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,encoding='utf-8')
class PublicSkillTests(unittest.TestCase):
 def test_source_hashes_and_editable_geometry(self):
  rows=json.loads((ROOT/'assets/library/catalog.json').read_text(encoding='utf-8'))
  self.assertEqual(len(rows),6)
  for a in rows:
   f=ROOT/'assets/library'/a['local_path'];self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),a['sha256'])
   svg=ET.parse(f).getroot();self.assertTrue(svg.findall('.//{http://www.w3.org/2000/svg}path'));self.assertFalse(svg.findall('.//{http://www.w3.org/2000/svg}image'))
 def test_semantic_search(self):
  p=run('catalog.py','--theme','thinking','--editable');self.assertEqual(p.returncode,0,p.stderr)
  self.assertIn('STUDIO-thought',[r['id'] for r in json.loads(p.stdout)['results']])
 def test_unknown_id_signals_missing(self):
  p=run('catalog.py','--id','DOES-NOT-EXIST');self.assertNotEqual(p.returncode,0)
 def test_scaffold_and_overwrite_protection(self):
  with tempfile.TemporaryDirectory() as temp:
   out=Path(temp)/'site';p=run('scaffold.py','--out',out,'--motion','none','--title','A </script> & B')
   self.assertEqual(p.returncode,0,p.stderr);self.assertTrue((out/'index.html').is_file())
   js=(out/'content.js').read_text(encoding='utf-8');data=json.loads(js.removeprefix('window.VISUAL_STUDIO=').strip().removesuffix(';'))
   self.assertEqual(data['title'],'A </script> & B');self.assertNotIn('</script>',js)
   self.assertEqual(data['motion'],'none');self.assertEqual(len(data['artworks']),6)
   for a in data['artworks']:self.assertTrue((out/a['original']).is_file())
   if not (ROOT/'assets/local/fonts').exists():self.assertFalse(data['hasBundledFonts']);self.assertNotIn('@font-face',(out/'fonts.css').read_text())
   before=(out/'content.js').read_bytes();p=run('scaffold.py','--out',out);self.assertNotEqual(p.returncode,0);self.assertEqual(before,(out/'content.js').read_bytes())
 def test_invalid_asset_creates_no_directory(self):
  with tempfile.TemporaryDirectory() as temp:
   out=Path(temp)/'site';p=run('scaffold.py','--out',out,'--asset','NOT-A-REAL-ASSET');self.assertNotEqual(p.returncode,0);self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
