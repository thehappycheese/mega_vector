# 1. mega_vector <!-- omit in toc -->

A basic pure python vector manipulation library because I got sick of copy pasting it.

[![PyPI - Version](https://img.shields.io/pypi/v/mega-vector.svg)](https://pypi.org/project/mega-vector)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mega-vector.svg)](https://pypi.org/project/mega-vector)

-----

**Table of Contents**

- [1. Installation](#1-installation)
- [2. Features](#2-features)
  - [2.1. Conversion to String](#21-conversion-to-string)
  - [2.2. Conversion to String with format string](#22-conversion-to-string-with-format-string)
  - [2.3. Conversion to `list` or `tuple` or `dict`](#23-conversion-to-list-or-tuple-or-dict)
  - [2.4. Conversion to `numpy.ndarray`](#24-conversion-to-numpyndarray)
- [3. License](#3-license)

## 1. Installation

```console
pip install mega-vector
```

## 2. Features

### 2.1. Conversion to String

```python
print(Vector3(1,2,0))
```

```text
'❬1.00, 2.00, 0.00❭'
```

### 2.2. Conversion to String with format string

```python
f"{Vector3(1,2,0):>7.3f}"
```

```text
'❬  1.000,   2.000,   0.000❭'
```

### 2.3. Conversion to `list` or `tuple` or `dict`

```python
list(Vector3(1,2,0))
tuple(Vector3(1,2,0))
dict(zip("xyz",Vector3(1,2,0)))
```

```text
[1,2,0]
(1,2,0)
{'x': 1, 'y': 2, 'z': 0}
```

### 2.4. Conversion to `numpy.ndarray`

```python
np.array(Vector3(1,2,0))
```

```text
array([1, 2, 0])
```


## 3. License

`mega-vector` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
