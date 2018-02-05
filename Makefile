default : lint test run
		
lint:
		pylint ./cronparser.py || \
		pylint ./tests/doctests.py

test:
		python -mdoctest ./tests/doctests.py -v

run:
		python ./cronparser.py 1 2 3 4 5 ifconfig -a
		python ./cronparser.py 1-2 3-4 1-2 3-4 1-2 ls -la
