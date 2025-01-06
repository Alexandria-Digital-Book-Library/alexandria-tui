POETRY := ${HOME}/.local/bin/poetry

build: 
	$(POETRY)	build

install:
	$(POETRY) install

run: 
	$(POETRY) run alexandria-tui

run-raw:
	python3 -m alexandria

publish:
	$(POETRY) publish

.PHONY: build install run
