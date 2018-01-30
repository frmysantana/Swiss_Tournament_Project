# Completed as the final project of the Backend Developer path for the Intro to Programming nanodegree on Udacity.com.

# Tournament

The files tournament.sql, and tournament.py create a PostgreSQL database and a Python module, respectively, that keeps track 
of the players and matches in a Swiss-system tournament. In this system, players are not eliminated, and matches are between
players with as close a win-record as possible. Matches are 1-on-1 and the code was written assuming that an even-number of
players are involved. Lastly, tournament_test.py (given to me by Udacity) contains unit tests on the code that one may modify for their own tournaments.

## Needed Software

In order to use this code, one needs PostgreSQL (at least version 9.3.15)  installed into their virtual machine as well as
Python (at least version 2.7.9).

## Installation

To install, simply unzip the files into your virtual machine CLI tool (e.g. vagrant) folder as "tournament". 

## Usage
With the files unzipped, the database can be set up by:
1. Opening a CLI and navigating to your virtual machine directory. Then start and connect to a virtual machine. 
2. With the machine up, change directories into the tournament directory. 
3. Go into psql by entering `psql` into the command line
4. Enter `\i tournament.sql` to import the sql file to psql. This will setup all of the needed database schema. 

To run the unit tests, enter `python tournament_test.py` from the virtual machine command line.
