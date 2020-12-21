# ECE656 Project - Recipe Finder
ECE656 Project 

# Initial Setup

To install required dependancies run following

```
bash setup.sh
```
This will create a virtual environment and install necessary dependancies


Create DB

```
mysql --local-infile=1 -u root -p
CREATE DATABASE SmartChef;
USE SmartChef;
```

Load data into the DB

```
source /path/to/project/DBfiles/dbscript.sql
```

# Start Web server

```
python3 namage.py runserver 0.0.0.0:8000
```

Connect to the webser using web browser

IP:8000
