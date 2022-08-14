PY_FILES := $(shell find . -name '*.py')

.DEFAULT_GOAL := .tested

.tested: $(PY_FILES)
	nosetests
	touch .tested

.PHONY: clean
clean:
	git clean -Xdff
