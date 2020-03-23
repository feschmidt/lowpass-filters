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

<!-- #region toc=true -->
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"></ul></div>
<!-- #endregion -->

```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

```python
sorted(glob.glob(datamisc+'*'))
```

```python
myfiles = sorted(glob.glob(datamisc+'*triton*'))
myfiles
```

```python
RCfile = myfiles[3]
CPfile = myfiles[1]
RCCPfile = myfiles[2]
```

```python
RCdata= np.loadtxt(RCfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)
CPdata= np.loadtxt(CPfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)
RCCPdata= np.loadtxt(RCCPfile,delimiter=';',skiprows=3,usecols=range(5),unpack=True)
```

```python
ftheo = RCdata[0,:]
```

```python
fig = plt.figure(figsize=cm2inch(12,8))

plt.plot(RCdata[0,:],RCdata[3,:],label='RC filter')
plt.plot(CPdata[0,:],CPdata[3,:],label='CP filter')
plt.plot(RCCPdata[0,:],RCCPdata[3,:],label='RC + CP')

#plt.plot(ftheo,S21dB(w=2*pi*ftheo,R1=470,C1=10e-9,R2=2e3,C2=470e-12),c='k',ls='--',label='theo')

plt.legend()
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|S$_{21}$| (dB)')
plt.tight_layout()
plt.savefig('plots/misc_RC_measured_python.png',bbox_to_inches='tight',dpi=1000)
plt.show()
plt.close()
```

```python

```
