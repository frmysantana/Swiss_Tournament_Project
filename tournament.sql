-- Table definitions for the tournament project.--

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	ID SERIAL PRIMARY KEY,
	Name TEXT);

ALTER SEQUENCE players_id_seq RESTART WITH 1;


--This function sets the round number based off of how many total matches have been played.
--It also restarts the match number once a new round has begun. For example, a tournament with ten players
--would have five matches per round, so the match number would only go up to 5 before the round number
--is incremented by one. At this point, the match number would then be reset to 1.
CREATE FUNCTION roundNumber() RETURNS INTEGER AS $currentRound$
DECLARE
currentRound INTEGER;
matchesSoFar INTEGER := COUNT(*) FROM matches;
maxMatches INTEGER := COUNT(*)/2 FROM players;
BEGIN
currentRound := matchesSoFar/maxMatches + 1;
IF currentRound > 1 AND matchesSoFar = maxMatches*(currentRound - 1) THEN
ALTER SEQUENCE matches_match_seq RESTART WITH 1;
END IF;
RETURN currentRound;
END;
$currentRound$ LANGUAGE plpgsql;

CREATE TABLE matches (
	Round SMALLINT DEFAULT roundNumber(), 
	Match SERIAL,
	Winner INT REFERENCES players(ID) ON DELETE CASCADE,
	Loser INT REFERENCES players(ID) ON DELETE CASCADE,
	CHECK (Winner<>Loser),
	PRIMARY KEY (Round, Match));


--Displays total wins for each player
CREATE VIEW wins_count AS
SELECT players.id, players.name, COUNT(matches.Winner) AS total_wins
FROM players LEFT JOIN matches
ON players.id = matches.Winner
GROUP BY players.id ORDER BY players.id;

--Displays total losses for each player
CREATE VIEW losses_count AS
SELECT players.id, players.name, COUNT(matches.Loser) AS total_losses 
FROM players LEFT JOIN matches ON players.id = matches.Loser 
GROUP BY players.id ORDER BY players.id;

--Counts total matches
CREATE VIEW matches_count AS
SELECT players.id, players.name, COUNT(matches) AS total_matches
FROM players LEFT JOIN matches
ON players.id = matches.winner OR players.id = matches.loser
GROUP BY players.id;

--Gives all needed information for the playerStandings function in tournament.py
CREATE VIEW standings AS
SELECT wins_count.id, wins_count.name, wins_count.total_wins, matches_count.total_matches
FROM wins_count JOIN matches_count ON wins_count.id = matches_count.id
ORDER BY wins_count.total_wins DESC;
