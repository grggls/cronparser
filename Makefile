default: test
		
test:
		pylint ./cronparser.py || \
		python -mdoctest ./cronparser.py -v
