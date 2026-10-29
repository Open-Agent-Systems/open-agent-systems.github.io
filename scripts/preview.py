"""Export an isolated, noindex preview from a built design branch."""
from pathlib import Path
import argparse,json,re,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--slug',required=True);p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a.slug):p.error('slug must be lowercase letters, digits and hyphens')
root=Path(__file__).resolve().parents[1];source=root/'docs';dest=a.destination.resolve();prefix='/previews/'+a.slug
if dest==source or source in dest.parents:p.error('export outside the source docs tree')
if dest.exists():p.error('destination already exists; choose a new path')
shutil.copytree(source,dest,ignore=shutil.ignore_patterns('previews','.DS_Store'))
for page in dest.rglob('*.html'):
 text=page.read_text().replace('href="/','href="'+prefix+'/').replace('src="/','src="'+prefix+'/')
 text=text.replace('https://open-agent-systems.github.io/','https://open-agent-systems.github.io'+prefix+'/')
 text=text.replace('<head>','<head><meta name="robots" content="noindex,nofollow">')
 banner='<aside style="padding:10px 20px;background:#fff4e9;color:#623b21;text-align:center;font:12px sans-serif">Design preview / 设计预览 · '+a.slug+' · <a href="https://open-agent-systems.github.io/zh/" style="color:inherit">当前正式版 / Live site ↗</a></aside>'
 text=text.replace('<body>','<body>'+banner);page.write_text(text)
for name in ['sitemap.xml','robots.txt']:
 path=dest/name
 if path.exists():path.unlink()
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
(dest/'preview.json').write_text(json.dumps({'slug':a.slug,'source_commit':commit,'status':'preview'},indent=2)+'\n')
print('[PASS] Preview exported to '+str(dest))
