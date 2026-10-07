"""Netlify build: create a deploy directory containing only public site files."""
from pathlib import Path
import shutil
from configure_seo import configure
ROOT=Path(__file__).resolve().parent.parent
configure(ROOT)
out=ROOT/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir()
for name in ['index.html','privacy.html','404.html','styles.css','legal.css','script.js','config.js','robots.txt','sitemap.xml','_headers','_redirects']:
    source=ROOT/name
    if source.exists(): shutil.copy2(source,out/name)
shutil.copytree(ROOT/'assets',out/'assets')
print('배포 폴더: '+str(out))
