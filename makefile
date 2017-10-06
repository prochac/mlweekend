# mlweekend - Enter task for Machine learning weekend
# author: prochac

clean:
	rm -rf venv

venv:
	python3 -m venv venv

install: clean venv
	. venv/bin/activate; python3 setup.py install
	. venv/bin/activate; python3 setup.py develop

launch: venv
	. venv/bin/activate; python3  mlweekend.py

