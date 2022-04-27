# LESPY

[![GitHub stars](https://img.shields.io/github/stars/natanfeitosa/lespy)](https://github.com/natanfeitosa/lespy/stargazers)
[![GitHub license](https://img.shields.io/github/license/natanfeitosa/lespy)](https://github.com/natanfeitosa/lespy/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/lespy.svg)](https://badge.fury.io/py/lespy)
[![PyPI download month](https://img.shields.io/pypi/dm/lespy.svg)](https://pypi.python.org/pypi/lespy/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/lespy.svg)](https://pypi.python.org/pypi/lespy/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/lespy)

## Overview 
A small and robust micro Python framework for building simple and solid web apps.

## Quick start
> DEMO: You can see a working examples [here](./examples).

### Instalation

Via PIP (recommended):

```bash
pip install lespy
```

Via Poetry:
```bash
poetry add lespy
```

Via GitHub:

```bash
git clone https://github.com/natanfeitosa/lespy.git && cd lespy && pip install .
```

### Creating a simple app

In your `main.py` file import the `App` class from `lespy`
```python
from lespy import App
```

Now instantiate the App class and pass it a name
```python
app = App('first_app')
```

Now we need to create a route with the GET method
```python
@app.get('/')
def home(request):
    return 'Hello world'
```

Yes, it's that simple.

### Running the app

**_With the simple server included:_**
> This is a simple implementation, do not use for production environment.

First import the `run` method
```python
from lespy import run
```

Now let's use the method passing the App instance
```python
if __name__ == '__main__':
    run(app)
```

Now, just run our python file, and if everything went well, just access in <http://localhost:3000>.

**_With Gunicorn:_**

```bash
$ gunicorn main:app
```
