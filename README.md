# Cocoapods Extract
This is going to read the podspec.json files from the https://github.com/CocoaPods/Specs repository and extract information to populate sql database.

## Getting Started

Please make sure that the local environemnt has python and postgres installed

### Prerequisites

In Python make sure to have git and psycopy installed, if not do execute the steps below

pip install gitpython
pip install psycopg2

In postgres, make sure the database is created, if not excute the steps below

psql -U postgres
CREATE DATABASE cocoapods;
\connect cocoapods;

## Deployment

Step 1 - Run the Cocoapods_clone_repo.py file to clone the https://github.com/CocoaPods/Specs repo to your local direcotry. The script will ask you to input the url of the github repo you want to download, as well as the path of the local directory where you want to clone to.

Step 2 - Run the Cocoapods__create_tables.py file to create the library and library_version table in postgres. The script will ask you to input the database name, the username and the password to connect to postgres sql.

Step 3 - Run the Cocoapods__insert_clone_tables.py file to parse the podspec.json files in the repo and populate the library and library_verson tables with information found in the files. The script will ask you to input the path of the local directory where you have saved the clone to, database name, the username and the password to connect to postgres sql.

Step 4 - Run the Cocoapods_update_repo.py file to check if there are new commits in the repository, this will rename the original repo to a backup directory and clone the url again to the local directory. The script will ask you to input the url of the github repo you want to download, the path to the new repo directory and the path to the original repo (backup direcotry).

Step 5 - Run the Cocoapods__update_clone_tables.py file to insert information from the newly commited files to the library and library_version tables. The script will ask you to input the path to the new repo directory, the path to the original repo (backup direcotry), the database name, the username and the password to connect to postgres sql.

## License

This project is licensed under the MIT License


