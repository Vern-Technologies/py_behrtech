
# Cleans dist folder of old version files
rm -R dist/

# Builds the package with wheel
python3 gateway_package/setup.py sdist bdist_wheel

source venv/bin/activate

# Pushes package to pypi package repository
twine upload -u matthewashley1 -p S8#E54sa90##osiZGWSE dist/*

