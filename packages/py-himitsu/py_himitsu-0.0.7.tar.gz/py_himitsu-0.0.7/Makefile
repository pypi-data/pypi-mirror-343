VERSION=$(shell python scripts/version.py)
DESTDIR=/
PREFIX=/usr

wheel := dist/py_himitsu-$(VERSION)-py3-none-any.whl

all: check lint build

check:
	PYTHONPATH=src python -m unittest tests/test*

lint:
	ruff check -q .

build:
	python3 -m build

build-wheel: $(wheel)
	python3 -m build -w

install: build-wheel
	python -m installer --destdir=$(DESTDIR) --prefix=$(PREFIX) $(wheel)

clean:
	rm -f $(wheel)
	rm -rf __pycache__
	rm -rf src/himitsu/__pycache__
