# Pypertext

Create HTML elements the Pythonic way.

```python
from pypertext import ht

div = ht.div(id="my-div", classes=["container"], style={"color": "red"})
div + ht.h1("Hello World") + ht.p("This is a paragraph.")
```

## Install

```bash
pip install pypertext
```