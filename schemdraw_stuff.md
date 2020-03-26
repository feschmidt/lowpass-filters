---
jupyter:
  jupytext:
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
import SchemDraw
import SchemDraw.SchemDraw.elements as elm
```

```python
d = SchemDraw.SchemDraw.Drawing()

d.add(elm.DOT,lftlabel='V$_1$')

r1=d.add(elm.RES, d='right', label='R$_1$')
c1=d.add(elm.CAP, d='down', label='C$_1$',l=2)
d.add(elm.GND)

r2=d.add(elm.RES, d='right', label='R$_2$', xy=r1.end)
c2=d.add(elm.CAP, d='down', label='C$_2$',l=2)
d.add(elm.GND)

d.add(elm.LINE,d='right',xy=r2.end,l=1)
d.add(elm.DOT,rgtlabel='V$_2$')

d.draw()
d.save('RC_twostage.pdf')
```

```python

```
