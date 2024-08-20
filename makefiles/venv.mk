# Define the name of the requirements file
REQUIREMENTS_FILE = requirements.txt

# Default target
all: freeze

# Target to freeze the current pip environment
freeze:
	pip freeze > $(REQUIREMENTS_FILE)
	echo "Requirements have been written to $(REQUIREMENTS_FILE)"

# Target to install requirements from requirements.txt
install:
	pip install -r $(REQUIREMENTS_FILE)
	echo "Installed packages from $(REQUIREMENTS_FILE)"

# Clean target (optional)
clean:
	rm -f $(REQUIREMENTS_FILE)
	echo "$(REQUIREMENTS_FILE) has been removed"
