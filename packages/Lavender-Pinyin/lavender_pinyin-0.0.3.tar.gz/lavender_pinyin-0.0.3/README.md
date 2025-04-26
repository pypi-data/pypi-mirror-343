# Lavender-Pinyin

A Python package for obtaining various pinyin representations of Chinese characters.

## Quick Start

Install the package with pip:

```bash
pip install Lavender-Pinyin
```

Import it in your Python scripts:

```python
from lavender_pinyin import *
```

## Functions

| Usage                                  | Description                                                  |
| -------------------------------------- | ------------------------------------------------------------ |
| `pinyin_list(cc, style_name="normal")` | Returns a list of all possible pinyin pronunciations for the given Chinese character `cc`. You can specify the pinyin style by setting `style_name` (default: "normal"). |