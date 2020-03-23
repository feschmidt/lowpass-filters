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
<div class="toc"><ul class="toc-item"><li><span><a href="#Data-analysis-of-low-pass-filter-measurements-at-room-temperature" data-toc-modified-id="Data-analysis-of-low-pass-filter-measurements-at-room-temperature-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data analysis of low-pass filter measurements at room temperature</a></span><ul class="toc-item"><li><span><a href="#What-does-a-simple-cable-look-like?" data-toc-modified-id="What-does-a-simple-cable-look-like?-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>What does a simple cable look like?</a></span></li><li><span><a href="#What-effect-does-a-filter-have-on-the-transfer-function?" data-toc-modified-id="What-effect-does-a-filter-have-on-the-transfer-function?-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>What effect does a filter have on the transfer function?</a></span></li><li><span><a href="#How-do-all-the-filters-compare-with-each-other-at-medium-frequencies?" data-toc-modified-id="How-do-all-the-filters-compare-with-each-other-at-medium-frequencies?-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>How do all the filters compare with each other at medium frequencies?</a></span></li><li><span><a href="#How-do-all-the-filters-compare-with-each-other-at-low-frequencies?" data-toc-modified-id="How-do-all-the-filters-compare-with-each-other-at-low-frequencies?-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>How do all the filters compare with each other at low frequencies?</a></span></li></ul></li></ul></div>
<!-- #endregion -->

# Data analysis of low-pass filter measurements at room temperature

```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

## What does a simple cable look like?

```python
myfiles = [
    dataHe7+'F1_2018_12_17_16.51.24_powersweep_RT_short_semiflex/F1_2018_12_17_16.51.24_powersweep_RT_short_semiflex.dat',
    dataHe7+'F3_2018_12_17_16.55.48_powersweep_RT_short_blue1/F3_2018_12_17_16.55.48_powersweep_RT_short_blue1.dat',
    dataHe7+'F5_2018_12_17_16.58.52_powersweep_RT_short_blue2/F5_2018_12_17_16.58.52_powersweep_RT_short_blue2.dat'
]
```

```python
rfpower = 0
data_all_cables = []
names_all_cables = ['semiflex', 'blue 1', 'blue 2']
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
    linecut -= linecut.iloc[0]
    data_all_cables.append(linecut)
```

```python
fig, ax = plt.subplots()
for name, line in zip(names_all_cables, data_all_cables):
    plt.plot(line, label=name)
plt.title('Input power: {:.1f} dBm'.format(rfpower))
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('S21 (dB)')
plt.legend(loc='best')
plt.savefig('plots/He7_cable_comparison_Prf_{:.1f}dBm.png'.format(rfpower))
plt.show()
plt.close()
```

## What effect does a filter have on the transfer function?

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
    linecut -= linecut.iloc[0]
    data_all_filters.append(linecut)
```

```python
fig, ax = plt.subplots()
for name, line in zip(names_all_filters[::-1], data_all_filters[::-1]):
    plt.plot(line, label=name)
plt.title('Input power: {:.1f} dBm'.format(rfpower))
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('S21 (dB)')
plt.legend(loc='best')
plt.savefig('plots/He7_filter_comparison_Prf_{:.1f}dBm.png'.format(rfpower))
plt.show()
plt.close()
```

## How do all the filters compare with each other at medium frequencies?

```python
myfiles = [
    dataHe7+'F9_2018_12_17_17.06.20_powersweep_RT_short_blue2_RCfilter_midfreq/F9_2018_12_17_17.06.20_powersweep_RT_short_blue2_RCfilter_midfreq.dat',
    dataHe7+'F17_2018_12_17_17.24.47_powersweep_RT_short_blue2_RC2_midfreq/F17_2018_12_17_17.24.47_powersweep_RT_short_blue2_RC2_midfreq.dat',
    dataHe7+'F19_2018_12_17_17.28.04_powersweep_RT_short_blue3_RC3_midfreq/F19_2018_12_17_17.28.04_powersweep_RT_short_blue3_RC3_midfreq.dat',
    dataHe7+'F21_2018_12_17_17.33.57_powersweep_RT_short_blue3_RC4_midfreq/F21_2018_12_17_17.33.57_powersweep_RT_short_blue3_RC4_midfreq.dat',
    dataHe7+'F23_2018_12_17_17.38.16_powersweep_RT_short_blue3_RC5_midfreq/F23_2018_12_17_17.38.16_powersweep_RT_short_blue3_RC5_midfreq.dat',
    dataHe7+'F25_2018_12_17_17.42.24_powersweep_RT_short_blue3_RC6_midfreq/F25_2018_12_17_17.42.24_powersweep_RT_short_blue3_RC6_midfreq.dat',
    dataHe7+'F27_2018_12_17_17.46.36_powersweep_RT_short_blue3_RC7_midfreq/F27_2018_12_17_17.46.36_powersweep_RT_short_blue3_RC7_midfreq.dat',
    dataHe7+'F29_2018_12_17_17.52.20_powersweep_RT_short_blue3_RC8_midfreq/F29_2018_12_17_17.52.20_powersweep_RT_short_blue3_RC8_midfreq.dat',
    dataHe7+'F31_2018_12_17_17.57.05_powersweep_RT_short_blue3_RC9_midfreq/F31_2018_12_17_17.57.05_powersweep_RT_short_blue3_RC9_midfreq.dat'
]
```

```python
rfpower = 0
data_all_filters = []
names_all_filters = ['RC1','RC2','RC3','RC4','RC5','RC6','RC7','RC8','RC9']
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
    linecut -= linecut.iloc[0]
    data_all_filters.append(linecut)
```

```python
fig, ax = plt.subplots()
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line, label=name)
plt.title('Input power: {:.1f} dBm'.format(rfpower))
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('S21 (dB)')
plt.legend(loc='best')
plt.savefig('plots/He7_RC_all_midfreq_Prf_{:.1f}dBm.png'.format(rfpower))
plt.show()
plt.close()
```

## How do all the filters compare with each other at low frequencies?

```python
myfiles = [
    dataHe7+'F8_2018_12_17_17.04.54_powersweep_RT_short_blue2_RCfilter_lowfreq/F8_2018_12_17_17.04.54_powersweep_RT_short_blue2_RCfilter_lowfreq.dat',
    dataHe7+'F16_2018_12_17_17.23.48_powersweep_RT_short_blue2_RC2_lowfreq/F16_2018_12_17_17.23.48_powersweep_RT_short_blue2_RC2_lowfreq.dat',
    dataHe7+'F18_2018_12_17_17.26.57_powersweep_RT_short_blue3_RC3_lowfreq/F18_2018_12_17_17.26.57_powersweep_RT_short_blue3_RC3_lowfreq.dat',
    dataHe7+'F20_2018_12_17_17.31.50_powersweep_RT_short_blue3_RC4_lowfreq/F20_2018_12_17_17.31.50_powersweep_RT_short_blue3_RC4_lowfreq.dat',
    dataHe7+'F22_2018_12_17_17.37.05_powersweep_RT_short_blue3_RC5_lowfreq/F22_2018_12_17_17.37.05_powersweep_RT_short_blue3_RC5_lowfreq.dat',
    dataHe7+'F24_2018_12_17_17.41.08_powersweep_RT_short_blue3_RC6_lowfreq/F24_2018_12_17_17.41.08_powersweep_RT_short_blue3_RC6_lowfreq.dat',
    dataHe7+'F26_2018_12_17_17.45.30_powersweep_RT_short_blue3_RC7_lowfreq/F26_2018_12_17_17.45.30_powersweep_RT_short_blue3_RC7_lowfreq.dat',
    dataHe7+'F28_2018_12_17_17.49.39_powersweep_RT_short_blue3_RC8_lowfreq/F28_2018_12_17_17.49.39_powersweep_RT_short_blue3_RC8_lowfreq.dat',
    dataHe7+'F30_2018_12_17_17.55.04_powersweep_RT_short_blue3_RC9_lowfreq/F30_2018_12_17_17.55.04_powersweep_RT_short_blue3_RC9_lowfreq.dat'
]
```

```python
rfpower = 0
data_all_filters = []
names_all_filters = ['RC1','RC2','RC3','RC4','RC5','RC6','RC7','RC8','RC9']
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
    linecut -= linecut.iloc[0]
    data_all_filters.append(linecut)
```

```python
fig, ax = plt.subplots()
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line, label=name)
plt.title('Input power: {:.1f} dBm'.format(rfpower))
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('S21 (dB)')
plt.legend(loc='best')
plt.savefig('plots/He7_RC_all_lowfreq_Prf_{:.1f}dBm.png'.format(rfpower))
plt.show()
plt.close()
```

```python
fig, ax = plt.subplots()
for name, line in zip(names_all_filters, data_all_filters):
    plt.plot(line, label=name)
plt.xlim(9e3, 6e4)
plt.ylim(-5, 1)
plt.grid(which='both')
plt.title('Input power: {:.1f} dBm'.format(rfpower))
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('S21 (dB)')
plt.legend(loc='best')
plt.savefig('plots/He7_RC_all_lowfreq_zoom_Prf_{:.1f}dBm.png'.format(rfpower))
plt.show()
plt.close()
```

```python

```
