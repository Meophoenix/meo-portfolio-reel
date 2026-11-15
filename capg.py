import sys, os, time, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
from playwright.sync_api import sync_playwright
mode=sys.argv[1]
if mode=='stills':
    times=[float(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]; os.makedirs(out,exist_ok=True)
    frames=[(round(t*30), f'{out}/s_{t:06.2f}.jpg') for t in times]
else:
    a,b=int(sys.argv[2]),int(sys.argv[3]); out=sys.argv[4] if len(sys.argv)>4 else 'frames'; frames=[(f,f'{out}/f_{f:04d}.jpg') for f in range(a,b)]
with sync_playwright() as p:
    br=p.chromium.launch(args=['--force-device-scale-factor=1','--font-render-hinting=none'])
    pg=br.new_page(viewport={'width':1080,'height':1920})
    msgs=[]
    pg.on('console',lambda m:msgs.append(m.text)); pg.on('pageerror',lambda e:msgs.append('ERR '+str(e)))
    pg.goto((ROOT/'film2.html').as_uri()); pg.wait_for_function('window.READY===true',timeout=30000)
    t0=time.time()
    for f,path in frames:
        pg.evaluate(f'render({f}/30)'); pg.evaluate('window.waitImgs()')
        pg.screenshot(path=path,type='jpeg',quality=92)
    print('done',len(frames),'frames',round(time.time()-t0,1),'s'); print('\n'.join(msgs[:10]))
    br.close()
