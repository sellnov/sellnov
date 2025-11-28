.PHONY: development requirements.txt help$

clear:
	find . -name *.pyc -exec rm -f {} \;
	find . -name *.pyo -exec rm -f {} \;

env-activate:
	(source env/bin/activate)

development : env-activate
	(source env/bin/activate && pip install -e .)

runserver:
	(source env/bin/activate && ./manage runserver 0.0.0.0:7000)
