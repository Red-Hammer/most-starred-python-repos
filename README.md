# Top GitHub Python Repos

## Setup:

- Open a terminal in the project directory and type the command `python3 -m venv .venv`
- Then enter the virtual environment with `source .venv/bin/activate` (`.venv\Scripts\activate` on Windows)
- From now on, any terminal commands should be run in the venv environment
- To get all the packages, run `pip install -r requirements.txt`
- Create a `.env` file in your base directory and add in:


    SECRET_KEY=your-secret-key-here
    
    FLASK_APP=app.py

### Database Setup:

- To get the database initialized and up to the current version, run `flask db upgrade` in your terminal.

### Running the Application

- Run `flask run` in your terminal and navigate to http://127.0.0.1:5000/
- You will see an empty repository table. Go ahead and populate the data by clicking the 'Refresh Top Repos Button'
  - Without GitHub authentication, we can only run this 10 times per minute due to GitHub's rate limit.
- You've got data now! Hooray! You can navigate to a repository's details page by clicking on its name in the table.

### Pytest Unit Testing

Once you complete the above steps, you can run the pytest unit tests by running `pytest` in your terminal

## Architecture Decisions and Rationale

For this project, I used the Flask Application Factory Pattern detailed
[here](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/). I find this pattern more readable than a one
module Flask app, and it allows for greater logical abstraction. I used SQLite, SQLAlchemy, and Alembic for the
database, ORM, and migrations tool, respectively. SQLite is quick to stand up and has everything I needed for a small
database. SQLAlchemy and Alembic are the tools I'm most familiar with. I also find them to be quite powerful and easy to
use.

I make use of Flask 2.0's asynchronous functionality whenever a method interacts with the database.

I placed all the GitHub Search API calling and updating functionality into the `github` directory. The routes file
contains the view function that queries the GitHub Search API for the top 100 Python repositories by star rating. It
checks for a rate-limit error. If there is one it handles the exception gracefully and passes a warning to the user. If
the rate limit has not been reached, the response is converted to json and then passed into the request_interface
function. The request_interface orchestrates the cleaning and finally writing of the data to the db. The data_cleaner
private function pulls all the json records into one Pandas DataFrame, then, using pandas builtin methods, it trims the
data down to the desired columns and renames those columns to more user-friendly names. The formatted data is then
passed into the data_writer private function. This function pulls the records back out of the DataFrame and into a list
of dictionaries. It then checks each record to see if its repository ID already exists in the database. If it does, the
function grabs that database record via a SQLAlchemy Model and updates its fields using the new source. If the record
does not exist, a new database record is created and written. In each of these cases, the 'last_push_date' and '
created_date' fields are converted out of ISO 8601 datetime strings and into datetime.datetime objects using dateutil's
isoparser.

The view functionality for this project was built using Flask's Jinja2 templates with a lot of help from the
[DataTables.net](https://datatables.net/) jQuery plug-in. Even though our results are small, the pagination, and Ajax
extensibility it offers are fantastic. 
