# Define the virtual environment directory
VENV_DIR = $(PWD)/.venv/automedia_venv

# Define the apt and pip dependencies
APT_DEPENDENCIES = ffmpeg gcc libespeak1 libmariadb-dev libmariadb3 nfs-kernel-server python3-dev python3.11-venv imagemagick
PIP_DEPENDENCIES = -r requirements.txt

# Define the rules
.PHONY: all clean

# First apt dependencies, then the virtual environment, then install the dependencies into the virtual environment
all: apt_dependencies $(VENV_DIR)/bin/activate $(VENV_DIR)/.installed

# Rule to install apt dependencies
apt_dependencies:
    apt-get install $(APT_DEPENDENCIES)

# Rule to create the virtual environment
$(VENV_DIR)/bin/activate:
    python3 -m venv $(VENV_DIR)

# Rule to install dependencies within the virtual environment
$(VENV_DIR)/.installed: $(VENV_DIR)/bin/activate requirements.txt
    $(VENV_DIR)/bin/pip install $(PIP_DEPENDENCIES)
    touch $(VENV_DIR)/.installed

# Rule to clean installed dependencies and virtual environment
clean:
    rm -rf $(VENV_DIR)
    apt-get remove $(APT_DEPENDENCIES)