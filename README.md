### What is DjScript?

`djscript` is a Python package for using **RapydScript** in your Django application. This package installs NodeJS/npm/RapydScript in an isolated virtual environment and includes utilities for writing RapydScript `*.pyj` files in your web application.

### What is RapydScript?

From the RapydScript README: "RapydScript (pronounced 'RapidScript') is a pre-compiler for JavaScript, similar to CoffeeScript, but with cleaner, more readable syntax. The syntax is very similar to Python, but allows JavaScript as well."

*   Github: <https://github.com/atsepkov/RapydScript>
*   Community: <http://groups.google.com/group/rapydscript>

### Features

*   Convenient `djurl` templatetag for compiling javascript on page load (`settings.DEBUG = True`)
*   Exceptions are logged to `django.request` or custom logger (which can be emailed to admins, etc)
*   Parses Django templatetags before attempting to compile javascript

### Usage

For Django development, there is a convenient `djurl` template tag which will freshly compile your RapydScript on each page request. On production, the static compiled javascript is served directly from your `static/` folder.

```
    # settings.py
    PROJECT_HOME = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_HOME, 'static') + '/'
    STATIC_URL = '/static/'

    DJSCRIPT_PATHS = {
        'path.to.rapydscript.file': 'file.js'
    }
```

```
    # template.html
    {% djurl 'path.to.rapydscript.file' %}
```

Your source file (e.g. *path/to/rapydscript/file.pyj*) must end in the `.pyj` extension. Your target file destination is the value specified in settings.py. Your web server must have correct file permissions to write to your `static/` folder.

### Installation

```
    pip install djscript
```

### Under the hood

*   [RapydScript](https://github.com/atsepkov/RapydScript) pre-compiler for Javascript
*   [virtual-node](https://github.com/elbaschid/virtual-node) for installing [node.js](http://nodejs.org/) in a Python virtualenv.
*   [Django](https://www.djangoproject.com/) web framework