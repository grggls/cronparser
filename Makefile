default : lint test run
		
lint:
		pylint ./cronparser/__init__.py || \
		pylint ./tests/doctests.py

test:
		python -mdoctest ./tests/doctests.py -v

run:
		python -m cronparser.__init__ 1 2 3 4 5 ifconfig -a
		python -m cronparser.__init__ 1-2 3-4 1-2 3-4 1-2 ls -la
