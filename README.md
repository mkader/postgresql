Cloud Database for Web Apps  with Django

    Types of databases
        Non-relational / document databases: MongoDB, Firebase, CouchDB, etc.
        Relational databases: MySQL, SQLite, PostgreSQL, etc.
   
    Dockerfile
        ARG IMAGE=bullseye => The bullseye Docker image is based on Debian 11 Linux distribution.
        FROM mcr.microsoft.com/devcontainers/${IMAGE} => The image from the MS Container Registry for development containers. 
        ENV PYTHONUNBUFFERED 1 => Python output is unbuffered and sent directly to the console, which can be helpful when debugging applications.
        RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \ => used to prevent prompts from appearing during the installation process.
            && apt-get -y install --no-install-recommends postgresql-client \ =>installs the client package using apt-get, provides the psql command-line tool. 
            && apt-get clean -y && rm -rf /var/lib/apt/lists/* => clean up the package cache and remove unnecessary files to reduce the size of the Docker image.

    docker-compose.yaml
        services: => This defines two services - app and db.
        app:
            build:
                context: ..
                dockerfile: .devcontainer/Dockerfile
                args:
                    IMAGE: python:3.11
                volumes:
                    - ..:/workspace:cached
                command: sleep infinity
                network_mode: service:db
            The app service builds the Docker image from the dockerfile using the Python version. 
            
            The volumes section mounts the parent directory (..) of the .devcontainer directory to the /workspace directory in the ontainer, 
            allowing the local code changes to be reflected in the container. 
            
            The command section keeps the container running indefinitely, and network_mode section sets the network mode to be the same as the db service, allowing them to communicate with each other.       
        db:
            image: postgres:latest
            restart: unless-stopped
            volumes:
                - postgres-data:/var/lib/postgresql/data
            environment:
                POSTGRES_DB: postgres
                POSTGRES_USER: admin
                POSTGRES_PASSWORD: LocalPasswordOnly
            The db service uses the latest PostgreSQL image from Docker Hub,
            
            The volumes section mounts the postgres-data volume to the /var/lib/postgresql/data directory in the container. 
            
            The environment section sets the POSTGRES_DB, USER, PASSWORD variables, which are used to create a new PostgreSQL database and user.
        volumes:
            postgres-data: 
            A named volume called postgres-data, which can be used to persist data across container restarts. 
            
            Any data that is stored in the /var/lib/postgresql/data directory in the db service will be persisted in this volume.

    devcontainer.json -  is a configuration file used by VSC to define a development container for a project. 
        
        It specifies the dev environment, including the Docker image to use, the container configuration, and the extensions to install in the container.
        
        Configuration needed to work with the Docker files:
            "name": "python-db-copilot"  => Sets the name of the development container to python-db-copilot.
            
            "dockerComposeFile": "docker-compose.yaml" => Specifies the Docker Compose file to use when building the dev container.
            
            "service": "app" => Specifies which service in the Docker Compose file to use as the main dev environment.
            
            "workspaceFolder": "/workspace" => the workspace folder in the container that will be mapped to the local project directory.
            
            "forwardPorts": [5432] => which ports to forward from the container to the local machine (5432 is the default PostgreSQL port).
            
            "portsAttributes": { "5432": {"label": "PostgreSQL port", "onAutoForward": "silent"}} 
                Provides additional attributes for the forwarded port. In this case, a label to identify the forwarded port and sets the onAutoForward attribute to "silent", which means that VSC Code will automatically forward the port without prompting the user.

        Installing extensions:
            "ms-python.python" => Official Python extension for VSC, it provides features such as linting, debugging, code completion for Python.
            
            "ms-python.vscode-pylance" => An optional language server for Python that provides more advanced type checking and autocomplete features.
            
            "charliermarsh.ruff" => This extension provides support for the Ruff database migration tool.
           
            "ms-python.black-formatter" =>  Provides support for the Black code formatter for Python.
           
            "mtxr.sqltools" => General-purpose SQL extension that provides features(syntax highlighting, code completion, db management.)
           
            "mtxr.sqltools-driver-pg" => PostgreSQL driver for the SQL Tools extension.
           
            "ms-vscode.vscode-node-azure-pack" => Provides support for developing and deploying Node.js applications to Azure.

        Configuring SQLTools extension:
            "sqltools.connections": [
                {
                    "name": "Local database",
                    "driver": "PostgreSQL",
                    "server": "localhost",
                    "port": 5432,
                    "database": "postgres",
                    "username": "admin",
                    "password": "LocalPasswordOnly"
                }

    SQLTools extension: Connect to local or cloud databases. Create, Read, Write database
![alt](https://raw.githubusercontent.com/mkader/postgresql/main/github_codespace_sqltools.png)
    
Databases in Python
    
    create .env  file => DBHOST=..., DBNAME=...
    
    create requirements.txt
        psycopg2: PostgreSQL db adapter for Python, allows Python to connect and interact with PostgreSQL db.
        
        python-dotenv: Allows you to load environment variables from a .env file into your Python application. This can be useful for storing sensitive information like db credentials or API keys.
        
        SQLAlchemy: ORM (object-relational mapping) library for Python. It allows you to interact with db using Python code, a provides a high-level abstraction over SQL.
        
        mimesis: Python library for generating fake data. It can be useful for testing or populating a db with realistic-looking data.
        
        faker: Python library for generating fake data. It can also be useful for testing or populating a db with realistic-looking data.    

        pip install -r requirements.txt

    PostgreSQL in Python
        Option 1: use psycopg2 SQL directly. (psycopg.py)
        Option 2: Accessing DBs from Web Apps: ORM , SQLAlchemy (pyday_sqlalchemy.py)
    
Hosting DB (PostgreSQL) on Azure

    Managed services for PostgreSQL on Azure
        Option	                                        Description
        Azure Database for PostgreSQL – Single Server	MS's original offering. No longer recommended for new apps.
        
        Azure Database for PostgreSQL – Flexible Server	MS's most recent PostgreSQL offering. Fully managed service with vertical scaling.
        
        Azure Cosmos DB for PostgreSQL	                Distributed db using PostgreSQL and the Citus extension. Can scale horizontally.

        🔗 aka.ms/flex-vs-single Comparison: Flexible vs. Single Server
        🔗 aka.ms/flex-vs-cosmos Cosmos DB for PostgreSQL vs. Flex Server

    Provisioning PostgreSQL in Portal
        Portal -> "Select Azure Database for PostgreSQL – Flexible Server" resource -> Development -> Configure without Firewall
        
        Update Azure Connection setting in .env file
        
        Update your client ip address, check "Allow public access from any Azure ..." in Azure PostgreSQL Server Networking
        
        Codespace Terminal "curl ifconfig.me", get ip addess & update in firewall rule in Azure PostgreSQL Server Networking

        DATABASE_URI += "?sslmode=require" => Adds SSL mode require, connecting to the production server is to enforce SSL
  
![alt](https://raw.githubusercontent.com/mkader/postgresql/main/azure_postgresql_resource.PNG)
        
Writing Django Apps
    Django framework : an external library & framework for server-side code. Includes an ORM for database interaction.

    Apps written in Django:
        Coursera (originally, now Scala+Play)
        Instagram
        Pinterest (originally, now Flask)
        Eventbrite


Django apps on Azure   