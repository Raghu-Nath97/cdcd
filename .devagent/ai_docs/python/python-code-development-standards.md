# Python Code Development Standards - Basics

This is a Basics version of Code Development Standards - rules described are mandatory for any code to be considered production-ready.

## General guidelines
Make sure to start with an end-vision in mind, as complete as possible.

* It is important to first define the blueprint for application development, before starting actual build process. Note that development comes after experiment.
* Defining a blueprint (application architecture) involves selection of service providers, software tools, estimate resource requirements and evaluate various architecture options listing their pros and cons.
* Need to have clear understanding of the data that will go into the application and how it will be processed by application.
* Define application features and priorities of implementation.
* Important considerations for developing various components of Advanced Analytics include:
  * Number of users expected to use the application.
  * Need for data presentation/visualization for various level of users.
  * Does presentation/visualization require dynamic or static components, or both?
  * Is data processing required as batch, on-demand or streaming?
  * Performance and flexibility required for fulfilling application users needs.
  * Design for scalability and expansion of capability.
  * Advanced Analytics considerably broadens the integration challenge with need to integrate structured and unstructured data. 
  Data virtualization provides a flexible way to perform this integration. 
  Data virtualization is a powerful technique for declaring different logical data structures on underlying physical data.
  * Structure solution environments around analytics, not ad-hoc querying or standard reporting.
* Choose approaches that can be reprogrammed and re-hosted. 
* Consider using a metadata-driven codeless development environment to increase productivity and help insulate you from underlying technology changes (see Configuration file chapter).
* Apply filtering, cleansing, pruning, conforming, matching, joining, and diagnosing at the earliest touch points possible.
* Integrate separate data sources with conformed dimensions.
* Expect to integrate structured and unstructured data.
* Leverage existing shared library of tools and scripts (DE Coding Library IN DEVELOPMENT).

Whenever code is auto-generated, make sure that the final form, which is being executed, is written to a file (logged) for debugging purposes.

## Software maintenance
↑ back to top

In order to ensure highest possible software standards compliance and quality, significant amount of effort must be focused around code maintenance activities. 
Said activities mainly operate around functionality enhancements and defects fixing.

### Code repository
GitHub.

Git (GitHub) is a P&G choice of VCS for tracking changes in source code during software development. For DE/DS projects, it's required to leverage P&G Organization on GitHub which supplements raw Git with functionalities like: code hosting, change tracking, issue management, code reviews platform, CI/CD and documentation platform (GFM). Application code should reside in GitHub repository dedicated particularly for this app/project, under ownership of procter-gamble organisation.

For more guidelines and detailed information on this topic, refer to 
HWR-CT - Collaboration Tools and Best Practices.

### Documentation
When sharing code - quickstart matters first.

Every production application code should be properly documented using GitHub markdown. Documentation file (README.md) should be located in project GitHub repository, and cover topics like application quickstart guide for users/developers. When designing such document, please keep in mind KISS principle, as you would normally do when developing an application. Code technical documentation should follow "just barely good enough (JBGE)" rule, which means we should aim for "just enough documentation" for properly described application.

For Markdown syntax, refer to this 10 minute interactive tutorial which explains the basics. For complete explanation of GFM (GitHub Flavoured Markdown), reach out to GitHub Markdown Documentation.

## Coding standards and best practices

Dos and don’ts of code development.

This section covers development standards and best practices for production code. Currently designed with Python code in mid, while vast majority of rules is applicable to all common programming languages. 
Inspired by PEPs / Google Python Style Guide / The Hitchhiker’s Guide to Python / Real Python and community focused around Python software development.

## KISS

Keep it simple, stupid!

Common problem among today's software engineers and developers is that they tend to overcomplicate things, especially when it comes to advanced projects. Typical approach to programming is to break down problem we're facing into smaller, understandable pieces that are easy to implement. Common mistake is those pieces not being small enough to produce simple code, which leads complex implementations of even simplest problems, often in a form of spaghetti code. KISS principle helps to avoid those problems and produce robust software. At the same time, it doesn't require exceptional programming skillset to follow, which makes it easy to implement by anybody who writes code, regardless of skills and experience.

Following are main rules to deliver simple code:
* Keep your functions/methods and classes small - ideally 50 line each. If it’s growing bigger - consider splitting it.
* Solve the problem, then code it. Not the other way around.
* Refactor your code on regular basis to maintain its integrity.
* If you realise additional exception cases to your original solution, most probably it's time to break this module down.
* Keep everything in your code as simple as you can - it's hard, but practice makes perfect.
* If you're looking for more in-depth guide on how to implement KISS into your daily coding routine, or some info how will you benefit from following KISS principle, refer to Apache Foundation document on KISS.
* For Python version of general design guidelines, check The Zen of Python (also known as PEP20).
* Try `import this` in Python console.


## The Zen of Python

### Python version

Use the newest productionalized version you can.

Python runtime choice - rationale
This guide is written with Python 3+ in mind. When choosing a Python interpreter to use, it’s recommended to use the newest Python 3.x given that it’s compatible with external libraries required for your task. 
Every version brings new and improved standard library modules, security and bug fixes. Selecting the newest version with Maintenance status:security is usually a best choice (check the maintenance status at Download Python).

Having above as general rule of thumb, there’s also another factor that’s gaining importance recently - compatibility with P&G internal ecosystems/tools/platforms, like for instance AI Factory (aifactory.pg.com). Those platforms will often require specific Python version to ensure full support and compatibility. With AI Factory in mind, Python version recommendation is as follows:

| Current Python standard | Next standard |
--------------------------| --------------|
| 3.11 for most Python applications | |
| 3.10 for AI Factory (during transition to 3.11) | 3.12 not supported yet (to be added by OND’25) |

Why not Python 3.12+?
We’re aware of some compatibility problems occurring exclusively on runtimes 3.12+. Those usually surface for projects using older dependencies versions (but still a valid ones). Prioritize use of officially supported Python runtimes (3.9 - 3.11).

### Python 2.X runtimes
If your app still uses Python 2, consider migrating immediately migrate to 3.x, as Python 2 support officially stopped January 1 2020. 
To make sure you’re ready to go with Python 3 - check it on Can I Use Python 3?.

NOTE: This guide uses and recommends (by giving example) using f-Strings for string formatting.
f-Strings were introduced in Python 3.6 (via PEP498).


## Code layout/style (flake8)

Use and follow python-pod flake8 setup.

Proper structure is a key factor in code intelligibility and maintainability. Well-structured and advised software is easier to evolve and modify, doesn't require programmer to ask what author had in mind? every now and then when going through lines of code. In global projects its importance is highlighted even further. Below is the set of generic rules on how majority of code should be structured.

If you’re joining project with existing codebase, take a few minutes to learn its style and adapt to it - consistency is more important than blindly following rules.
As PEP8 states:
```
Consistency with this style guide is important. 
Consistency within a project is more important. 
Consistency within one module or function is the most important. 

However, know when to be inconsistent - sometimes style guide recommendations just aren't applicable. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!
```

#### Indentation
Use 4 spaces as indentation string.

#### Maximum line length
Consistency is the key.

Main rule here is to stay consistent within project codebase, keeping unified max line length for both code and docstrings.

Depending on scenario:
* joining existing project - obey rules applied by founders
* starting new project - align with team on max length (in range 80-120) and stick to it

When trying to reduce line length, try to split line into atomic operations, or wrap expressions into parentheses.
Ensure proper indentation of continued lines

It’s ok to violate line length rule for:
* URLs
* pathnames

atomic - in this context means “not splittable in parts”. 
It’s also referred to in thread synchronization mechanisms where the definition is more complicated.

It's ok:
```python
calc_engine = SomeLongCalculationEngineClassName()
calc_result = calc_engine.some_long_get_calculation_method_of_engine_class()
print(f'Result of a calculation is {calc_result}')
```

It's not ok:
```python
print(f'Result of a calculation is {SomeLongCalculationEngineClassName().some_long_get_calculation_method_of_engine_clas()}'
```

#### Indentation when breaking line
When indenting broken line, you can align elements either:
* vertically
* using single indentation string (4 spaces) - if first line ends with open parenthesis/bracket

```python
answer = (f'For circle of radius {radius}, accurate area'
          f'is {accurate_area} and simplified is {simplified_area}')
result = some_function_name(
    var_one, var_two, var_three,
    var_four)
```

#### Semicolons
Don’t.

Don’t use semicolons - neither for line ending, nor for accumulating multiple statements in one line. They damage code readability and give nothing worthy in return.
Generally - use one statement per line.

#### String quoting
Consistency, again.

Similarly to PEP8, this guide doesn’t make a recommendation for here. Pick a rule and stick to it - it improves readability. When a string contains single or double quote characters, however, use the other one to avoid backslashes in the string.

Use “““triple-double quoting””” for docstrings. 

```python
"""Examples of string quoting."""
user = 'trojak.r'
issue = "Can't stop the coding"
resolution = """Try to replace coding with:
             - cooking
             - sports
             - hard math problems
             """
```

NOTE:
* ‘Single quotes’ allow un-escaped embedding of '“double quotes”'.
* ”Double quotes” allow for embedding of un-escaped "'single quotes'”.
* It’s claimed most Pythonic to use 'single quotes' until you need double quotes.

#### Whitespaces
Use whitespaces:
* after a comma(,) or colon(:)
* around binary operators: =, ==, <, >, !=, <>, <=, >=, in, not in, is, is not, and, or, not

Don’t use whitespaces:
* inside (parentheses), [brackets] or {braces}
* before a comma(,), semicolon(;), or colon(:)
* before the open paren/bracket that starts an argument list, indexing or slicing
* around keyword / parameter equals - def func(value=5):, not def func(value = 5):

Use as you prefer/consider best:
* around arithmetic operators: +, -, *, /, //, %, **, @ - with intention to clarify the expression

NOTE: No need to remember these rules - pip install flake8 and it will point out all misplaced whitespaces

It's ok:
```python
laundry_products = ['ariel', 'tide']
laundry_product = laundry_products[0]
print(laundry_product)
```

It's not ok:
```python
laundry_products=[ 'ariel' ,'tide' ]
laundry_product=laundry_products [ 0 ]
print ( laundry_product )
```

NOTE: Bad code above generates 12 warnings in flake8. Can you manually point all of them?

#### Imports
Always on top of module. Use 3 sections -  stdlib, third party and local imports.

Always import at the top of the file, right after module docstring and __all__ attribute.

Imports should be grouped, with the order being:
* imports from standard Python lib (Stdlib)
* imports from  third party libraries
* imports from local code repository

With below rules applied:
* Never do from library import *, always import explicitly.
* Within a group, do non-from imports before from imports.
* Import exactly one module per non-from import line.
* Names imported from one source in should appear in one from import statement.
* Non-dotted imports first, dotted imports follow.
* Use from module import module as mdl if:
  * two modules named module are to be imported
  * module is an inconveniently long name
* `import module as mdl` when mdl is a standard abbreviation (e.g., np for numpy).

Example 
main.py
```python
"""Example of good import statement styling."""
__all__ = []
# Stdlib imports
import copy
import socket
# Third party imports
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
# Local code repository imports
from mailman import public
from mailman.interfaces.mta import IMailTransportAgentDelivery
from mailman.mta.connection import Connection
from zope.interface import implementer
```

#### Blank lines
Separate line blocks for easy scanning through code.

Proper usage of blank line improves code readability. It's encouraged to follow PEP8 rules here. Below's a quick summary of them.

When following below rules, try to also reduce vertical whitespace in your code. 
When separating logical sections of code, consider adding comments explaining said sections purposes.

| Between | Blank lines | 
| --------|-------------|
| any top level code block (functions, classes)| 2 | 
| methods in class | 1 |
| class declaration and it's first method | 1 (after class docstring) or 0 | 
| class/method declaration and it's docstring | 0 |
| groups of related functions| 2 |
| logical sections of code within one function | 1 |

Example
sharepoint_plugin.py
```python
"""Module for sharepoint file management."""
__all__ = ['SharepointSiteFile']
import io
import requests
from os import path
from urllib.parse import urljoin
from shew.auth import SPAuth
class SharepointSiteFile():
    """Class for managing file hosted on Sharepoint site."""
    def __init__(self, username, password, host_name, site, file_path):
        """Create object for managing file hosted on Sharepoint.
        Args:
            username: Sharepoint username.
            password: Sharepoint password.
            host_name: Host address.
            site: Sharepoint site address.
            file_path: Path to file.
        """
        self._username = username
        self._password = password
        self._host_name = host_name
        self._site = site
        self._file_path = file_path
    def sharepoint_bytesIO(self):
        """Return BytesIO object of Sharepoint file."""
        # Preparing variables.
        url = urljoin(self._host_name, urljoin('sites/', self._site))
        folder, doc = path.split(self._file_path)
        # Running Sharepoint session.
        sp_session = requests.Session()
        sp_session.auth = SPAuth(self._host_name, self._username, self._password)
        response = sp_session.get(url, stream=True)
        if response.status_code != 200:
            raise Exception(response.json())
        else:
            response_io = io.BytesIO(response.content)
            return(response_io)
```

## Configuration file


Parametrize static and/or re-used elements of your code. Especially those that differ between runtime/env.

The more advanced and complex application is, the stronger its need for a properly structured configuration. For simple tasks it may be working out to keep it embedded between lines of code, but it's neither the safest, nor most elegant way to handle application settings - especially when working with VCS. To exclude local configuration file from being committed every time with rest of application code, as it's usually only serviceable when personalized, use .gitignore file. Having separate configuration file will make it much easier to maintain changing app settings and fixed values used across runtime (e.g., URLs, parameters, binary switches).

Configuration file can be structured in variety of formats, depending on its content and used programming language. In Python, most popular formats include INI, JSON, YAML, XML and Python itself. One provides functionality that others lack, so it's up to programmer which one will be leveraged. 

Below are 2 examples for configuration files and how to read them in Python, witch some descriptive comments. 


* INI
Example
config.ini
```ini
[GLOBAL]
VERSION = 1.0
NAME = Loretta

[CREDENTIALS]
LOGIN = trojak.r

[BOOLEAN_EXAMPLES]
EX1 = 1
EX2 = yes
EX3 = true
EX4 = on
EX5 = 0
EX6 = no
EX7 = false
EX8 = off

[COMPOUND]
APP_FULL_NAME = ${GLOBAL:NAME}_${GLOBAL:VERSION}
```

usage.py
```python
# 1. Import required libraries
from configparser import ConfigParser, ExtendedInterpolation

# 2. Create a ConfidParser object and read config file
#    Notice that 'interpolation' keyword argument is only needed for step example 10
my_config = ConfigParser(interpolation=ExtendedInterpolation())
my_config.read('./config.ini')

# 3. Get all sections available in config file
print(my_config.sections())

# 4. Get all options in GLOBAL section
print(my_config.options('GLOBAL'))

# 5. Get value of specific config item - LOGIN from CREDENTIALS section
print(my_config.get('CREDENTIALS', 'LOGIN'))

# 6. Check of CREDENTIALS is an existing section in config file
print('CREDENTIALS' in my_config)

# 7. Read app version as string (default)
app_version = my_config.get('GLOBAL', 'VERSION')
print(app_version, type(app_version))

# 8. Read app version as float
app_version = my_config.getfloat('GLOBAL', 'VERSION')
print(app_version, type(app_version))

# 9. Get value, use fallback when not found in config file
print(my_config.get('GLOBAL', 'NAME', fallback='Charlotte'))
print(my_config.get('GLOBAL', 'SECOND_NAME', fallback='Charlotte'))

# 10. All possible boolean inputs for INI config
print(
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX1'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX2'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX3'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX4'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX5'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX6'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX7'),
    my_config.getboolean('BOOLEAN_EXAMPLES', 'EX8')
)

# 11. Read compound config item
print(my_config.get('COMPOUND', 'APP_FULL_NAME'))
```

* JSON

config.json
```json
{
    "GLOBAL":{
        "VERSION":"1.0",
        "NAME":"Loretta"
    },
    "CREDENTIALS":{
        "LOGIN":"trojak.r"
    }
}
```

usage.py
```python
# 1. Import required library
import json

# 2. Read config file
with open('./config.json') as config_file_json:
    my_config_json = json.load(config_file_json)

# 3. Get all sections available in config file
print(my_config_json.keys())

# 4. Get all options in GLOBAL section
print(my_config_json['GLOBAL'].keys())

# 5. Get value of specific config item - LOGIN from CREDENTIALS section
print(my_config_json['CREDENTIALS']['LOGIN'])

# 6. Check of CREDENTIALS is an existing section in config file
print('CREDENTIALS' in my_config_json)

# 7. Read app version as string - no built-in parse methods for JSON
app_version = my_config_json['GLOBAL']['VERSION']
print(app_version, type(app_version))

# 9. Get value, use fallback when not found in config file
#    Note that it's only possible to use fallback in get() method, which required unnested config item
app_version = my_config_json['GLOBAL']
print(app_version.get('NAME', 'Charlotte'))
print(app_version.get('SECOND_NAME', 'Charlotte'))
```

## Environment variables
Information about what environment you are in is not configuration, but requires separation, too.

When working in a dev/prod separation - which we should always do - it is prudent to keep environment specifics, like database or proxy addresses, logging levels or API keys in the environment variables.

Many of our deployment technologies like containers or pipelines allow for variables that describe the runtime environment to be accessed or defined separate from application configuration files.

The simplest way to read and set environment variables in python is through the os.environ dictionary:


```python
import os
# read an environment variable
my_api_endpoint = os.environ.get("API_ENDPOINT")  # can also be read by os.environ["API_ENDPOINT"]
# set an environment variable
os.environ["LOGLEVEL"] = "DEBUG"
```
Writing environment variables from your code can be dangerous, if you are overriding something already set, or can be irrelevant as you already have to have the value of the variable in your code to be able to set it.

A generic way to set environment variables for python code is using the python-dotenv module. Unfortunately, it has on pypi a clone that is usually used instead of the correct one because of naming.

A .env file contains environment variables as key-value pairs, like so:
```ini
API_ENDPOINT=https://application.pg.com/api/dev/
LOGLEVEL=DEBUG
```
After installing the package by adding it to requirements.txt and running pip install -e . you can use it in your workflow, like this:
```python
import os
from dotenv import load_dotenv
load_dotenv("{path_to_dotenv_file}")  # can be left empty, read documentation https://github.com/theskumar/python-dotenv
api_endpoint = os.environ.get("API_ENDPOINT")
loglevel = os.environ.get("LOGLEVEL")
```

Make sure, that .env is always in .gitignore before you add the file to your repository!

## Default argument values
Calling your function with the same static argument 90% of cases? Make it a default one.

Whenever you create a function that uses default values, but on rare occasions you want to override them - use default argument values. This way you’ll avoid implementing functions dedicated for those rare exception cases. This is Python way of ‘imitating’ overloading mechanism (known from other languages).

default_argument_values.py
```python
"""Module for default argument values showcase."""
__all__ = ['calc_circle_area']
import math
def calc_circle_area(radius, pi=math.pi):
    """Return area for circle of given radius.
    Args:
        radius: Circle radius.
        pi (optional): Value of pi to use in calculation.
    """
    return pi * radius**2
```

main.py
```python
"""Module for running default argument values showcase."""
from default_argument_values import calc_circle_area
if __name__ == '__main__':
    radius = 4
    accurate_area = calc_circle_area(radius)
    simplified_area = calc_circle_area(radius, 3.14)
    print(f'For circle of radius {radius}, accurate area'
          f'is {accurate_area} and simplified is {simplified_area}')
```

console output
```text
python main.py
For circle of radius 4, accurate areais 50.26548245743669 and simplified is 50.24
```

## Main function
Single starting point on others way to understand your code.

For any algorithm, embed highest-level execution calls in main.py module (or similar). This way, you clearly instruct others - “Hey - if you want to understand my code, here’s where you start”.

If your module has any top-level code (i.e. code that gets executed when you call the module as executable, for instance: python module.py), it should check if __name__ == '__main__' before executing your main program so that the main program is not executed when the module is imported.

module.py
```python
"""Example module."""
__all__ = []
def main():
    pass
if __name__ == '__main__':
    main()
```

## Code modularity
Module, class, function - all should have one, clear purpose. Purpose definition differs between them.

Split your code into independent modules focused around functions offered by them, and treat modules as service providers. Typical module length should be ~150 lines. 
In general, there should be one class per module, with exceptions for auxiliary classes that are heavily-binded to their respective main classes from the same module.

List everything that's meant to be exported from module in `__all__` so that `from module_name import *` imports only names explicitly exposed to public - even though from module import * is discouraged in production code, it may come handy during development and/or interactive sessions. `__all__` provides a clear information on what’s exported from a module (or package, if located in `__init__.py`). What’s more, `__all__` provides a convenient point of reference to what’s public within a module.

Always explicitly decide on module attributes publicness - use `__all__ = []` if module is entirely private.

This convention supersedes `_leading_underscore` which was previously used for non-public attributes - but it’s ok to use both, as `_leading_underscore` will be useful in static code checks, highlighting unauthorised access to private name. 

When attribute name conflicts with reserved keywords (e.g. class, print) use prefix/suffix instead of leading/trailing underscores (math_class, print_status).

NOTE: Module level "dunder names" (i.e. special attributes with two leading and two trailing underscores) such as `__all__`, `__author__`, `__version__`, etc. should be placed after the module docstring, before any import statements.

Consider following example of module containing 3 classes (I used example names here: PrimaryClass, HelperClass and UtilityClass) among which only one is meant to be used outside of primary_class.py - `__all__` declaration does the necessary work here.

Code has been enriched with some comments for better understanding + control prints in class constructors.

primary_class.py
```python
"""Module that offers some functionality.
Or at least would, normally. In this case, it only serves as example.
"""
__all__ = ['PrimaryClass']
class PrimaryClass(object):
    """Class for doing some stuff."""
    def __init__(self):
        """Construct class object using helpers."""
        self._main_helper = _HelperClass(1)
        self._secondary_helper = _HelperClass(2)
        self._utility_heper = _UtilityClass()
        print('Primary class constructor')
class _HelperClass(object):
    """Helper class to PrimaryClass.
    Attributes:
        id: Object id number.
    """
    def __init__(self, id):
        """Construct an object of specified id.
        Args:
            id: Object id number.
        """
        self._id = id
        print(f'Helper class constructor, id: {self._id}')
    def helper_method(self):
        """Do this and that."""
        pass
class _UtilityClass(object):
    """Class providing some utility."""
    def __init__(self):
        # Docstring not needed here as it's obvious.
        print('Utility class constructor')
    def utility_method(self):
        """Do some utility actions."""
        pass
    def another_utility_method(self):
        """Do some other utility actions."""
        pass
```

main.py
```python
"""Module for running modularity chapter example."""
# Don't use 'import *' in production code! Always import explicitly.
from primary_class import *
def main():
    primary_app_class = PrimaryClass()  # works fine
    helper_app_class = _HelperClass(3)  # throws NameError
if __name__ == "__main__":
    main()
```

console output
```
python main.py
Helper class constructor, id: 1
Helper class constructor, id: 2
Utility class constructor
Primary class constructor
Traceback (most recent call last):
  File "main.py", line 9, in <module>
    main()
  File "main.py", line 6, in main
    helper_app_class = HelperClass(3)  # throws NameError
NameError: global name 'HelperClass' is not defined
```

You can also use dir() (built-in Python function) to check what names are defined within a module, without looking into source code. Please note difference between defined names and names exposed to public (__all__):
```
>>> import primary_class
>>> dir(primary_class)
['HelperClass', 'PrimaryClass', 'UtilityClass', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__']
>>> primary_class.__all__
['PrimaryClass']
```

## Naming convention
Name objects clear and precise.

### Code objects
General idea of having proper naming convention is to ensure software comprehension within projects, so people joining existing project will ‘feel like home’ (or at least not confused). Naming objects is where programmers are given significant dose of freedom, which unsupervised may lead to degradation of source-code understanding and readability. In fact, there are 2 popular, alternative approaches used for composing multi-word identifiers: underscore_casing and camelCasing. This section recommends naming rules that are a combination of them.

Good name should be:
* clear - obvious to see what it refers to
* precise - obvious to see what it doesn't refer to

Do not define variables/classes/functions named I, O, or l as they can be very hard to read and distinguish between. Generally - avoid one-letter names.

Do not use Python ‘built-in’ identifiers for naming objects (variables, functions, classes, parameters, etc.). It will cause them to override builtins and lead to unexpected code behavior.

It's clear that objects name should be descriptive enough to explain its content. However, making a sentence out of name is a dreadful idea as well. 

Overly-extended identifiers may:
* lower clarity of code
* make it hard to visually scan modules
* obscure importance of arguments lists (e.g., of classes, methods)
* annoy programmer who needs to use them repeatedly
* generate huge expression chains

When deciding on name, omit words that:
* are obvious given a variable’s or parameter’s type
* don’t disambiguate the name
* are known from the surrounding context
* don’t mean much of anything

For DE/DS projects, it's recommended to follow convention introduced by PEP8. Below's a quick look at it's core takeaways:

| Object type | Naming rule | Name example
|-------------|-------------|--------------
| Package/Module | all-lowercase w/ underscores | module_name.py
| Class | CamelCase | class ClassName(object)
| Variable | all-lowercase w/ underscores | my_variable
| Constants | all-uppercase w/ underscores| CONSTANT_VALUE
| Instance method | all-lowercase w/ underscores | def instance_method(self):
| Class method | all-lowercase w/ underscores | @classmethod<br>def class_method(cls):
| Static method | all-lowercase w/ underscores | @staticmethod<br>def static_method():

as well as some example code for reference:

module_name.py
```python
"""Module for naming convention showcase."""
__all__ = ['ClassName']
class ClassName(object):
    """Class with example name."""
    def __init__(self, purpose='Example'):
        self._class_purpose = purpose
        print(f'Initializing {self._class_purpose} class instance')
    _class_origin = 'P&G'
    def instance_method(self):
        """Print object metadata."""
        print(f'This objects class purpose is: {self._class_purpose}, '
              f'and origin is: {ClassName._class_origin}')
    @classmethod
    def class_method(cls, purpose):
        """Return ClassName object of given purpose.
        Args:
            purpose: Purpose of object.
        """
        return cls(purpose)
    @staticmethod
    def static_method(message):
        """Print message passed to it.
            Args:
            message: Message to be printed.
        """
        print(f'Message passed: {message}')
```

main.py
```python
"""Module executing naming convention showcase."""
from module_name import ClassName
def main():
    my_object = ClassName()
    my_object.instance_method()
    other_object = ClassName.class_method('Other example')
    other_object.instance_method()
    ClassName.static_method('Yet another example')
if __name__ == "__main__":
    main()
```

console output
```
python main.py
Initializing Example class instance
This object's class purpose is: Example, and origin is: P&G
Initializing Other example class instance
This object's class purpose is: Other example, and origin is: P&G
Message passed: Yet another example
```

### Data objects
Production applications and the enterprise layer of production data feeds MUST conform to the P&G Data Naming Convention. It makes models easier to read, support and share. This is based upon uxHive Naming Convention.

NOTE: When ‘producing’ new data as a calculation/transformation result, obey below rules. If sourcing from enterprise-level P&G source, keeping source naming convention is ok.
Keep consistency within data object first, then module/project.

According to DataVercity,  proper data modeling can reduce the development cost by 70%.

### General principles

* Names must be unambiguous, meaningful, self-documenting and concise.
* Words should be written in lowercase and separated by underscores.
* Singular noun or noun phrases should be used over plural (e.g. event not events).
* Use United States English spelling (e.g. color not colour).
* Use abbreviations to create shorter, yet useful names under the following conditions:
  * abbreviations must by understandable, use the full name when in doubt
  * limit the number of word abbreviations to the most commonly used (e.g. ID)
  * follow economy principle (long and/or very often used words are the best candidates for shortening)
  * avoid abbreviating short words (e.g. u for unit) or which saves just few letters (e.g. sttus for status)
  * use first letters (e.g. MM for Market Measurements)
  * do not use a widely used abbreviation for your specific purpose (e.g. IT for Inventory Target).
* Names and abbreviations should be used consistently with and across the datasets/projects.

Column specific principles

Attributes consist of optional subject words & qualifiers (attribute categories), mandatory class and function words:

| Attribute name | Comment | Qualifiers | Class | Function
|---------------|---------|-------------|-------|---------
| user_id | Unique identifier of the user | - | user | id
| prod_categ_name | Name of the product category | prod | categ | name
| order_amt | Total monetary value of the order | - | order | amt

 

Common attribute function types:

* id (unique identifier), name (attribute name), code (known domain of values)
* measurements function words: amt (monetary amount), qty (quantity), cnt (count), pct (percent), rate, factor
* time attributes: date (date), datetm (date and time), tmstp (timestamp)
* descriptive function words: desc (description), cmmnt (comment), label, txt
* other: flag (binary value), lvl (hierarchy level), val (value)

### Comments
```
Code tells you how.
Comments tell you why.
```
~Jeff Atwood
Stack Overflow co-founder, Coding Horror author


There are few things programmer can do to make his code easy for others (and/or future himself) to understand - follow a uniform naming convention, properly organize code and obviously - use descriptive and well structured comments. 
One can use comments/strings in multiple ways - defining module/class/function-level docstrings or simply use one-liners explaining particular block/line of code. 
Both mentioned forms are accepted and desirable, both need to follow conventions to remain clean and serve their purpose effectively.

It's recommended to use comments for:
* explaining particular (complicated) block/line of code
* outlining function algorithm
* tagging - label specific sections of code
* overall support of your code

but never use comments to:
* hide 'smelly code'
* state something that's obvious from the code itself
* “versioning” the code (e.g., commenting out “old” versions)
* toggle on/off blocks of code per execution needs

NOTE: If you’re spending too much time explaining what you did, then you need to go back and refactor to make your code more clear and concise.

 

#### Standard comments
Short explanation of specific line/block of code.

Insert space between # and comment contex.
Comments should always be complete sentences, with proper capitalization and full stops at the end.

It's ok
```python
# If you don't commit, changes won't persist in db.
db_connection.commit()
```
```python
db_connection.commit()  # If you don't commit, changes won't persist in db.
```

It's not ok
comment that re-phrases code content
```python
# Commiting actins to db using commit().
db_connection.commit()
```

bad whitespace usage
```python
db_connection.commit() #If you don't commit, changes won't persist in db.
```

maximum line length violation
```python
db_connection.commit()  # Some long comment that violates maximum line length and should be definitely put above the line.
``` 

#### Multi-line comments
Elaborate explanation (when needed).

Multi-line commenting is not natively supported in Python, like it is in other languages. There are ways to imitate this mechanism - you can either comment out every consecutive line using #, or use triple-quote """. The latter cause confusion with docstring and can be misleading for others reading your code, so use the first method, as it's the only way to get true multi-line comments in Python that get ignored by parser.

It's not ok
```python
# Good example of multi-line comment.
# Immediately suggests it's purpose.
# Ignored by parses, doesn't allocate memory. 
    # Indentation doesn't matter.
```

It's not ok
```python
"""Bad example of multi-line comment.
Can be mistaken with docstring.
Allocates memory, unlike # comments.
You also need to make sure it's intended well.
"""
```

NOTE: Triple-quote comments are in fact multi-line strings. When used as presented above, are saved to runtime memory, but not assigned to any identifier.

#### TODO comments
Python built-in to-do list.

Use TODO comments to communicate to others (or future you) that something in code is not perfect yet and you plan to address it in future. 

```python 
# TODO(trojak.r): Split this function as it grew too much.
```

#### Docstrings
Document reusable and/or public code. For others, or future yourself.

Docstring is a string, unassigned explicitly to any variable, placed within `"""triple-double quotes"""`.
Docstring documents particular module/function/class/method and is its first statement. Python interpreter assign its value to `__doc__` attribute of respective object.
A function docstring should give enough information to write a call to the function without reading the function’s code.

It's required that every public module/function/class/method has a docstring, unless really obvious/simple/self-explanatory from code. Package docstring should be placed in `__init__.py` module.

Few additional rules for docstrings:
* one-line docstring - open and close quotes within the same line.
* don't use blank lines before or after docstring (with exception for class docstring - use one after)
* capitalise docstring and end it with a period


docstring_example.py
```python
"""This is a module docstring."""
__all__ = ['DocstringExample']
class DocstringExample(object):
    """This is a class docstring.
    Methods:
        filter_categories: Filter data leaving only specified categories.
    """
    def __init__(self):
        # Extra simple constructor - no docstring needed
        print('An object is being made.')
    def filter_categories(self, channel_data, categories):
        """Filter data leaving only specified categories.
        Args:
            channel_data (pandas.core.frame.DataFrame): POS channel data.
            categories (list): Categories for processing.
        Returns:
            data_filtered (pandas.core.frame.DataFrame): Data of specified categories.
        """
        data_filtered = pd.DataFrame()
        for cat in [cat for cat in channel_data.Category.unique() if cat in categories]:
            cat_data = channel_data[channel_data.Category == cat]
            data_filtered = pd.concat([data_filtered, cat_data], axis=0)
        return data_filtered
```


main.py
```python
"""Module for docstrings showcase."""
__all__ = []
from docstring_example import DocstringExample
def main():
    myDocstringClass = DocstringExample()
    print(DocstringExample.__doc__)
if __name__ == "__main__":
    main()
```

console output
```
python3 main.py
An object is being made.
This is a class docstring.
```

Most probably recommended style for docstrings will be Google Style or reST, hence its use in this guide examples.
There's a plan to use documentation generator (e.g., Docutils/Sphinx, pydoc) for Python code, but first it's required to ensure proper implementation of docstrings across projects.

| Docstring of: | Should contain: (besides summary line and optional elaborate description)
|------|-----|
| Stand-alone script | Quick reference of script, covering its usage syntax.
| Package | List of names exported by package.
| Module | List of names exported by module. (already in __all__)<br>Example of module usage.
| Class | Summary of class behavior<br>List of names exported by class (i.e. public methods and attributes).<br>Verbs override and extend when implementing inheritance.
| Function/Method | Summary of the function behavior.<br>List of arguments (also optional and keyword), returns, effects and exceptions raised.


##### Multi-line docstring

More descriptive docstring can be spread over multiple line - it should have summary line + blank line + detailed description structure and keep consistent level of indentation.
Place """opening quotes in the first line along with summary. Closing quotes should be in separate line.

```python
"""Docstring summary line.
Detailed description with further elaboration on details. Notice the blank
line above that separates this and summary line above.
"""
# Blank line is mandatory after multi-line docstring. Code should continue here.
```

NOTE: If needed, use `r"""raw docstring"""` and/or `u"""unicode docstring"""` per your best judgment.


## Code snippets collection

How to do specific things in pythonic way. 

Below is a set of specific low-level actions implementations - feel free to provide your own snippets to be posted here! As the collection will grow, it will be properly categorized.

Testing flags
```python
# Different ways to test multiple
# flags at once in Python

x, y, z = 0, 1, 0

if x == 1 or y == 1 or z == 1:
    print('passed')

if 1 in (x, y, z):
    print('passed')

# These only test for trueness:
if x or y or z:
    print('passed')

if any((x, y, z)):
    print('passed')
```

Getting value from dictionary + default value
```python
# The get() method on dicts
# and its "default" argument

name_for_userid = {
    382: 'Alice',
    590: 'Bob',
    951: 'Dilbert',
}


def greeting(userid):
    return(f'Hi {name_for_userid.get(userid, "there")}!')

>>> greeting(382)
'Hi Alice!'

>>> greeting(333333)
'Hi there!'
```

Namedtuple - quick&dirty imitation of class
```python
# Why Python is Great: Namedtuples
# Using namedtuple is way shorter than
# defining a class manually:
>>> from collections import namedtuple
>>> Car = namedtuple('Car', 'color mileage')

# Our new "Car" class works as expected:
>>> my_car = Car('red', 3812.4)
>>> my_car.color
'red'
>>> my_car.mileage
3812.4

# We get a nice string repr for free:
>>> my_car
Car(color='red' , mileage=3812.4)

# Like tuples, namedtuples are immutable:
>>> my_car.color = 'blue'
AttributeError: "can't set attribute"
```

Unpacking tuples and dicts into function arguments
```python
# Function argument unpacking

def myfunc(first: int, second: int, third: int) -> None:
    print(first, second, third)

tuple_vec = (1, 0, 1)
dict_vec = {'first': 1, 'third': 1, 'second': 0}

>>> myfunc(*tuple_vec)
1, 0, 1

>>> myfunc(**dict_vec)
1, 0, 1

# The reverse is also possible
def magic_print(**kwargs) -> None:
    for k, v in kwargs.items():
        print(k, v, sep=": ")
        
>> magic_print(first=1, second=0, third=1)
first: 1
second: 0
third: 1

```

In-place value swapping
```python
# In-place value swapping

# Let's say we want to swap
# the values of a and b...
a = 23
b = 42

# The "classic" way to do it
# with a temporary variable:
tmp = a
a = b
b = tmp

# Python also lets us
# use this short-hand:
a, b = b, a
```

Comparing objects
```python
# "is" vs "=="

>>> a = [1, 2, 3]
>>> b = a

>>> a is b
True
>>> a == b
True

>>> c = list(a)

>>> a == c
True
>>> a is c
False

# • "is" expressions evaluate to True if two 
#   variables point to the same object

# • "==" evaluates to True if the objects 
#   referred to by the variables are equal
```

Functions - Python first-class citizen
```python
# Functions are first-class citizens in Python:

# They can be passed as arguments to other functions,
# returned as values from other functions, and
# assigned to variables and stored in data structures.

>>> def myfunc(a, b):
...     return a + b
...
>>> funcs = [myfunc]
>>> funcs[0]
<function myfunc at 0x107012230>
>>> funcs[0](2, 3)
5
```

List comprehensions
```python
# Python's list comprehensions are awesome.

vals = [expression 
        for value in collection 
        if condition]

# This is equivalent to:

vals = []
for value in collection:
    if condition:
        vals.append(expression)

# Example:

>>> even_squares = [x * x for x in range(10) if not x % 2]
>>> even_squares
[0, 4, 16, 36, 64]
```

Lambda functions
```python
# The lambda keyword in Python provides a
# shortcut for declaring small and 
# anonymous functions:

>>> add = lambda x, y: x + y
>>> add(5, 3)
8

# You could declare the same add() 
# function with the def keyword:

>>> def add(x, y):
...     return x + y
>>> add(5, 3)
8

# So what's the big fuss about?
# Lambdas are *function expressions*:
>>> (lambda x, y: x + y)(5, 3)
8

# • Lambda functions are single-expression 
# functions that are not necessarily bound
# to a name (they can be anonymous).

# • Lambda functions can't use regular 
# Python statements and always include an
# implicit `return` statement.
```

Conditional expressions aka Ternary operator
```python
# Python supports one additional decision-making
# entity called a conditional expression:

>>> raining = False
>>> print("Let's go to the", 'beach' if not raining else 'library')
Let's go to the beach
>>> raining = True
>>> print("Let's go to the", 'beach' if not raining else 'library')
Let's go to the library

>>> age = 12
>>> s = 'minor' if age < 21 else 'adult'
>>> s
'minor'

>>> 'yes' if ('qux' in ['foo', 'bar', 'baz']) else 'no'
'no'

# Notice the non-obvious order: the middle
# expression is evaluated first, and based
# on that result, one of the expressions on
# the ends is returned.

# A common use of the conditional expression
# is to select variable assignment:
>>> m = a if a > b else b

# Note that conditional expression has lower
# precedence than virtually all the other operators:
>>> x = y = 40

>>> z = 1 + x if x > y else y + 2
>>> z
42

>>> z = (1 + x) if x > y else (y + 2)
>>> z
42

>>> z = 1 + (x if x > y else y) + 2
>>> z
43
```

 