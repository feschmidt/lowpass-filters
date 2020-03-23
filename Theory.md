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
\frac{V_{\rm out}}{V_{\rm in}} = \frac{1}{\left(1+i\omega R_1C_1\right)\left(1+i\omega R_2C_2\right)}
\end{align}


```python
%load_ext autoreload
%autoreload 2
```

```python
%run src/basemodules.py
```

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
def myfun(w):
    return S21dB(w,R1,C1,R2,C2)-(-3)
```

```python
f3dB=fsolve(myfun,30e3)/2/pi
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

```python

```
