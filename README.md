# ManageBac-Plus
> Since ManageBac **SUCKS**, we decided to make a new one. A better one. *This, is **ManageBac Plus.***

Just a simple Python Flask webapp built around ManageBac that adds a lot of useful functions to it.

## Table of contents
<!-- TOC -->
* [ManageBac-Plus](#managebac-plus)
  * [Table of contents](#table-of-contents)
  * [Features](#features)
  * [Usage](#usage)
    * [Prerequisites](#prerequisites)
    * [Launch](#launch)
    * [Parameters](#parameters)
    * [Deployment](#deployment)
  * [Current limitations](#current-limitations)
  * [TODOs](#todos)
<!-- TOC -->

## Features
- A convenient dashboard for checking your GPAs using dynamic pie charts
- GPA calculator for mid-terms and finals
- GPA calculator for marginal tasks (One extra task in a given category)
- Graphs for all those calculations
- Radar graph generation with respect to multiple subjects
- Personal projects gallery
- An online platform for sharing Mochi decks as well as notebooks
- AES256 encryption for student credentials database
- Reverse proxy with nginx and deployment level WSGI backend server to parallel process requests
- ... and much more!

## Usage
### Prerequisites
Before launching the app, make sure you have the **latest version of MySQL**, **Redis**, and the **required python libraries** installed.

Then, in your **MySQL terminal**, run the following commands to initialize the databases:
```shell
CREATE DATABASE credentials;
CREATE DATABASE scores;
CREATE DATABASE mochi;
CREATE DATABASE notebooks;
```
As for Redis, the default configuration should work fine.

To install the required python libraries, run the following command in your terminal:
```shell
python -m pip install -r requirements.txt
```
As MBP uses AES256 encryption for student credentials, you need to set a secret key for data encryption. You can do so by executing the following command in your terminal:
```shell
export key="[Your secret key]"
```
### Launch
To launch the app, make sure you have all the prerequisites installed, then simply run the following command in your terminal:
```shell
python app.py
```
The app will be deployed at `http://localhost:8000/` and will be open to LAN by default.
### Parameters
In case you have a custom installation/configuration of MySQL, you can specify the username, password, and port for MBP to connect to with the environment variables `db_username`, `db_password`, and `db_port` respectively.

Set `db_reset=1` to reset the databases upon launch and `debug=1` to enable Flask debug mode.

Set `logs_reset=0` to keep the log file from previous sessions instead of deleting it.
### Deployment
For deployment, MBP uses `gunicorn` by default (included in `requirements.txt`) and is bound to `0.0.0.0:8000`. To deploy, simply run the following command in your terminal:
```shell
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES; gunicorn
```
The environment variables mentioned above can also be set for deployment.

As for `nginx`, you should configure it to reverse proxy requests to `0.0.0.0:8000`.

## Current limitations
We're all just high school students and making perfect dynamic websites is obviously not our daily job. Hence I'll have to admit that there are many limitations to the current website:
- Lack of encryption for student credentials (SOLVED with AES256)
- Horrible database schema that minimizes efficiency
- Tons of hidden bugs not fixed
- Uses a ton of RAM (not optimized at all)
- Funding problems for future server deployment (SOLVED)

Just to name a few. However, we are also actively working on finding solutions to these problems, and I'm confident that this process won't take long.

## TODOs
- Uploaded files delete function (Hard, need full account system)
- /grades add load GPA history
- Uploaded files change name, description, etc. (Hard, need full account system)
- Curving calculator for teachers (Currently unaccepted)
- Apple Calendar/WeChat notification for approaching DDLs
- Finish GPA trend graph generation (DIFFICULT)
