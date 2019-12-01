# Publishing to PyPI

Generate the distribution files.

```
python3 setup.py sdist bdist_wheel
```

Upload to Test PyPI.
```
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Test publication to Test PyPI in a new Python virtualenv.

```
pip3 install --extra-index-url https://test.pypi.org/simple/ ontogram
```

If all is good, publish to the production PyPI.

```
python3 -m twine upload dist/*
```