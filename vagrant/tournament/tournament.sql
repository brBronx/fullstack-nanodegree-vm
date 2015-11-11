-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS players;
Create table players (name TEXT,
					 wins integer,
					 losses integer,
					 matches integer,
					 active boolean,
                     id SERIAL PRIMARY KEY );


DROP TABLE IF EXISTS matches;
Create table matches (winner integer,
					  loser integer,
                      id SERIAL PRIMARY KEY );
