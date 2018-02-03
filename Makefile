default : lint test run
		
lint:
		pylint ./cronparser.py || \
		pylint ./doctests.py

test:
		python -mdoctest ./doctests.py -v

run:
		python ./cronparser.py 1 2 3 4 5 ifconfig -a
		python ./cronparser.py 1-2 3-4 1-2 3-4 1-2 ls -la
