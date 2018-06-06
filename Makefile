.PHONY: development requirements.txt help

env-activate: env
	(source .env/bin/activate)

development : env-activate init requirements.txt

requirements.txt :
	(source .env/bin/activate && pip install -r $@)
