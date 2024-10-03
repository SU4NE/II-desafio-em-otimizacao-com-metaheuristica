include .env
.PHONY: pylint activeblack format check

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE) $(FORMAT_CHECK_SRC)

activeblack:
	black $(FORMAT_CHECK_SRC)

format: activeblack

check: pylint 

prepare-commit: format check