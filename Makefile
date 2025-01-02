prepare:
	rm -rf ./dist
	rm -rf ./equipment.egg-info
	rm -rf ./project/equipment
	mkdir -p ./project/equipment
	rsync -av --exclude '__pycache__' ./equipment/ ./project/equipment/
	rm -rf ./equipment/Command/_project
	mkdir -p ./equipment/Command/_project
	rsync -av --exclude '__pycache__' ./project/* ./equipment/Command/_project/
	cp README.md ./equipment/Command/_project/README.md

build:
	make prepare
	python -m pip install -r requirements.txt
	python -m build

test:
	make prepare
	python -m pip install coverage runtype faker
	python -m coverage run -m unittest discover -s tests
