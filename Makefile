# ----------------------------------------------------------- #
# ------------------------ MAKEFILE ------------------------- #
# ----------------------------------------------------------- #
# ---------------- MAKE SURE TO RUN AS ROOT ----------------- #
# ----------------------------------------------------------- #

# ---------------------------- Variables ---------------------------- #

# Define the virtual environment directory
VENV_DIR = $(PWD)/.venv/automedia_venv

# Define the apt and pip dependencies
APT_DEPENDENCIES = ffmpeg gcc libespeak1 libmariadb-dev libmariadb3 nfs-kernel-server python3-dev python3.11-venv imagemagick
PIP_DEPENDENCIES = -r requirements.txt
# Define the URL for the Google Chrome .deb package
CHROME_URL = https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Define the name of the downloaded .deb package
CHROME_DEB = google-chrome-stable_current_amd64.deb

# Define the rules
.PHONY: all clean


# ------------------------ All/Regular Nodes ------------------------ #

# First install chrome, then the apt dependencies, then the virtual environment, then install the dependencies into the virtual environment
all: install_chrome apt_dependencies $(VENV_DIR)/bin/activate $(VENV_DIR)/.installed

# Rule to install apt dependencies
apt_dependencies:
	apt-get install -y $(APT_DEPENDENCIES)

# Rule to create the virtual environment
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)

# Rule to install dependencies within the virtual environment
$(VENV_DIR)/.installed: $(VENV_DIR)/bin/activate requirements.txt
	$(VENV_DIR)/bin/pip install $(PIP_DEPENDENCIES)

# Define the rule to download and install Google Chrome
install_chrome:
	wget $(CHROME_URL) -O $(CHROME_DEB)
	-dpkg -i $(CHROME_DEB)
	apt-get install -y -f  # Install any missing dependencies
	rm -f $(CHROME_DEB)

# ------------------------ Additional NFS Client Rules ------------------------ #

# Rule that sets the nfs mount points on clients
# Expects a specific ip, ex: 10.10.2.3
nfs_mount:
	mkdir /mnt/active
	mkdir /mnt/archive
	echo "$(IP_ADDRESS):/mnt/active /mnt/active nfs auto 0 0" | tee -a /etc/fstab >/dev/null
	echo "$(IP_ADDRESS):/mnt/archive /mnt/archive nfs auto 0 0" | tee -a /etc/fstab >/dev/null
	systemctl reboot

# Rule to clean the nfs mounts
clean_nfs_mounts:
	-umount /mnt/activate
	-umount /mnt/archive
	rm -r /mnt/archive
	rm -r /mnt/active
	head -n -2 /etc/fstab > tmp && mv tmp /etc/fstab


# ------------------------ Additional DbNas Server Rules ------------------------ #

# Rule that sets the nfs exports on the server
# Expects an ip range, ex: 10.10.2.0/24
# ex call:
# make export_nfs_directories IP_RANGE=10.10.2.0/24
nfs_exports:
	mkdir /mnt/active
	mkdir /mnt/archive
	echo "/mnt/active $(IP_RANGE)(rw,sync,no_subtree_check,insecure,no_root_squash)" | tee -a /etc/exports >/dev/null
	echo "/mnt/archive $(IP_RANGE)(rw,sync,no_subtree_check,insecure,no_root_squash)" | tee -a /etc/exports >/dev/null
	systemctl reboot

# Rule to clean the nfs exports
clean_nfs_exports:
	-umount /mnt/activate
	-umount /mnt/archive
	rm -r /mnt/archive
	rm -r /mnt/active
	head -n -2 /etc/exports > tmp && mv tmp /etc/exports

# Rule to install mariadb server and secure the installation
secure_mariadb:
	apt-get install -y mariadb-server
	mysql_secure_installation


# ------------------------ CLEAN ------------------------ #

# Rule to clean installed dependencies and virtual environment
clean:
	rm -rf $(VENV_DIR)
	rm -rf $(HOME)/.config/google-chrome
	apt-get remove -y google-chrome-stable
	apt-get remove -y $(APT_DEPENDENCIES)


