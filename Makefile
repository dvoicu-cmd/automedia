# ----------------------------------------------------------- #
# ------------------------ MAKEFILE ------------------------- #
# ----------------------------------------------------------- #
# ---------------- MAKE SURE TO RUN AS ROOT ----------------- #
# ----------------------------------------------------------- #

# ---------------------------- Variables ---------------------------- #

# Define the virtual environment directory
VENV_DIR = $(PWD)/.venv/automedia_venv

# Define the apt and pip dependencies, maybe replace imagemagic with libmagick++-dev
APT_DEPENDENCIES = ffmpeg gcc libespeak1 libmariadb-dev libmariadb3 nfs-kernel-server python3-dev python3.11-venv imagemagick cron
PIP_DEPENDENCIES = -r requirements.txt
# Define the URL for the Google Chrome .deb package
CHROME_URL = https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Define the name of the downloaded .deb package
CHROME_DEB = google-chrome-stable_current_amd64.deb
# Define update link
UPDATE_URL = https://github.com/dvoicu-cmd/automedia/archive/refs/heads/main.zip

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
	apt-get update
	wget $(CHROME_URL) -O $(CHROME_DEB)
	-dpkg -i $(CHROME_DEB)
	apt-get install -y -f  # Install any missing dependencies
	rm -f $(CHROME_DEB)

# ------------------------ Additional NFS Client Rules ------------------------ #

# Rule that sets the nfs mount points on clients
# Expects a specific ip, ex: 10.10.2.3
nfs_mount:
	-mkdir /mnt/active
	-mkdir /mnt/archive
	echo "$(IP_ADDRESS):/mnt/active /mnt/active nfs noauto,x-systemd.automount 0 0" | tee -a /etc/fstab >/dev/null
	echo "$(IP_ADDRESS):/mnt/archive /mnt/archive nfs noauto,x-systemd.automount 0 0" | tee -a /etc/fstab >/dev/null
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
# If the nfs gives issues with caching use this command to drop cache data: sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
nfs_exports:
	-mkdir /mnt/active
	-mkdir /mnt/archive
	echo "/mnt/active $(IP_RANGE)(rw,sync,no_subtree_check,insecure,all_squash)" | tee -a /etc/exports >/dev/null
	echo "/mnt/archive $(IP_RANGE)(rw,sync,no_subtree_check,insecure,all_squash)" | tee -a /etc/exports >/dev/null
	systemctl reboot

# Rule that sets the nfs exports for publisher dirs.
publisher_nfs_exports:
	echo "/home/user/automedia_exports $(IP_RANGE)(rw,sync,no_subtree_check,insecure,all_squash)" | tee -a /etc/exports >/dev/null
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


# ------------------------ UPDATE ------------------------ #
# Rule to update to install from the latest main branch
# excepts a personal authorization token
# ex: TOKEN="<sha hash what not>"
update:
	# Set Parent Directory var
	$(eval THIS_DIR := $(PWD))
	$(eval PARENT_DIR := "$(shell dirname "$(THIS_DIR)")")

	# Access github api and install main branch zip archive
	apt-get install -y curl

	curl --output automedia-main.zip -L \
	-H "Accept: application/vnd.github+json" \
	-H "Authorization: Bearer $(TOKEN)" \
	-H "X-GitHub-Api-Version: 2022-11-28" \
	https://api.github.com/repos/dvoicu-cmd/automedia/zipball/main

	# unzip the archive
	unzip automedia-main.zip
	rm -f automedia-main.zip
	mv dvoicu-cmd-automedia-* $(PARENT_DIR)/automedia-main

	# Replace the py_services to the new proj to keep user information
	# central
	rm -rf $(PARENT_DIR)/automedia-main/src/central/py_services
	mv $(PARENT_DIR)/automedia/src/central/py_services $(PARENT_DIR)/automedia-main/src/central/py_services

	# creator
	rm -rf $(PARENT_DIR)/automedia-main/src/creator/py_services
	mv $(PARENT_DIR)/automedia/src/creator/py_services $(PARENT_DIR)/automedia-main/src/creator/py_services

	# publisher
	rm -rf $(PARENT_DIR)/automedia-main/src/publisher/py_services
	mv $(PARENT_DIR)/automedia/src/publisher/py_services $(PARENT_DIR)/automedia-main/src/publisher/py_services

	# scraper
	rm -rf $(PARENT_DIR)/automedia-main/src/scraper/py_services
	mv $(PARENT_DIR)/automedia/src/scraper/py_services $(PARENT_DIR)/automedia-main/src/scraper/py_services

	# move the config.ini file to the new project
	-mv src/config.ini $(PARENT_DIR)/automedia-main/src

	# rm the old python venv to save space for update
	rm -rf $(VENV_DIR)

	# rm the old project.
	# Btw the program starts to get unstable cuz the makefile has been deleted.
	rm -r $(PARENT_DIR)/automedia

	# Rename the new project (context.py bricks without this name)
	mv -f $(PARENT_DIR)/automedia-main $(PARENT_DIR)/automedia

	echo "SUCCESS: Remember to do "make all" after execution to update pip dependencies"
