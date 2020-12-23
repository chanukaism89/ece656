#!/bin/bash

sudo apt-get update
sudo apt-get install python3-dev libssl-dev python3

# install pip
apt-get install python3-venv
apt install python3-pip
rm -rf venv
python3 -m venv venv

# create virtual environment and install requirements
source venv/bin/activate
pip install -r requirements.txt

# copy data files to mysql file folder
tar -xvf DBfiles/recipes_all.tar
tar -xvf DBfiles/recipe_ingredient_mapping.tar
cp DBfiles/ingredients_table.csv /var/lib/mysql-files/
cp DBfiles/recipe_prep_steps_1000 /var/lib/mysql-files/
cp DBfiles/recipes_all.csv /var/lib/mysql-files/
cp DBfiles/recipe_ingredient_mapping /var/lib/mysql-files/

