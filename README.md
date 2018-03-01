# LOGS ANALYSIS PROJECT

## Project Description

This project is a part of [Udacity's Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
The project connects to a database named "news" for some news website. The `logs_analysis.py` file queries the DB using psycopg2 and prints out the results in tabular format.

The file quries the DB for:
1. 3 most popular articles of all time
2. Most popular author of all time
3. Days for which more than 1% of requests failed.

### Prerequisites

The project requires
* Python 2.7
* PostgreSQL 9.5.6
* psycopg2 2.7.1

### Installation and Set up

* Download and set up the Virtual Machine for the project.
* Use `vagrant ssh` to log into the machine.
* In case the machine doesnt has `pip`:

```
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install python-pip
```
* Install psycopg2
```
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

### Database Set up

From the commandline, `cd` into the project folder.
```
psql -d news -f newsdata.sql
```

### Third Party Libraries
The data is printed using the [PrettyTable](https://code.google.com/archive/p/prettytable/) library, which should be installed using
```
 sudo easy_install prettytable
```

### How to Run
Once the Database has been setup, use the following command to access DB console.
```
psql -d news
```
To run the project, type from the command line
```
python logs_analysis.py
``` 

### Database Views
Create the following view for the code to run properly.

```
CREATE VIEW article_counter as SELECT substring(path, 10) AS slug, count(*) AS count FROM log WHERE path LIKE '/article%' AND status='200 OK' GROUP BY slug ORDER BY count;

```
