from playwright.sync_api import sync_playwright
import sys, pathlib
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto((pathlib.Path(__file__).resolve().parent/'film2.html').as_uri()); pg.wait_for_function('window.READY===true')
    seen=set(); n=0
    t=0.0
    while t<108.75:
        r=pg.evaluate(f'audit({t})')
        for x in r:
            key=x.split('"')[0]+x.split('"')[1]
            if key not in seen: seen.add(key); print(round(t,2),x)
        t+=0.25
    print('audit done',len(seen))
    b.close()
