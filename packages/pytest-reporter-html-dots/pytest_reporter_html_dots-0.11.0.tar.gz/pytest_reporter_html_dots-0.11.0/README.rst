=========================
pytest-reporter-html-dots
=========================

This is a fork of the great template `pytest-reporter-html1 <https://pypi.org/project/pytest-reporter-html1/>`_ with one detail changed: Instead of grouping the tests and showing only a number how many tests have failed and how many have passed, this template tries to mimic the standard pytest output with one dot for every test.
This has the advantages that (1) even without expanding a file it's visible which tests have failed and whether they are the same like in the last run and (2) it gives a better visualization how many tests have failed in a specific file.
Hovering over a badge shows the name of the test and it's status (e.g. passed/failed/skipped).

A basic HTML report for `pytest`_ using `Jinja2`_ template engine.
Based on `pytest-reporter`_ which provides the data to the template.


Features
--------

* Overview of files, tests, and phases with expandable sections
* Includes information about tests such as documentation, markers, and fixtures
* Fairly mobile friendly
* Complies with Jenkins default CSP policy (with ``--split-report``)
* Support for `pytest-metadata`_ and `pytest-rerunfailures`_
* May be used as a base template for customization

.. image:: https://gitlab.com/erzo/pytest-reporter-html-dots/-/raw/master/screenshot.png
    :alt: Screenshot


Installation
------------

You can install "pytest-reporter-html-dots" via `pip`_ from `PyPI`_::

    $ pip install pytest-reporter-html-dots


Usage
-----

Specify the html-dots template and the output path of the report::

    $ pytest --template=html-dots/index.html --report=report.html

By default the report is self-contained, but you can separate CSS, images,
and JavaScript by specifying the ``--split-report`` option.


Customization
-------------

You can customize this template using  `template inheritance`_.

If you want to add more information to the meta data table, extend the ``session_metadata`` block.
Create the following file called ``report-template.html`` next to your ``tox.ini``:

.. code:: html

    {% extends "html-dots/index.html" %}
    {% block session_metadata %}
        {{ super() }}
        <tr>
            <th>System under test version</th>
            <td>{{ version }}</td>
        </tr>
    {% endblock %}

Add ``version`` to the context in the `pytest_reporter_context hook <https://github.com/christiansandberg/pytest-reporter/blob/master/pytest_reporter/hooks.py>`_ in ``conftest.py``:

.. code:: python

    import pytest

    @pytest.hookimpl  # type: ignore [misc]  # Untyped decorator makes function "pytest_reporter_context" untyped
    def pytest_reporter_context(context: 'dict[str, object]', config: 'pytest.Config') -> None:
        context['version'] = '0.1.2'

Add ``--template-dir`` and change ``--template`` in ``tox.ini``
(I am using ``bash`` to insert a timestamp into the report name via command substitution with ``date``):

.. code:: ini

    [tox]
    envlist = py3
    isolated_build = True
    
    [testenv]
    allowlist_externals = bash
    deps =
        mypy
        pytest
        pytest-reporter-html-dots
    commands =
        mypy src
        bash -c "pytest --template-dir={toxinidir} --template=report-template.html --report={toxinidir}{/}log{/}pytest-`date +%Y-%m-%d_%H-%M`.html {posargs}"


----

Some additional filters are available for templates to use:

``asset(path_or_content, extension)``
    Takes a path to a local file or a raw bytes object and either returns a
    base64 encoded URL or a new relative URL to a copy depending on if the
    report is self-contained or not.

    .. code:: html

        <img src="{{ 'path/to/image.png'|asset }}">
        <img src="{{ raw_byte_data|asset('png') }}">

``ansi(s)``
    Convert ANSI color codes to HTML.

``strftime(value, format)``
    Format a Unix timestamp using `datetime.strftime`_.

    .. code:: html

        Started: {{ started|strftime('%Y-%m-%d %H:%M:%S') }}

``timedelta(value)``
    Convert a time in seconds to a `timedelta`_ object.

``rst(s)``
    Convert reStructuredText to HTML.


.. _`Jinja2`: https://jinja.palletsprojects.com/
.. _`template inheritance`: https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pytest-reporter`: https://github.com/christiansandberg/pytest-reporter
.. _`pytest-metadata`: https://github.com/pytest-dev/pytest-metadata
.. _`pytest-rerunfailures`: https://github.com/pytest-dev/pytest-rerunfailures
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`datetime.strftime`: https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime
.. _`timedelta`: https://docs.python.org/3/library/datetime.html#timedelta-objects
