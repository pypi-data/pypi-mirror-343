
# Hello-NOO

This is an example repository for a python package, for my own reference.




## Development: Things to remember

### Make a source distribution

```text
python -m build --sdist
```

This makes a `*tar.gz` in the `dist/` folder


### Make a wheel

```text
python -m build --wheel
```

This makes a `*.whl` in the `dist/` folder

### Check with twine

```text
twine check dist/*
```

Checks the files in the `dist/` folder


### Upload to PyPi

```text
twine upload --verbose --repository pypi dist/*
```

### Uninstall everyting

```
pip freeze --exlucde hello-NOO | xargs pip uninstall -y
pip uninstall hello-NOO
```

## Resources

[https://pypi.org/classifiers/]()

[https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#classifiers]()


