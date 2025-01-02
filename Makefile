prepare:
	rm -rf ./dist
	rm -rf ./equipment.egg-info
	rm -rf ./project/equipment
	mkdir -p ./project/equipment
	cp -r ./equipment/* ./project/equipment/

build:
	make prepare
	python -m pip install -r requirements.txt
	python -m pip install build setuptools wheel twine
	python -m build

test:
	make prepare
	python -m pip install coverage runtype faker
	python -m coverage run -m unittest discover -s tests
