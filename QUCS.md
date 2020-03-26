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

```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

# Import qucs data

```python
myfiles = sorted(glob.glob('qucs/*.dat'))
myfiles
```

```python
mysims = {}
for myfile in myfiles:
    name = myfile.split('/')[1].strip('.dat')
    data = stlabutils.utils.readdata.readQUCS(myfile)
    mysims[name]=data
```

```python
mysims.keys()
```

```python
mysims['RC_lowpass'][0].keys()
```

```python
mysims['RC_lowpass'][1]
```

## plot sims

```python
fig = plt.figure(figsize=cm2inch(12,8),constrained_layout=True)
for i,(key,_) in enumerate(mysims.items()):
    if i==0:
        c='C0'
        ls='-'
        label='real, two-stage'
    elif i==1:
        c='C0'
        ls='--'
        label='ideal, two-stage'
    elif i==2:
        c='C1'
        ls='-'
        label='real, single stage'
    else:
        c='C1'
        ls='--'
        label='ideal, single stage'
    plt.plot(mysims[key][0]['indep_acfrequency'],mysims[key][0]['dep_S21dB'],label=label,c=c,ls=ls)
plt.xscale('log')
plt.legend()
plt.ylim(-150,20)
plt.xlabel('Frequency (Hz)')
plt.ylabel(r'$|S_{21}|$ (dB)')
plt.savefig('plots/RCfilter_qucs.png',dpi=1000,bbox_inches='tight')
plt.show()
plt.close()
```

# Fit qucs data

```python
class MyFitter:
    
    def __init__(self,classparams):
        self.bools=[True,True,False,False]
        for key,val in classparams.items():
            setattr(self,key,val)
            
        self.mymodel = lmfit.Model(S21dB)
            
        print(self.mymodel.param_names,self.mymodel.independent_vars)

        self.params = self.mymodel.make_params(R1=self.R1,C1=self.C1,R2=self.R2,C2=self.C2)
        for key,val in self.params.items():
            self.params[key].min=0

        for key,val in zip(['R1','C1','R2','C2'],self.bools):
            self.params[key].vary=val

        print(self.params)
        
    def runfit(self):
        
        self.result = self.mymodel.fit(self.y, self.params, w=2*pi*self.x)

        print(self.result.fit_report())

        print(self.result.params)
        
        return self.result
```

## ideal


### single

```python
x = mysims['RC_lowpass_single_ideal'][0]['indep_acfrequency']
y = mysims['RC_lowpass_single_ideal'][0]['dep_S21dB']
myfitterRCsingleideal = MyFitter({
    'x': x,
    'y': y,
    'R1': 1e4,
    'C1': 4e-9,
    'R2': 0,
    'C2': 0
})
```

```python
result = myfitterRCsingleideal.runfit()
```

```python
result.params
```

```python
plt.plot(x,y,'.',label='data')
plt.plot(x,result.init_fit,label='init fit')
plt.plot(x,result.best_fit,label='best fit')
plt.xscale('log')
plt.legend()
```

### two stage

```python
x = mysims['RC_lowpass_ideal'][0]['indep_acfrequency']
y = mysims['RC_lowpass_ideal'][0]['dep_S21dB']
myfitterRCsingleideal = MyFitter({
    'x': x,
    'y': y,
    'R1': 1e3,
    'C1': 4e-9,
    'R2': 1e3,
    'C2': 4e-9,
    'bools':[True,True,True,True]
})
```

```python
result = myfitterRCsingleideal.runfit()
```

```python
result.params
```

```python
plt.plot(x,y,'.',label='data')
plt.plot(x,result.init_fit,label='init fit')
plt.plot(x,result.best_fit,label='best fit')
plt.xscale('log')
plt.legend()
```

```python

```
