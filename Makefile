include .env
.PHONY: pylint activeblack format check

#* Git Rules
isort:
	isort --settings-path=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE)  --recursive=y  $(FORMAT_CHECK_SRC)

activeblack:
	black $(FORMAT_CHECK_SRC)

format: activeblack isort

check: pylint 

prepare-commit: format check