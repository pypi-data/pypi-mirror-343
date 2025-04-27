
.PHONY: docs

docs:
	rm -r ./docs/source -f
	rm -r ./docs/_templates -f
	rm -r ./docs/_build -f
	sphinx-apidoc -o ./docs/source ./checksum_dict

mypyc:
	mypyc checksum_dict/_utils.py --strict --pretty --disable-error-code unused-ignore --install-types 
	mypyc checksum_dict/base.py --strict --pretty --disable-error-code unused-ignore --install-types
	mypyc checksum_dict/default.py --strict --pretty --disable-error-code unused-ignore --install-types
