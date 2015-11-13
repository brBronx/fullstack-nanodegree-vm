#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players")
    num = int(c.fetchone()[0])
    if num == None:
        num = 0
    else:
        num
    DB.close
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (name, wins, losses, matches, active) values (%s, %s, %s, %s, %s)",  (name, 0, 0, 0, True))  
    DB.commit()
    DB.close()


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
    DB = connect()
    c = DB.cursor()
    c.execute("select p.id, name, wins, matches \
        from players p left outer join matches m on p.id = m.id \
        order by wins")
    standings = []
    for row in c:
        tup = (row[0], row[1], row[2], row[3])
        standings.append(tup)
        tup = ()
    DB.close()  
    return standings   


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("update players set wins = wins + 1, matches = matches + 1 where id = '%s'", (winner,))
    c.execute("update players set losses = losses + 1, matches = matches + 1 where id = '%s'", (loser,))
    c.execute("insert into matches (winner, loser) values (%s, %s)", (winner, loser))
    DB.commit()
    DB.close()    
 
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

#   Rows are selected in pairs.  THe first row is delivered by the 'for' loop.  THe second row of
#   the pair comes from the 'c.fetchone' statement.  Each pair of rows is inserted into the tuple 
#   'match'.  The 'match' tuple is then appended to the 'matches' list which is returned.
#   The 'matches' list contains a tuple for each pair of players for the next round of the match.    
    DB = connect()
    c = DB.cursor()
    c.execute("select id, name from players order by wins")
    matches = []
    for row in c:
        match = ()
        id1 = row[0]
        name1 = row[1]
        row = c.fetchone()
        id2 = row[0]
        name2 = row[1]      
        match = (id1, name1, id2, name2)
        matches.append(match)
    
    DB.close()  
    return matches

