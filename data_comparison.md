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
<div class="toc"><ul class="toc-item"><li><span><a href="#Data-comparison" data-toc-modified-id="Data-comparison-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data comparison</a></span><ul class="toc-item"><li><span><a href="#Triton" data-toc-modified-id="Triton-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Triton</a></span></li><li><span><a href="#He7" data-toc-modified-id="He7-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>He7</a></span></li></ul></li><li><span><a href="#Plot" data-toc-modified-id="Plot-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Plot</a></span></li></ul></div>
<!-- #endregion -->

```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

# Data comparison


## Triton

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
fTriton = RCdata[0,:]
```

## He7

```python
myfiles = [
    dataHe7+'F5_2018_12_17_16.58.52_powersweep_RT_short_blue2/F5_2018_12_17_16.58.52_powersweep_RT_short_blue2.dat',
    dataHe7+'F7_2018_12_17_17.03.43_powersweep_RT_short_blue2_RCfilter/F7_2018_12_17_17.03.43_powersweep_RT_short_blue2_RCfilter.dat',
    dataHe7+'F10_2018_12_17_17.11.26_powersweep_RT_short_blue2_CuPW/F10_2018_12_17_17.11.26_powersweep_RT_short_blue2_CuPW.dat',
    dataHe7+'F13_2018_12_17_17.16.50_powersweep_RT_short_blue2_RC_CuPW/F13_2018_12_17_17.16.50_powersweep_RT_short_blue2_RC_CuPW.dat'
]
```

```python
rfpower = 0
data_all_filters = []
names_all_filters = ['no filter', 'RC only', 'CuPW only', 'RC+CuPW']
```

```python
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
mtx.pmtx
```

```python
fHe7 = data_all_filters[0].index.values
```

```python
[plt.plot(fHe7,vals,label=pwr) for vals,pwr in zip(mtx.pmtx.values.T,mtx.pmtx.columns)]
plt.xscale('log')
plt.legend()
```

```python

names_all_filters
```

# Plot

```python
fig = plt.figure()#figsize=cm2inch(12,8))

plt.plot(RCdata[0],RCdata[3],label='RC filter')
plt.plot(CPdata[0],CPdata[3],label='CP filter')
plt.plot(RCCPdata[0],RCCPdata[3],label='RC + CP')
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line,'--',label=name)
plt.legend()
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|S$_{21}$| (dB)')
plt.tight_layout()
plt.show()
plt.close()
```

```python

```
