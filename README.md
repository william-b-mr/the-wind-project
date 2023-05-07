# the-wind-project

## Baseline simulation
- __Includes:__
    - 1) Fetching data from an external weather API
    - 2) Launching 2 services, one for a PostgreSQL DB and another for a Grafana instance (visualization)
    - 3) Populating the DB with these data - after simple preprocessing operations
    - 4) Populating the Grafana instance with data extracted from the DB
    - 5) Housekeeping
## Requirements:
- 1) Have docker installed in your system
- 2) Have the following libraries installed in your python environment (note: install them via the shell)
    - pip install psycopg2-binary
    - pip install pandas
## Instructions:
- 1) Using a the shell command line, go to the __docker__ folder
- 2) Run __docker-compose up -d__ from the shell
- 3) Run __docker ps__: you should see 2 containers up and running:
    - grafana (our frontend service)
    - postgres (our database service)

- 4) Run __python3 main.py__ from the shell

- 5) Go to __http://localhost:3000__, then use __admin + admin__ as the combination of __username + password__ and check your dashboards. You should see 3 basic timseries visualizations with the data gathered from the API from a certain period (feel free to add more visuals)

- 6) After finishing, run __python3 drop.py__ (this will cleanup the database)
