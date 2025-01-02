prepare:
	rm -rf ./dist
	rm -rf ./equipment.egg-info
	rm -rf ./project/equipment
	mkdir -p ./project/equipment
	cp -r ./equipment/* ./project/equipment/
	rm -rf ./equipment/Command/_project
	mkdir -p ./equipment/Command/_project
	cp -r ./project/* ./equipment/Command/_project/
	cp project/.gitignore ./equipment/Command/_project/.gitignore
	cp project/.env.example ./equipment/Command/_project/.env.example
	cp project/.editorconfig ./equipment/Command/_project/.editorconfig
	cp project/.coveragerc ./equipment/Command/_project/.coveragerc
	cp README.md ./equipment/Command/_project/README.md

build:
	make prepare
	python -m pip install -r requirements.txt
	python -m build

test:
	make prepare
	python -m pip install coverage runtype faker
	python -m coverage run -m unittest discover -s tests
