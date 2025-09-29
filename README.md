
                Happy data engineering!

Cricket Data Loader: Series & Matches Table
This project automates the ingestion, enrichment, and audit of cricket series and match data into a PostgreSQL database using the Cricbuzz RapidAPI endpoints. It supports full coverage from January 1, 2024, through today, including international, league, domestic, and women's cricket, with resilient handling of missing or ambiguous data.

Features
•	Automated ingestion: Fetches live, recent, and archived matches and series from the Cricbuzz API across all cricket 

categories.
•	Data enrichment: Resolves missing host/venue country, cleans ambiguous fields, and ensures data completeness for relational 

integrity.
•	Flexible schema: Table design for series and matches retains detailed metadata including toss/winner info, match format, and 

venue attributes.
•	Post-processing cleanup: Fills empty toss/winner and country fields post-ingest for high-quality analytics.
•	Auditing/reporting: Prints summary statistics and missing-data audits to assist coverage tracking and troubleshooting.
•	Resilient error handling: Retries API fetches and adapts to various API response shapes.

Table Schema

series

Column	Type	Description
series_id	BIGINT	Unique series identifier
series_name	TEXT	Series name/title
series_type	TEXT	Category/type of series
start_date	DATE	Series start date
end_date	DATE	Series end date
host_country	TEXT	Host country
match_format	TEXT	Format (Test/ODI/T20/etc)
total_matches	INT	Total scheduled matches
created_at	TIMESTAMP	Row creation timestamp


matches

Column	Type	Description
match_id	BIGINT	Unique match identifier
series_id	BIGINT	FK to series(series_id)
match_desc	TEXT	Match description
match_format	TEXT	Format (Test/ODI/T20/etc)
match_type	TEXT	Type (International/League/Tour)
start_date	TIMESTAMP	Match start datetime
end_date	TIMESTAMP	Match end datetime
state	TEXT	Current match state
status	TEXT	Status (e.g., 'won by', 'draw')
team1_id	BIGINT	Team 1 ID
team1_name	TEXT	Team 1 name
team2_id	BIGINT	Team 2 ID
team2_name	TEXT	Team 2 name
venue_id	BIGINT	Venue ID
venue_name	TEXT	Venue name
venue_city	TEXT	Venue city
venue_country	TEXT	Venue country
toss_winner_id	BIGINT	Team ID who won the toss
toss_decision	TEXT	Decision after toss
winner_team_id	BIGINT	Winning team ID
winner_team_name	TEXT	Winning team name
win_by_runs	INT	Margin by runs
win_by_wickets	INT	Margin by wickets
win_by_innings	BOOLEAN	True if win by innings
created_at	TIMESTAMP	Row creation timestamp

Setup Instructions

Prerequisites
•	PostgreSQL (v13+ recommended) running locally
•	Python 3.8+ and pip
•	Cricbuzz RapidAPI key (add to HEADERS config)
•	Install packages: psycopg2, requests
        pip install psycopg2 requests

Database Configuration

Update the DB dictionary in your code with your PostgreSQL connection credentials.

API Key

Set your RapidAPI key in the HEADERS dictionary. You can sign up for the Cricbuzz API on RapidAPI.

Usage
     Run the script directly:
            python cricket_loader.py

The script will:
•	Ensure required tables exist
•	Load current live and recent matches
•	Load archived series and matches from all major categories (international, league, domestic, women)
•	Post-process the database to clean up blanks and ambiguous values
•	Audit dataset coverage and print summary statistics

Code Organization
•	connect() — database connection utility
•	api_get() — API request function with retry logic
•	ensure_tables() — table creation DDL
•	upsert_series() / upsert_match() — insert or update series/match records
•	ingest_live_recent() — fetches and loads live/recent match data
•	ingest_archives_all() — paginates through archived series by category
•	post_clean() — cleans and fills missing data
•	audit() — prints data coverage and audit results
•	main() — entry point orchestrating full ingestion and audit

Maintenance & Extensibility
•	Adjust date filters to customize coverage window
•	Add new categories or extra scraping enrichers as needed
•	Extend schema for player stats, events, or additional metadata (recommend new tables for scalability)

Licensing and Attribution
This code is for educational and non-commercial use. Respect Cricbuzz RapidAPI usage limits and policies when collecting data. Modify API key and database credentials before deployment.

