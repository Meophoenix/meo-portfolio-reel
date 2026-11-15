import numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile
SR=48000; DUR=108.75; N=int(SR*DUR)
rng=np.random.default_rng(11)
L=np.zeros(N);Rr=np.zeros(N)
def put(t,x,g=1.0,pan=0.0):
    i=int(t*SR)
    if i>=N or i+len(x)<=0: return
    a=max(0,-i); x=x[a:]; i=max(0,i); n=min(len(x),N-i); x=x[:n]
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=x*g*l*1.414; Rr[i:i+n]+=x*g*r*1.414
def lp(x,f,o=2): b,a=butter(o,f/(SR/2),'low'); return lfilter(b,a,x)
def hp(x,f,o=2): b,a=butter(o,f/(SR/2),'high'); return lfilter(b,a,x)
def bp(x,f1,f2,o=2): b,a=butter(o,[f1/(SR/2),f2/(SR/2)],'band'); return lfilter(b,a,x)
def tt(d): return np.arange(int(SR*d))/SR
def env(n,a,d):  # attack, decay (exp)
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))*np.exp(-t/d); return e
def kick(): t=tt(.35); f=45+90*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*env(len(t),.002,.11)*1.0+hp(rng.normal(0,1,len(t)),3000)*env(len(t),.001,.006)*.15
def clap(): t=tt(.3); n=bp(rng.normal(0,1,len(t)),1200,4500); e=env(len(t),.001,.07)+.6*env(len(t),.001,.02); return n*e*.8
def hat(o=False): t=tt(.25 if o else .06); n=hp(rng.normal(0,1,len(t)),7000); return n*env(len(t),.001,.09 if o else .018)*.5
def bass(f,d=.45): t=tt(d); s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*8)+.15*((2*((f*t)%1)-1)); return lp(s,420)*env(len(t),.004,d*.55)
def pluck(f,d=.35): t=tt(d); s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t+.3)+.25*np.sin(2*np.pi*3*f*t); s=lp(s,3500)*env(len(t),.002,.12); return s*.5
def padchord(freqs,d): 
    t=tt(d); s=np.zeros(len(t))
    for f in freqs:
        for dt in (-.4,0,.4): s+=np.sin(2*np.pi*(f+dt)*t)+.3*np.sin(2*np.pi*2*f*t)
    s=lp(s,1800); a=np.minimum(1,t/.5)*np.minimum(1,(d-t)/.6); return s*a/ (len(freqs)*3)
def whoosh(d,up=True,f1=300,f2=6000):
    t=tt(d); n=rng.normal(0,1,len(t)); out=np.zeros(len(t)); seg=24
    for k in range(seg):
        a=int(k*len(t)/seg); b=int((k+1)*len(t)/seg); fr=k/seg; fc=f1*(f2/f1)**(fr if up else 1-fr)
        out[a:b]=bp(n,max(100,fc*.7),min(20000,fc*1.4))[a:b]
    e=(t/d)**2.2 if up else (1-t/d)**2; e=e*np.minimum(1,(d-t)/.02); return out*e
def impact(): t=tt(1.2); f=60+120*np.exp(-t*14); s=np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(t),.002,.35); n=lp(rng.normal(0,1,len(t)),1500)*env(len(t),.001,.25)*.5; return s+n
def click(): t=tt(.08); return (hp(rng.normal(0,1,len(t)),2500)*env(len(t),.0005,.008)+np.sin(2*np.pi*1800*t)*env(len(t),.0005,.012)*.5)
def glass(f=1760): t=tt(.5); s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.76*t)+.3*np.sin(2*np.pi*f*5.4*t); return s*env(len(t),.001,.09)*.35
def blip(f): t=tt(.2); return np.sin(2*np.pi*f*t)*env(len(t),.002,.05)*.5
def chime(f): t=tt(1.6); s=sum(np.sin(2*np.pi*f*m*t)*a for m,a in [(1,1),(2,.5),(3,.25),(4.01,.15)]); return s*env(len(t),.003,.5)*.4
def sparkle(): t=tt(.7); s=sum(np.sin(2*np.pi*f*t)*np.exp(-t*7)*(t>d0) for f,d0 in [(2637,0),(3136,.05),(3951,.1),(4699,.15)]); return s*.3


N_=lambda m: 440*2**((m-69)/12)
BPM=128; B=60/BPM; BAR=4*B
T=[0,5.625,13.125,22.5,31.875,35.625,45.0,54.375,63.75,78.75,97.5,108.75]; ROLE=[5.625,8.0,10.5]
prog=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]; rootm=[45,41,36,43]
nb=int(DUR/B); NB=58
def intr(bar): return 17<=bar<19
for bar in range(NB):
    ch=prog[bar%4]; g=.18 if bar<3 else .24
    if bar>=54: ch=(57,60,64,69); g=.22*(1-(bar-54)/5)
    put(bar*BAR,padchord([N_(m) for m in ch],BAR+.5),g,0)
for beat in range(nb):
    t=beat*B; bar=int(t//BAR)
    kick_on=(bar>=1 and bar<54 and not intr(bar))
    if kick_on: put(t,kick(),.5 if bar<3 else .8)
    if bar>=3 and beat%2==1 and bar<54 and not intr(bar): put(t,clap(),.42)
    if intr(bar) and beat%2==1: put(t,clap(),.3)
    if bar<56: put(t+B/2,hat(),.2 if bar<3 else .24)
    if bar>=7 and bar<54: put(t,hat(True) if beat%4==3 else hat(),.16)
    if intr(bar):
        for k in range(4): put(t+k*B/4,hat(),.1+.05*k)
for bar in range(3,54):
    if intr(bar): continue
    r=N_(rootm[bar%4])
    for k,(off,d) in enumerate([(0,.4),(.75*B,.3),(2*B,.4),(3*B,.3)]):
        put(bar*BAR+off,bass(r*(2 if k==3 else 1),d+.1),.5)
for s16 in range(int(7*BAR/(B/4)),int(54*BAR/(B/4))):
    t=s16*(B/4); bar=int(t//BAR)
    if intr(bar): continue
    ch=prog[bar%4]; notes=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+24]
    put(t,pluck(N_(notes[s16%4])),.13,pan=np.sin(s16*.7)*.5)
for i,tb in enumerate(T[1:11],1):
    put(tb-.75,whoosh(.75,True),.36); put(tb,impact(),.4)
for tm,f in [(.1,880),(T[1]+.15,1175),(T[2]+.2,1319),(T[3]+.2,1175),(T[4]+.05,1568),(T[4]+.85,1760),(T[4]+1.65,1976),(T[5]+.2,1319),(T[6]+.2,1175),(T[7]+.2,1319),(T[8]+.3,1175),(T[9]+.2,1319),(T[10]+.5,1568)]:
    put(tm,whoosh(.35,True,800,7000),.1); put(tm+.28,blip(f),.12)
for tr in ROLE[1:]: put(tr-.1,whoosh(.4,True,600,6000),.2); put(tr+.2,click(),.4)
for tc,p in [(4.0,.2),(T[3]-.85,0),(T[6]-.85,-.3),(T[10]-.85,.3)]: put(tc,click(),.55,p)
chipt=[T[2]+1.0,T[3]+.9,T[5]+1.0,T[6]+1.0,T[7]+1.0,T[8]+5.5,T[8]+6.5,T[8]+7.5,T[8]+8.5,T[8]+10.3,T[9]+1.0,T[9]+11.2]
for i,tc in enumerate(chipt): put(tc+.3,glass(1568+(i%3)*220),.2,pan=-.3+.1*(i%7))
for k,tc in enumerate([3.5,3.65,3.8]): put(tc,glass(1318+k*200),.18)
for i in range(4): put(ROLE[0]+.15+i*.12+.1,glass(1000+i*230),.12)
for i in range(4): put(T[2]+1.0+1.3*i-.4,whoosh(.45,True,400,4000),.1)
# FutureGate / Delivery Ease device moves
for tc in [T[6]+1.0,T[6]+3.7,T[6]+4.0,T[6]+6.2,T[7]+.2,T[7]+4.3,T[7]+4.9]: put(tc,whoosh(.5,True,500,5000),.12)
# video cuts
for st in [.9,4.4,7.9,11.4,14.4]: put(T[9]+st,click(),.5); put(T[9]+st,glass(1760),.18)
# close
put(T[10]+4.2,chime(N_(69)),.3); put(T[10]+4.3,chime(N_(76)),.2); put(T[10]+5.6,sparkle(),.35)
for k,m in enumerate([69,72,76,81]): put(T[10]+.1+k*.12,pluck(N_(m),.8),.2,pan=-.3+k*.2)
mx=np.stack([L,Rr],1); mx=mx/max(1e-9,np.max(np.abs(mx)))*.9
f=np.ones(N); f[:int(.02*SR)]=np.linspace(0,1,int(.02*SR)); f[-int(1.5*SR):]=np.linspace(1,0,int(1.5*SR))
mx*=f[:,None]
wavfile.write('raw3.wav',SR,(mx*32767).astype(np.int16)); print('ok')
