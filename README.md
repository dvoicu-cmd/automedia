# Project-Automatic
A system to autogenerate and upload short form content

## Tree File Structure 
```
.
├── deployments
│   ├── environments
│   └── mariadb
│       └── db_setup
├── doc
└── scripts
    ├── creator
    ├── lib
    ├── publisher
    └── scraper

```

### deployments:
infrastructure documentation, constraints and set up for the project

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

