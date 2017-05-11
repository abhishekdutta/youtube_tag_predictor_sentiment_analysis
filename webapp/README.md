# Web Application for YouTube Recommender
This folder contains all files needed to run the application on localhost.

# Setup
## Basic Environment

* Node: v6.10.2
* mysql: Ver 14.14 Distrib 5.5.54
* Required ports: 1881

### Database
YouTube Recommender uses mysql as its database. Install mysql before continuing.

Log in to mysql with an admin account and run `CREATE DATABASE youtube_data;`. Remember the account username and password. We will need it later.

### Configuration
Secrets and configuration information are stored in `config.js`. However this file is gitignored to prevent leaking of secrets.

We provide an example file `config.js.example`. Run `cp config.js.example config.js` to create `config.js` in the same directory. DO NOT DELETE THE ORIGINAL EXAMPLE FILE.

Edit the `config.js` file with the required information. You will need the database account information as mentioned above.

### Node
Dependencies should already be saved in `package.json`. 

Run `npm install` to install dependencies. 

Run `node server.js` to start the app.

### Errors
If there are missing dependency errors, run `npm install <ANY_MISSING_DEPENDENCIES>` to add them. 

If you encounter a node-gyp error on Windows, download Visual C++ Build Tools 2015 and then run `npm config set msvs_version 2015`. Now node-gyp should work. Run `npm install <DEPENDENCY_WHICH_CAUSED_ERROR>` to redo the installation.

If there are any other errors, ensure that all steps above have been followed. Try turning it off and on again. 

Contact us if there are any further issues.

## Development Environment
Access App via http://localhost:1881. Please do not change the port number. 