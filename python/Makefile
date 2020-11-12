requirements.txt: Pipfile Pipfile.lock
	@pipenv lock --requirements > requirements.txt

release:
	@pipenv run python setup.py sdist bdist_wheel upload

.PHONY: release
