from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import argparse
parser=argparse.ArgumentParser(description='Check the three bundled offline application examples.')
parser.add_argument('--out',required=True);parser.add_argument('--channel',default='msedge');args=parser.parse_args()
R=Path(__file__).resolve().parents[1];Q=Path(args.out).resolve();Q.mkdir(parents=True,exist_ok=True)
checks={};errors=[];requests=[];failed=[]
def check(name,ok):
 checks[name]=bool(ok)
def listen(page):
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.on('requestfailed',lambda r:failed.append(r.url))
with sync_playwright() as p:
 browser=p.chromium.launch(channel=args.channel,headless=True)
 c=browser.new_context(offline=True,viewport={'width':1440,'height':1000},accept_downloads=True)
 pages={}
 for name in ['paper','article','garden']:
  page=c.new_page();listen(page);pages[name]=page
  page.goto((R/f'examples/{name}/index.html').as_uri());page.evaluate('document.fonts.ready')
  page.evaluate('localStorage.clear()');page.reload();page.wait_for_timeout(300)
  check(name+'_all_images_loaded',page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'))
  check(name+'_desktop_no_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.screenshot(path=str(Q/f'{name}-desktop.png'),full_page=True)
  page.screenshot(path=str(Q/f'{name}-cover.png'))
 paper=pages['paper'];paper.bring_to_front()
 paper.locator('#tab-method').click();check('paper_tabs_change_visible_content',paper.locator('#panel-method').is_visible() and not paper.locator('#panel-summary').is_visible())
 paper.keyboard.press('ArrowRight');check('paper_tabs_keyboard_navigation',paper.locator('#tab-limits').evaluate('e=>e===document.activeElement') and paper.locator('#panel-limits').is_visible())
 before=paper.locator('#research-figure').get_attribute('src');paper.locator('#figure-switch').click();paper.locator('#research-figure').evaluate('e=>e.decode()');check('paper_figure_switch_changes_real_asset',paper.locator('#research-figure').get_attribute('src')!=before and '对话' in paper.locator('#research-figure').get_attribute('alt'))
 paper.locator('summary').click();check('paper_method_expands',paper.locator('details').evaluate('e=>e.open'))
 with paper.expect_download() as dl:paper.locator('#download-citation').click()
 dest=Q/dl.value.suggested_filename;dl.value.save_as(dest);check('paper_downloads_truthful_bibtex','@misc{' in dest.read_text() and 'not a research publication' in dest.read_text())
 article=pages['article'];article.bring_to_front();before=article.locator('.essay p').nth(1).evaluate('e=>getComputedStyle(e).fontSize');article.locator('#font-up').click();check('article_font_control_changes_text',article.locator('.essay p').nth(1).evaluate('e=>getComputedStyle(e).fontSize')!=before)
 article.locator('#bookmark').click();article.reload();check('article_reading_preferences_persist',article.locator('#bookmark').get_attribute('aria-pressed')=='true' and article.locator('.essay').evaluate("e=>e.style.getPropertyValue('--reading-size')==='18px'"))
 article.evaluate('scrollTo(0,document.body.scrollHeight)');article.wait_for_timeout(600);check('article_reading_progress_tracks_scroll',article.locator('#reading-progress').evaluate('e=>parseFloat(e.style.width)>95'))
 for _ in range(5):
  if article.locator('#font-up').is_enabled():article.locator('#font-up').click()
 check('article_font_limit_is_enforced',article.locator('#font-up').is_disabled() and article.locator('.essay').evaluate("e=>e.style.getPropertyValue('--reading-size')==='22px'"))
 garden=pages['garden'];garden.bring_to_front();initial=garden.locator('.idea-card').count();check('garden_initial_examples_present',initial==3)
 title='做一本 <手写> & 小书';garden.locator('#idea-input').fill(title);garden.locator('#plant-form button').click()
 check('garden_adds_safe_text_card',garden.locator('.idea-card').count()==4 and garden.locator('#detail-title').inner_text()==title and garden.locator('#detail-title>*').count()==0)
 garden.locator('#advance-idea').click();check('garden_advances_stage_and_counts',garden.locator('#growing-count').inner_text()=='2' and garden.locator('[data-stage="1"]').evaluate("e=>e.classList.contains('active')"))
 garden.locator('[data-filter="1"]').click();check('garden_filter_selects_stage',garden.locator('.idea-card').count()==2)
 garden.reload();check('garden_created_note_and_stage_persist',garden.locator('.idea-card').count()==4 and garden.locator('#detail-title').inner_text()==title and garden.locator('#growing-count').inner_text()=='2')
 garden.locator('#advance-idea').click();check('garden_completes_note',garden.locator('#advance-idea').is_disabled() and garden.locator('#ripe-count').inner_text()=='2')
 with garden.expect_download() as dl:garden.locator('#export-garden').click()
 dest=Q/dl.value.suggested_filename;dl.value.save_as(dest);data=json.loads(dest.read_text());check('garden_download_matches_saved_data',len(data['ideas'])==4 and data['ideas'][0]['title']==title and data['ideas'][0]['stage']==2)
 before=garden.locator('.garden-hero .illustration').evaluate('e=>getComputedStyle(e).transform');garden.wait_for_timeout(600);after=garden.locator('.garden-hero .illustration').evaluate('e=>getComputedStyle(e).transform');check('garden_motion_actually_moves',before!=after)
 garden.locator('#garden-motion').click();before=garden.locator('.garden-hero .illustration').evaluate('e=>getComputedStyle(e).transform');garden.wait_for_timeout(500);check('garden_pause_stops_motion',before==garden.locator('.garden-hero .illustration').evaluate('e=>getComputedStyle(e).transform'))
 for name,page in pages.items():
  page.bring_to_front()
  for width in [390,360]:
   page.set_viewport_size({'width':width,'height':844});page.evaluate('scrollTo(0,0)');page.wait_for_timeout(400)
   check(f'{name}_{width}_no_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   page.screenshot(path=str(Q/f'{name}-mobile-{width}.png'),full_page=True)
  page.emulate_media(reduced_motion='reduce');check(name+'_reduced_motion_css',page.evaluate("getComputedStyle(document.documentElement).scrollBehavior==='auto'"))
 garden.emulate_media(reduced_motion='reduce');garden.wait_for_timeout(100);check('garden_reduced_motion_disables_animation',garden.locator('#garden-motion').is_disabled() and garden.locator('.garden-hero .illustration').evaluate("e=>getComputedStyle(e).animationName==='none'"))
 check('no_javascript_or_console_errors',not errors);check('zero_network_requests',not requests);check('no_failed_resources',not failed)
 browser.close()
report=dict(passed=all(checks.values()),checks=checks,errors=errors,network_requests=requests,failed_resources=failed)
(Q/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],checks=len(checks),failed=[k for k,v in checks.items() if not v],errors=errors),ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
