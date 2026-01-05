# Automedia
A modular method to auto generating content.
Deploy the automedia project to multiple machines as microservices and configure to your liking

## Set Up Instructions

Download the latest release and unzip it.
```commandline
unzip automedia.zip
```
From there you will want to install all the dependencies. I've made a make file for this:
```commandline
cd automedia
make all
```
This should install all the needed dependencies.

Activate the python virtual environment
```commandline
source .venv/automedia_venv/bin/activate
```

The run the project root, and you should be good to go
```commandline
cd ..
python3 automedia
```

## Additional Set Up for Central Nodes

Nodes that are set up to be the central database require a little more additional system level set up.



### deployments:
infrastructure documentation, constraints and set up for the project found in the deploy dir

### doc:
project documentation.

### scripts:
contains the script files to deploy

scraper:
Visit predetermined source websites and media from the internet.

creator:
Take from database server media files and construct procedurally generated content.

publisher: 
Take saved video content from database server and publish the content.

## Account Pipeline
![diagram](/doc/system_diagram.png)
- abstract diagram of system

An account to publish to is established. A scraper is then created to pull specific content for the account. Raw media is stored in a designated storage server. Raw media for the desired account is then pulled and processed. Processed videos are then stored in designated storage server. Publisher then takes processed videos, uploades and archives the content.

Further documentation on system is in the doc directory.

## Demo
### CLI Navigation
![cli](/doc/cli_menus.gif)

### Youtube Uploading Automation Setup - AKA: Making a Formula
![general](/doc/general_nav.gif)

### More Navigation
![yt](/doc/formula_example.gif)


