# ****************************************************************************
#
#    Makefile
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Created: 2026/04/22
#
# ****************************************************************************

PYTHON = python3
MAIN   = a_maze_ing.py

# ********************************* INSTALL **********************************
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install flake8 mypy
	$(PYTHON) -m pip install mpg123

# ******************************** RUN ***************************************
run:
	$(PYTHON) $(MAIN) config.txt

# ******************************** DEBUG *************************************
debug:
	$(PYTHON) -m pdb $(MAIN) config.txt

# ******************************** CLEAN *************************************
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# ******************************** LINT **************************************
lint:
	flake8 .
	mypy . --warn-return-any \
	        --warn-unused-ignores \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs

# ******************************** LINT STRICT *******************************
lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict