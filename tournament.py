#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def executeQuery(query):  #query
    """Completes the passed query, including commiting the changes or returning the resulting table.

    Args: 
    	query: the string representation of the sql query to be completed. If parameters have to be included, the
    			string and parameters should be in a tuple.

    Returns: 
    	The resulting table of a select query or None in the case of a delete, insert, or update query."""
    if isinstance(query, tuple):
    	queryPhrase = query[0]; parameters = query[1]
    	conn = psycopg2.connect("dbname=tournament"); cursor = conn.cursor()
    	cursor.execute(queryPhrase, parameters)
    else:
    	queryPhrase = query
    	conn = psycopg2.connect("dbname=tournament"); cursor = conn.cursor()
    	cursor.execute(queryPhrase)
    queryWords = queryPhrase.split(' ')
    if queryWords[0].upper() == 'SELECT':
       result = cursor.fetchall()
    if queryWords[0].upper() in ['UPDATE','TRUNCATE','INSERT']:
       conn.commit(); result = None
    conn.close()
    return result

def deleteMatches():
    """Remove all the match records from the database."""
    executeQuery("TRUNCATE matches RESTART IDENTITY;")
    
def deletePlayers():
    """Remove all the player records from the database."""
    executeQuery("TRUNCATE players RESTART IDENTITY CASCADE;")

def countPlayers():
    """Returns the number of players currently registered."""
    for row in executeQuery("SELECT COUNT(*) FROM players;"):													
    	number_of_players = row[0]
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    executeQuery(("INSERT INTO players (name) VALUES (%s)", (name,)))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return executeQuery('SELECT * FROM standings;')

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    executeQuery(("INSERT INTO matches (Winner, Loser) VALUES (%s, %s)", (winner, loser,)))
	 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    roster_length = countPlayers(); i = 0; pairings = [];
    if roster_length % 2 != 0:
    	raise ValueError("There must be an even number of players. There are {c}".format(c=roster_length)) #Why does period have to be after closing quote for "format" to work?
    player_list = playerStandings()

    # Goes through the list of players to make match pairings and put into the pairings list as an element.
    while i < roster_length - 1:																	
    	match = player_list[i][0:2] + player_list[i+1][0:2]
    	pairings.append(match); i += 2;
    return pairings
