build:
	rm -rf dist
	hatch build

publish:
	rm -rf dist
	hatch build
	twine upload dist/*

inspector:
	npx @modelcontextprotocol/inspector