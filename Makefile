VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

build: $(VENV)/bin/activate
	@truncate -s 0 database/*.log
	$(PYTHON) database/init_db.py

run: $(VENV)/bin/activate
	$(PYTHON) insert.py

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)