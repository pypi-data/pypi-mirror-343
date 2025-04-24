# MadeLibLBL

Package for my daily use functions at Made.

## Upload to PyPI

1)Install dependencies:

```pip install hatchling wheel twine```

2)Remover builds antigos (optional):

```Remove-Item -Recurse -Force dist, build, *.egg-info```

3)Build package:

```python -m build```

4)Test upload to TestPyPI first (optional):

```twine upload --repository testpypi dist/*```

5)Upload to PyPI:

```twine upload dist/*```
