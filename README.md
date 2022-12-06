#####  Simple project for a book reviews system

#####  Stack 
* fastAPI web framework
* postgresql database

##### Docker installation and run server
* `docker build -t movies_watchlist .`
* `docker run -d -p 9999:9999 movies_watchlist`
* Docker container will firstly run the automated tests and then deploy the web app
* Access the API at `localhost:9999/v1/`
* Access the API documentation at `localhost:9999/v1/documentation`


#####  Native installation and run server
* Use an environment with `python3` installed
* Open a terminal and navigate to project's main folder
* Create a python virtual environment by running the following command:
`python3.9 -m venv python_venv`
* Activate the python virtual environment by running the command:
`source python_venv/bin/activate`
* Install requirements of app by running the following command:
`pip3 install -r requirements.txt`
*  Run the server `python3 src/main.py`
*  Access the API at `localhost:9999/v1`
*  Access the API documentation at `localhost:9999/v1/documentation`





`
NOTE:
If the test suite has ran before, make sure to delete the derived sqlite3db named "books_reviews.db",
which in that case would be present in the same folder, so that the tests are not affected by any previous inserted records
`

#
#####  Who do I talk to  
* christos.karvouniaris247@gmail.com