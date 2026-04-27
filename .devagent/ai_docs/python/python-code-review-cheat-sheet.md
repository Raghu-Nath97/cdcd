PYTHON GENERIC

----------------------------------------------------------------------------------------------------
Consider using [conditional expression](https://docs.python.org/3/reference/expressions.html#conditional-expressions) here.
----------------------------------------------------------------------------------------------------
Consider using [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) here.
----------------------------------------------------------------------------------------------------
Use [pathlib](https://docs.python.org/3/library/pathlib.html).
----------------------------------------------------------------------------------------------------
Use appropriate log severity level as described in [Logging HOWTO](https://docs.python.org/3/howto/logging.html#when-to-use-logging).
----------------------------------------------------------------------------------------------------
Use absolute imports instead of relative for [this reasons](https://realpython.com/absolute-vs-relative-python-imports/#pros-and-cons-of-absolute-imports).
----------------------------------------------------------------------------------------------------
For operations on sets, use non-operator versions of methods (e.g., `union` instead of `|`, `difference` instead of `-`).

[set() documentation](https://docs.python.org/3.8/library/stdtypes.html#set)
> Note, the non-operator versions of union(), intersection(), difference(), and symmetric_difference(), issubset(), and issuperset() methods will accept any iterable as an argument.
In contrast, their operator based counterparts require their arguments to be sets. This precludes error-prone constructions like set('abc') & 'cbs' in favor of the more readable set('abc').intersection('cbs').
----------------------------------------------------------------------------------------------------
Use descriptive-style for functions and methods docstrings.

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)
> The docstring should be descriptive-style ("""Fetches rows from a Bigtable.""") rather than imperative-style ("""Fetch rows from a Bigtable.""").
The docstring for a @property data descriptor should use the same style as the docstring for an attribute or a function argument ("""The Bigtable path.""", rather than """Returns the Bigtable path.""").
----------------------------------------------------------------------------------------------------
Use Google style docstrings.

[Gist with examples](https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e)
[Google Style Guide - Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
[Examples by Napoleon](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
----------------------------------------------------------------------------------------------------
Never use triple-quoted strings as multi-line comments.

[Python Code Development Standards - Multi-line comments](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Multi-line-comments)
----------------------------------------------------------------------------------------------------
Use consistent nomenclature for modules and packages.

[Python modules](https://docs.python.org/3/tutorial/modules.html)
> A module is a file containing Python definitions and statements. The file name is the module name with the suffix .py appended.

[Python packages](https://docs.python.org/3/tutorial/modules.html#packages)
> The __init__.py files are required to make Python treat directories containing the file as packages.
----------------------------------------------------------------------------------------------------
You can also format timestamps using f-Strings

```suggestion
            "timestamp": f"{datetime.now():%Y-%m-%d %T}",
```
----------------------------------------------------------------------------------------------------
To avoid conflicts with Python keyword or other co-existing variable of the same name, it's prefered to use `NAME_SUFFIX`/`name_suffix` convention first as primary one, alternatively just a trailing underscore (e.g., `class_` instead of `class`). Leading underscore is, by convention introduced in PEP8, a weak “internal use” indicator.

> `_single_leading_underscore`: weak “internal use” indicator (..) `single_trailing_underscore_`: used by convention to avoid conflicts with Python keyword
~ [PEP8 - Descriptive: Naming Styles](https://peps.python.org/pep-0008/#descriptive-naming-styles)

> When attribute name conflicts with reserved keywords (e.g. `class`, `print`) use prefix/suffix instead of leading/trailing underscores (`math_class`, `print_status`).
~ [P&G Python Code Development Standards: Code modularity](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Code-modularity)
----------------------------------------------------------------------------------------------------
Use import `module` as `mdl` only when `mdl` is a standard abbreviation (e.g., `np` for `numpy`, `pd` for `pandas`).

> [Python Code Development Standards - Imports](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Imports)
----------------------------------------------------------------------------------------------------
Names imported from one source in should appear in one `from (...) import (...)` statement.

> [Python Code Development Standards - Imports](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Imports)
----------------------------------------------------------------------------------------------------
Always import at the top of the file, right after module docstring and `__all__` attribute (if such is used).

> [Python Code Development Standards - Imports](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Imports)
----------------------------------------------------------------------------------------------------
Files generated as part of _project-specific development process_ shouldn't be listed in `.gitignore` - it's not possible to cover all potential scenarios.

> [StackOverflow - What should contain .gitignore file when is a public repository?](https://stackoverflow.com/questions/61982834/what-should-contain-gitignore-file-when-is-a-public-repository)
----------------------------------------------------------------------------------------------------
For unusual, unobvious, strange or unexpected implementations where context is needed to understand the choice - please provide explanation that would allow high-level understanding (e.g., in a form of a comment - even a brief one) to the reader. Links with reference reading material are welcome too.
----------------------------------------------------------------------------------------------------
If method is supposed to be overwritten, but class is not abstract so can't use `@abstractmethod` decorator - throw a `raise NotImplementedError('Not implemented or some other comment.')`
----------------------------------------------------------------------------------------------------
Use [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals) above other string formatting methods.

[f-strings - Python Documentation](https://realpython.com/python-f-strings/)
[f-strings - RealPython](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
[Python Code Development Standards - Python version](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Python-version)
----------------------------------------------------------------------------------------------------
> When trying to reduce line length, try to split line into atomic operations, or wrap expressions into parentheses.

~ [Python Code Development Standards - Maximum line length](https://jira-pg-ds.atlassian.net/wiki/spaces/DSUG/pages/221151431/Python+Code+Development+Standards+-+Basics#Maximum-line-length)
----------------------------------------------------------------------------------------------------
Don't inherit from `object` - it raises a question of "_Why it is there?_". Explicit inheriting from `object` was a thing for Python2/3 compatible code, which is a song of the past. It's a default in 3.

~ [StackOverflow topic](https://stackoverflow.com/questions/4015417/why-do-python-classes-inherit-object)
----------------------------------------------------------------------------------------------------
Using bare `return` without explicitly stating returned object is not needed and creates confusion.

- use `return None` when your intention is to return `None` explicitly
- use bare `return` when your intention is to break the loop / stop code block from further execution
- do nothing if function is supposed to be void and not return anything (will still return `None` but the code is more idiomatic this way)

~ [StackOverflow topic](https://stackoverflow.com/questions/15300550/return-return-none-and-no-return-at-all)
----------------------------------------------------------------------------------------------------
When facing repetition of values like string literals (most common case), it may be a good idea to invert dependency from concretions to abstractions (variables keeping those string literals) defined separately (either separate module or as module-level code in this one).

~ [Dependency Inversion Principle via Wikipedia](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
----------------------------------------------------------------------------------------------------



DNALIB

----------------------------------------------------------------------------------------------------
[Always pin the dnalib dependency](https://github.com/procter-gamble/de-cf-dnalib#installation-from-github-legacy) using release tag / commit SHA, unless on development environment.
On top of that, I suggest [using JFrog as dnalib source index](https://github.com/procter-gamble/de-cf-dnalib#installation-from-jfrog)

> Note you can (you should) specify an exact version (aka tag, e.g., v0.4.0) after the @ sign instead of master. We recommend using master only for development and release tags for production use. You can find all available tags in dnalib [releases page on GitHub](https://github.com/procter-gamble/de-cf-dnalib/releases).
~ [dnalib README](https://github.com/procter-gamble/de-cf-dnalib#installation-from-github-legacy)
----------------------------------------------------------------------------------------------------
Don't pin dependencies, but use ranges instead - widest possible (on both sides of range) and if there's no known limitation regarding newest supported version (i.e., if the newest available version of dependency is supported) then use `<NEXT_MAJOR_VERSION`, e.g., if current version of Flask is `2.1.3` and it's supported, while 1.X versions are not - use `Flask>=2.0.0,<3`
----------------------------------------------------------------------------------------------------
Only mock not-mocked-yet 3rd party dependencies, that are not listed in either `requirements.txt` or `requirements-devel.txt`.

> Always make sure you mocked all external (3rd party) modules not listed in requirements.txt or requirements-devel.txt. Only dependencies from those files are available when documentation is being built as part of CI/CD pipeline.
~ [dnalib.CONTRIBUTING: External modules' mocking](https://github.com/procter-gamble/de-cf-dnalib/blob/master/CONTRIBUTING.md#external-modules-mocking)
----------------------------------------------------------------------------------------------------
Don't use `dnalib.auxiliaries.log` in dnalib sub-package.

> In your steering Python script or executable (but not in your contributions to dnalib)
~ [dnalib.README: Change the appearance and level of logging](https://github.com/procter-gamble/de-cf-dnalib#change-the-appearance-and-level-of-logging)

> dnalib uses the standard Python logging module for the log event stream
~ [dnalib.CONTRIBUTING: Logging in dnalib modules](https://github.com/procter-gamble/de-cf-dnalib/blob/master/CONTRIBUTING.md#logging-in-dnalib-modules)
----------------------------------------------------------------------------------------------------
Every dnalib executable (public CLI script) should contain a module-level docstring explaining basics reqiuired to get started - can be a syntax guide, usage sample, scope overview, reference to external docs, etc.  

Examples:  
DBR CLI ([code](https://github.com/procter-gamble/de-cf-dnalib/blob/master/src/dnalib/exe/dbr.py) | [render](https://verbose-telegram-4859758a.pages.github.io/cli/dnalib.exe.dbr.html))  
MLX CLI ([code](https://github.com/procter-gamble/de-cf-dnalib/blob/master/src/dnalib/exe/mlx.py) | [render](https://verbose-telegram-4859758a.pages.github.io/cli/dnalib.exe.mlx.html))
----------------------------------------------------------------------------------------------------