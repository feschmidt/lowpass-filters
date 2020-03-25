---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

Transfer function of a single stage RC filter:

\begin{align}
\frac{V_{\rm out}}{V_{\rm in}} = \frac{1}{1+i\omega RC}
\end{align}


Transfer function of a two stage RC filter:

\begin{align}
H(\omega) = \frac{1}{-\omega^2 R_1R_2C_1C_2 + i\omega\left(R_1C_1+R_1C_2+R_2C_2\right)+1}
\end{align}



For noise calculations, see
* https://link.springer.com/article/10.1140/epjqt/s40507-019-0072-0
* https://blog.qutech.nl/index.php/2020/02/20/cooling-a-hot-photon-wind-part-1/
* https://en.wikipedia.org/wiki/Johnson%E2%80%93Nyquist_noise

```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

# General

```python
w=2*pi*np.logspace(3,7,401)
R1,C1,R2,C2=470,10e-9,2e3,470e-12
```

```python
vratio = S21(w,R1,C1,R2,C2)
pratio = S21dB(w,R1,C1,R2,C2)
```

```python
from scipy.optimize import fsolve
```

```python
def myfun(w,*args):
    R1,C1,R2,C2 = args
    return S21dB(w,R1,C1,R2,C2)-(-3)
```

```python
f3dB=fsolve(myfun,30e3,args=(R1,C1,R2,C2))/2/pi
f3dB
```

```python
plt.plot(w/2/pi,pratio)
plt.axhline(-3,c='k',ls='--')
plt.axvline(f3dB,c='C3')
plt.xscale('log')
```

```python
plt.plot(w/2/pi,S21ph(w,R1,C1,R2,C2))
plt.axvline(f3dB,c='C3')
plt.xscale('log')
```

# Compare filters

```python
f=np.logspace(3,7,401)
w=2*pi*f
filter_Delft = S21dB(w,R1=470,C1=10e-9,R2=2e3,C2=470e-12)
filter1 = S21dB(w,R1=100,C1=33e-9,R2=100,C2=33e-9)
filtersingle = S21dB(w,R1=470,C1=10e-9,R2=0,C2=0)
```

```python
plt.plot(f,filter_Delft)
plt.plot(f,filter1)
plt.plot(f,filtersingle)
plt.xscale('log')
plt.axhline(-3,ls='--',c='k')
```

```python
fsolve(myfun,30e3,args=(100,33e-9,100,33e-9))/2/pi
```

```python
fsolve(myfun,30e3,args=(470,10e-9,2000,470e-12))/2/pi
```

```python
fsolve(myfun,30e3,args=(470,10e-9,0,0))/2/pi
```

# Attenuations

```python
from scipy.constants import h,Boltzmann
```

```python
kB=Boltzmann
```

```python
from numpy import exp
```

```python
def nBE(f,T):
    return 1/(exp(h*f/kB/T)-1)

def Att(f,T1,T2):
    return nBE(f,T2)/nBE(f,T1)

def AttdB(f,T1,T2):
    return 10*np.log10(Att(f,T1,T2))

def Attapp(T1,T2):
    return 10*np.log10(T2/T1)

def nphot(f,T1,T2,W):
    return W*nBE(f,T1)+(1-W)*nBE(f,T2)

def Tnew(f,T1,T2,W):
    n = nphot(f,T1,T2,W)
    return h*f/(kB*np.log((n+1)/n))
```

## single-stage calculations

```python
#freqs = np.logspace(1,10,401)
freqs = np.linspace(1,20e9,401)
T1=300
T2=3
```

```python
plt.plot(freqs,AttdB(freqs,300,100))
plt.axhline(Attapp(300,100),c='C0',ls='--')
plt.plot(freqs,AttdB(freqs,300,30))
plt.axhline(Attapp(300,30),c='C1',ls='--')
plt.plot(freqs,AttdB(freqs,300,3))
plt.axhline(Attapp(300,3),c='C2',ls='--')
#plt.xscale('log')
```

```python
plt.plot(freqs,nBE(freqs,300))
plt.plot(freqs,nBE(freqs,3))
plt.plot(freqs,nphot(freqs,300,3,0.01))
plt.xscale('log')
plt.yscale('log')
```

```python
plt.plot(freqs,Tnew(freqs,300,3,0.01))
plt.xscale('log')
```

```python
atts = np.linspace(-40,0,401)
```

```python
plt.plot(atts,Tnew(1,300,3,10**(atts/10)))
plt.yscale('log')
```

## 300K to 10mK


Let's assume we have the following stages: 300K, 50K, 4K, 1K, 0.1K, 0.01K, and we use the following attenuators (typical for our setups): 3, 6, 20, 20, 3

```python
freqs = np.logspace(0,12,401)
```

```python
# after 3dB at 50K
att50=3
n50 = nphot(freqs,300,50,10**(-att50/10))
T50 = Tnew(freqs,300,50,10**(-att50/10))

# after 6dB at 4K
att4=6
n4 = nphot(freqs,T50,4,10**(-att4/10))
T4 = Tnew(freqs,T50,4,10**(-att4/10))

# after 20dB at 1K
attStill=20
nStill = nphot(freqs,T4,1,10**(-attStill/10))
TStill = Tnew(freqs,T4,1,10**(-attStill/10))

# after 20dB at 100mK
attCold=20
nCold = nphot(freqs,TStill,0.1,10**(-attCold/10))
TCold = Tnew(freqs,TStill,0.1,10**(-attCold/10))

# after 3dB at 10mK
attMXC=10
nMXC = nphot(freqs,TCold,0.01,10**(-attMXC/10))
TMXC = Tnew(freqs,TCold,0.01,10**(-attMXC/10))

attTotal = att50+att4+attStill+attCold+attMXC
for x,theatt in zip([50,4,1,0.1,0.01],[att50,att4,attStill,attCold,attMXC]):
    print(f'Attenuation at {x} K: {theatt} dB')
print(f'Total attenuation: {attTotal} dB')
print(f'Minimum temperature at MXC: {min(TMXC)} K')
```

```python
fig=plt.figure(figsize=(12,4))
gs=fig.add_gridspec(1,2)
ax1=fig.add_subplot(gs[0,0])
plt.plot(freqs,T50)
plt.plot(freqs,T4)
plt.plot(freqs,TStill)
plt.plot(freqs,TCold)
plt.plot(freqs,TMXC)
[plt.axhline(x,c='C'+str(i),ls='--') for i,x in enumerate([50,4,1,0.1,0.01])]
plt.yscale('log')
plt.xscale('log')
plt.ylabel('Temperature (K)')

ax2=fig.add_subplot(gs[0,1])
plt.plot(freqs,n50)
plt.plot(freqs,n4)
plt.plot(freqs,nStill)
plt.plot(freqs,nCold)
plt.plot(freqs,nMXC)
plt.axhline(1,c='k',ls='--')
plt.yscale('log')
plt.xscale('log')
ylim = ax2.get_ylim()
[plt.plot(freqs,nBE(freqs,x),c='C'+str(i),ls='--',label=x) for i,x in enumerate([50,4,1,0.1,0.01])]
ax2.set_ylim(ylim)
plt.ylabel('Photon flux')
plt.legend()

for theax in [ax1,ax2]:
    #theax.set_xscale('log')
    #theax.set_yscale('log')
    theax.set_xlabel('Frequency (Hz)')
    
plt.suptitle('RF attenuators')
plt.savefig('plots/theo_RFatt.png',dpi=dpi,bbox_inches='tight')
plt.show()
plt.close()

print('Dashed lines: stage temperature/photon flux of',[50,4,1,0.1,0.01],'K')
print('Solid lines: electronic noise temperature/photon flux of the corresponding stages')
```

```python
fig = plt.figure()
[plt.plot(freqs,kB*x/(h*freqs),label=x) for i,x in enumerate([50,4,1,0.1,0.01])]
plt.axhline(1,c='k',ls='--')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel(r'$k_B T/h\nu$')
plt.show()
plt.close()

print('Deviations from exected stage temperature occur for hf>kT')
```

## DC low-pass He7

```python
myfiles = [
    dataHe7+'F5_2018_12_17_16.58.52_powersweep_RT_short_blue2/F5_2018_12_17_16.58.52_powersweep_RT_short_blue2.dat',
    dataHe7+'F7_2018_12_17_17.03.43_powersweep_RT_short_blue2_RCfilter/F7_2018_12_17_17.03.43_powersweep_RT_short_blue2_RCfilter.dat',
    dataHe7+'F10_2018_12_17_17.11.26_powersweep_RT_short_blue2_CuPW/F10_2018_12_17_17.11.26_powersweep_RT_short_blue2_CuPW.dat',
    dataHe7+'F13_2018_12_17_17.16.50_powersweep_RT_short_blue2_RC_CuPW/F13_2018_12_17_17.16.50_powersweep_RT_short_blue2_RC_CuPW.dat'
]

rfpower = 0
data_all_filters = []
names_all_filters = ['no filter', 'RC only', 'CuPW only', 'RC+CuPW']

for myfile in myfiles:
    data0 = stlabutils.readdata.readdat_pd(myfile)
    data = copy.deepcopy(data0)
    try:
        mtx = framearr_to_mtx(
            data=data,
            key='S21dB (dB)',
            xkey='Power (dBm)',
            ykey='Frequency (Hz)')
    except KeyError:
        continue

    # plotting linecut for reference
    linecut = mtx.pmtx[rfpower]
    #linecut -= linecut.iloc[0]
    data_all_filters.append(linecut)
```

```python
fig = plt.figure()#figsize=cm2inch(12,8))

for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line,label=name)
plt.legend()
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|S$_{21}$| (dB)')
plt.tight_layout()
plt.show()
plt.close()
```

```python
fmeas = line.index.values
attDC = abs(data_all_filters[-1])
```

```python
nDC = nphot(fmeas,300,0.01,10**(-attDC/10))
TDC = Tnew(fmeas,300,0.01,10**(-attDC/10))
print(f'Minimum temperature at MXC: {min(TDC)} K')
```

```python
fig=plt.figure(figsize=(12,4))
gs=fig.add_gridspec(1,2)
ax1=fig.add_subplot(gs[0,0])
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line.index.values,Tnew(fmeas,300,0.01,10**(-abs(line.values)/10)),label=name)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Noise temperature (K)')
plt.axhline(0.01,c='k',ls='--')
plt.legend()

ax2=fig.add_subplot(gs[0,1])
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line.index.values,nphot(fmeas,300,0.01,10**(-abs(line.values)/10)),label=name)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Photon flux')
plt.legend()
plt.axhline(1,c='k',ls='--')

plt.suptitle('DC filters')
plt.savefig('plots/theo_DCatt.png',dpi=dpi,bbox_inches='tight')
plt.show()
plt.close()
```

```python

```

## DC low-pass Triton

```python
myfiles = sorted(glob.glob(datamisc+'*triton*'))
myfiles

RCfile = myfiles[3]
CPfile = myfiles[1]
RCCPfile = myfiles[2]

RCdata= np.loadtxt(RCfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)
CPdata= np.loadtxt(CPfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)
RCCPdata= np.loadtxt(RCCPfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)

fmeas = RCdata[0]
```

```python
fig = plt.figure()#figsize=cm2inch(12,8))

plt.plot(fmeas,RCdata[3],label='RC filter')
plt.plot(fmeas,CPdata[3],label='CP filter')
plt.plot(fmeas,RCCPdata[3],label='RC + CP')
plt.legend()
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|S$_{21}$| (dB)')
plt.tight_layout()
plt.show()
plt.close()
```

```python
attDC = abs(RCCPdata[3])
```

```python
nDC = nphot(fmeas,300,0.01,10**(-attDC/10))
TDC = Tnew(fmeas,300,0.01,10**(-attDC/10))
print(f'Minimum temperature at MXC: {min(TDC)} K')
```

```python
fig=plt.figure(figsize=(12,4))
gs=fig.add_gridspec(1,2)
ax1=fig.add_subplot(gs[0,0])
for name, line in zip(['RC filter','CP filter','RC+CP filter'], [RCdata[3],CPdata[3],RCCPdata[3]]):
    plt.plot(fmeas,Tnew(fmeas,300,0.01,10**(-abs(line)/10)),label=name)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Noise temperature (K)')
plt.axhline(0.01,c='k',ls='--')
plt.legend()

ax2=fig.add_subplot(gs[0,1])
for name, line in zip(['RC filter','CP filter','RC+CP filter'], [RCdata[3],CPdata[3],RCCPdata[3]]):
    plt.plot(fmeas,nphot(fmeas,300,0.01,10**(-abs(line)/10)),label=name)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Photon flux')
plt.legend()
plt.axhline(1,c='k',ls='--')

plt.suptitle('DC filters')
plt.savefig('plots/theo_DCatt_Triton.png',dpi=dpi,bbox_inches='tight')
plt.show()
plt.close()
```

```python

```
