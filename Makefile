include .env
.PHONY:pylint activeblack format check

#* Git Rules
CPP_SCR_FORMAT = $(shell dir /B /S $(SRC)\*.cpp | findstr "$(SRC)")

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE)  --recursive=y  $(FORMAT_CHECK_SRC)

activeblack:
	black $(FORMAT_CHECK_SRC)

format: activeblack

check: pylint 

prepare-commit: format check