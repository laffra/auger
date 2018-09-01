rm dist/*

python setup.py sdist bdist_wheel

python -m twine upload dist/*

curl -s https://pypi.org/project/auger-python/ | grep "auger-python 0"
