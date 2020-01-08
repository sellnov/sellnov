.PHONY: development requirements.txt help

clear:
	find . -name *.pyc -exec rm -f {} \;
	find . -name *.pyo -exec rm -f {} \;

env-activate:
	(source env/bin/activate)

development : env-activate requirements.txt

requirements.txt :
	(source env/bin/activate && pip install pip --upgrade)
	(source env/bin/activate && pip install -r $@)

runserver:
	(source env/bin/activate && ./manage runserver 7000)
