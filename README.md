# ManageBac-Plus
> Since ManageBac **SUCKS**, we decided to make a new one. A better one. *This, is ManageBac Plus.*

Just a simple python Flask webapp built around ManageBac that adds a lot of useful functions to it.

## Table of contents
<!-- TOC -->
* [ManageBac-Plus](#managebac-plus)
  * [Table of contents](#table-of-contents)
  * [Features](#features)
  * [Usage](#usage)
    * [Prerequisites](#prerequisites)
    * [Launch](#launch)
  * [Current limitations](#current-limitations)
  * [TODOs](#todos)
<!-- TOC -->

## Features
- A convenient way of checking your GPA
- GPA calculator for midterms and finals
- GPA calculator for marginal tasks (One extra task in a given category)
- Graphs for all those calculations
- An online platform for sharing Mochi decks as well as notebooks

## Usage
### Prerequisites
Before launching the app, make sure you have the **latest version of MySQL** and the **required python libraries** installed.

Then, in your **MySQL terminal**, run the following commands to initialize the databases:
```shell
CREATE DATABASE credentials;
CREATE DATABASE scores;
CREATE DATABASE mochi;
CREATE DATABASE notebooks;
```
To install the required python libraries, run the following command in your terminal:
```shell
python -m pip install -r requirements.txt
```
### Launch
To launch the app, make sure you have all the prerequisites installed, then simply run the following command in your terminal:
```shell
python app.py
```
The app will be deployed at `http://localhost:8080/` and will be open to LAN by default.

## Current limitations
We're all just high school students and making perfect dynamic websites is obviously not our daily job. Hence I'll have to admit that there are many limitations to the current website:
- Lack of encryption for personal credentials
- Unsafe file upload system
- Horrible database schema that minimizes efficiency
- Tons of hidden bugs not fixed
- Code inconsistency
- Funding problems for future server deployment

Just to name a few. However, we are also actively working on finding solutions to these problems, and I'm confident that this process won't take long.

## TODOs
- Add login support for Microsoft accounts
- Update frontend design
- Fuzzy searching system (Currently only exact search)
- Simply use GET requests for GPA data
- GPA trend graph generation
- Remove/Modulize repeating code
- All kinds of encryptions for the credentials database (Hashing?)
