tdrop table if exists recipes_reviews;
drop table if exists recipes_likes;
drop table if exists recipes_recipe_prep_steps;
drop table if exists recipes_recipe_ingredient_mapping;
drop table if exists recipes_ingredients;
drop table if exists recipes_recipes;
drop table if exists auth_user;

CREATE TABLE auth_user (id INT AUTO_INCREMENT, password VARCHAR(128) NOT NULL, last_login DATETIME(6), is_superuser TINYINT(1), username VARCHAR(150) NOT NULL UNIQUE, first_name VARCHAR(150), last_name VARCHAR(150), email VARCHAR(254), is_staff TINYINT(1), is_active TINYINT(1), date_joined DATETIME(6), PRIMARY KEY (id));

CREATE TABLE recipes_recipes(recipe_id INT, recipe_name LONGTEXT NOT NULL, recipe_websearch_id INT, recipe_cooktime INT, recipe_contributor INT, recipe_submitted_date DATE, recipe_numof_steps INT NOT NULL, recipe_description LONGTEXT, recipe_numof_ingredients INT NOT NULL, recipe_likes INT DEFAULT 0, recipe_visits INT DEFAULT 0, PRIMARY KEY (recipe_id));

CREATE TABLE recipes_ingredients(ingredient_id INT, ingredient_name  LONGTEXT NOT NULL, ingredient_vists INT DEFAULT 0, PRIMARY KEY (ingredient_id));

CREATE TABLE recipes_recipe_ingredient_mapping(mapping_id INT, recipe_id_id INT NOT NULL, ingredient_id_id INT NOT NULL, PRIMARY KEY (mapping_id), FOREIGN KEY (recipe_id_id) REFERENCES recipes_recipes(recipe_id), FOREIGN KEY (ingredient_id_id) REFERENCES recipes_ingredients(ingredient_id));

CREATE TABLE recipes_recipe_prep_steps(steps_id INT, recipe_id_id INT NOT NULL, step_description LONGTEXT, step_number INT NOT NULL, PRIMARY KEY (steps_id), FOREIGN KEY (recipe_id_id) REFERENCES recipes_recipes(recipe_id));

CREATE TABLE recipes_likes(id INT AUTO_INCREMENT, recipe_id_id INT, user_id_id INT, is_like TINYINT(1), PRIMARY KEY (id), FOREIGN KEY (recipe_id_id) REFERENCES recipes_recipes(recipe_id), FOREIGN KEY (user_id_id) REFERENCES auth_user(id));

CREATE TABLE recipes_reviews(id INT AUTO_INCREMENT, review LONGTEXT, recipe_id_id INT, user_id_id INT, PRIMARY KEY (id), FOREIGN KEY (recipe_id_id) REFERENCES recipes_recipes(recipe_id), FOREIGN KEY (user_id_id) REFERENCES auth_user(id));

SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/recipes_all.csv'  INTO TABLE recipes_recipes FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/ingredients_table.csv' INTO TABLE recipes_ingredients CHARACTER SET UTF8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/recipe_prep_steps_1000' INTO TABLE recipes_recipe_prep_steps CHARACTER SET UTF8 FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/recipe_ingredient_mapping' INTO TABLE recipes_recipe_ingredient_mapping FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
