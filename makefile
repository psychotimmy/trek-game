#Note you must have a Virtualenv ‘env’ (default) created before
#running these commands

ENVIRONMENT = env

run:
	#Run tests and then main.py
	$(ENVIRONMENT)/bin/coverage run test/run_tests.py
	$(ENVIRONMENT)/bin/python trek.py

tests:
	#Just run unit tests and display code coverage result
	$(ENVIRONMENT)/bin/coverage run test/run_tests.py
	$(ENVIRONMENT)/bin/coverage report