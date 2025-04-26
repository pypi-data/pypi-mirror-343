To make a release:

- Run `tox` and check that the generated report looks good.
  Tests are supposed to fail, they don't test this package.
  They are examples in order to generate a test report.
  Testing this package means looking at the generated example report.
- Increment the version number in [pytest_reporter_html_dots/__init__.py](pytest_reporter_html_dots/__init__.py).
- Create a new tag.

  ```bash
  $ git tag html-dots-vX.X.X
  ```

- Install flit

  ```bash
  $ python -m venv venv
  $ venv/bin/pip install flit
  ```

- Release

  ```bash
  $ venv/bin/flit publish
  $ git push
  $ git push --tags
  ```
