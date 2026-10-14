import os
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[1]
out=root/'runtime/tests'
out.mkdir(parents=True,exist_ok=True)
web=root/'internal/services/gmtool/wwwroot'
section=re.search(r'  <section id="benefits-panel".*?</section>',(web/'index.html').read_text(encoding='utf-8'),re.S).group(0)
fixture='<html><head><meta charset="utf-8"><style>'+(web/'style.css').read_text(encoding='utf-8')+'</style></head><body><button id="btn-benefits">测试福利</button>'+section+'</body></html>'
campaigns=[]; jobs=[]; calls=[]; errors=[]
def route(r):
    path=r.request.url.split('http://benefits.test')[1]
    if path=='/': return r.fulfill(content_type='text/html',body=fixture)
    data=r.request.post_data_json if r.request.method=='POST' else None
    calls.append((path,data))
    if path=='/api/benefits': reply={'policy':{'revision':0,'accountCera':0,'characterGold':0},'jobs':jobs,'campaigns':campaigns}
    elif path=='/api/benefits/campaigns':
        assert data['itemId']==490009735 and data['count']==1
        c={'id':'a'*32,'revision':0,'enabled':False,'itemName':'天空自选礼盒 <b>fixture</b>','autoNewCharacters':True,'reward':{'title':data['title'],'body':data['body'],'gold':0,'attachments':[{'item_id':data['itemId'],'count':data['count']}]}}
        campaigns.append(c);reply={'campaign':c}
    elif path.endswith('/state'):
        assert data['confirm'] is True
        campaigns[0]['enabled']=data['enabled'];campaigns[0]['revision']+=1;reply={'campaign':campaigns[0]}
    elif path.endswith('/preview'):
        recipients=[{'accountId':'a','characterId':'1','name':'已发角色','mailId':'1'},{'accountId':'b','characterId':'2','name':'新增角色'}]
        job=dict(campaigns[0]['reward'],id='b'*32,campaignId='a'*32,createdAt='2026-10-14T00:00:00Z',started=False,recipients=recipients)
        jobs.insert(0,job);reply={'job':job}
    elif path.endswith('/run'):
        assert data['confirm'] is True
        jobs[0]['started']=True;jobs[0]['recipients'][1]['mailId']='2';reply={'job':jobs[0]}
    else: raise AssertionError(path)
    r.fulfill(content_type='application/json',body=json.dumps(dict(success=True,**reply)))

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, **({'channel':os.environ['BROWSER_CHANNEL']} if os.environ.get('BROWSER_CHANNEL') else {}))
    page=browser.new_page(viewport={'width':1280,'height':960})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.route('http://benefits.test/**',route);page.goto('http://benefits.test/')
    page.add_script_tag(content="const $=s=>document.querySelector(s);async function api(p,o){const d=await(await fetch(p,o)).json();if(d.success===false)throw Error(d.error);return d;}function post(p,b){return api(p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});}")
    page.add_script_tag(content=(web/'js/benefits.js').read_text(encoding='utf-8'))
    page.click('#btn-benefits');expect(page.locator('#benefits-save')).to_be_enabled()
    page.fill('#benefits-item-id','490009735');page.check('#benefits-item-auto')
    page.once('dialog',lambda d:d.dismiss());page.click('#benefits-item-create')
    assert not campaigns
    page.once('dialog',lambda d:d.accept());page.click('#benefits-item-create')
    expect(page.locator('#benefits-campaigns')).to_contain_text('已停用')
    assert not any(path.endswith('/run') for path,_ in calls)
    assert page.locator('#benefits-campaigns b').count()==0
    expect(page.locator('#benefits-campaigns')).to_contain_text('490009735 × 1')
    page.once('dialog',lambda d:d.dismiss());page.get_by_role('button',name='启用规则',exact=True).click()
    assert not campaigns[0]['enabled']
    page.once('dialog',lambda d:d.accept());page.get_by_role('button',name='启用规则',exact=True).click()
    expect(page.locator('#benefits-campaigns')).to_contain_text('已启用')
    page.get_by_role('button',name='预览现有角色／补发').click()
    expect(page.locator('#benefits-state')).to_contain_text('已发 1，待补发 1')
    assert not any(path.endswith('/run') for path,_ in calls)
    page.locator('#benefits-jobs summary').click()
    page.locator('#benefits-jobs').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'gm-item-preview.png'))
    page.once('dialog',lambda d:d.accept());page.locator('#benefits-jobs button').click()
    expect(page.locator('#benefits-state')).to_contain_text('已发送 2 封')
    assert len([path for path,_ in calls if path.endswith('/run')])==1
    page.once('dialog',lambda d:d.accept());page.get_by_role('button',name='停用规则',exact=True).click()
    expect(page.locator('#benefits-campaigns')).to_contain_text('已停用')
    page.locator('#benefits-item-form').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'gm-item-rules.png'))
    assert not errors,errors
    browser.close()
print('PASS browser: editable item ID/count, cancel, default disabled, enable/disable confirmation, dedup preview, send confirmation, escaped content')
