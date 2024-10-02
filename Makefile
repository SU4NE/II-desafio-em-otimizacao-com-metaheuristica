include .env
.PHONY:pylint activeblack format check

#* Git Rules
pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE)  --recursive=y  $(FORMAT_CHECK_SRC)

activeblack:
	black $(FORMAT_CHECK_SRC)

format: activeblack

check: pylint 

prepare-commit: format check