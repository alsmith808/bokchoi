# Bokchoi

Online Recipe Book

## Description

Bokchoi is a web app built with flask.  Its purpose is to allow users find or create recipes.  Users can sign up and view recipes currently in the database and they can also create their own recipes to share with the world.  Recipes are divided into categories by ethnicity and food course eg starter/main/dessert.  There is also a live barchart showing the popularity of these categories.


## User stories
User creates Account
User signs in
User updates profile info and selects own avatar
User can view all recipes in database
User can like a recipe by other users but not their own
User can create, update or delete their own recipes
User can filter recipes based on ethnicity, ingredient category or course.  They can also filter all recipes by view count, most likes, time created
User signs out


## Wireframes
https://wireframe.cc/Uassqo (small screens)
https://wireframe.cc/kuJecg (medium screens)
https://wireframe.cc/QHEGec (large screens)


## Database Schema
Many different styles of complexity were explored and eventually I decided to design a relatively simple schema. In my research into SQL vs NoSQL databases I found the development community seems to lean towards the conventional relational database approach for a project such as this so I went with a relational database approach.  
The three most important tables are User, Post and Ingredients so I concentrated my design around these tables and the relationships between them.  I also decided to have a table for view counts.  Two association tables were needed to represent many-to-many relationships for 'User likes Post' and also Post/Ingredients. In order to make application as flexible as possible I enabled a lot of options for users when creating a Post. To summarize the user selects what course the recipe is, its ethnicity, its ingredients and indicate if its vegan, vegetarian, meat based or contains nuts.  Users can also like a recipe that is not their own.  See ER Diagram in project root. (bokchoi_ER.png)


### Dependencies

* HTML5, CSS3, Python Flask Framework, Bootstrap 4, Javascript, sqlite3, Bokeh


## Authors

Alan Smith (solanus@gmail.com)

## Deployed

https://github.com/alsmith808/bokchoi
https://bokchoi.herokuapp.com/


## Run locally
Make sure your version of python is 3.6 or higher as new syntax and features such as f-strings are used
Install Pipenv and follow their documenation to create a virtual environment,
see https://pipenv.readthedocs.io/en/latest/ for documentation
Clone or download this repo into virtual environment
Navigate to root of project and open command line
Install dependencies: pipenv install -r requirements.txt
Set up your secret key in your own environment
Init and migrate database:
  pipenv run python manage.py db init
  pipenv run python manage.py db migrate
  pipenv run python manage.py db upgrade
To run project: pipenv run python run.py



## Development
The first thing I did was come up with an outline of how my app would appear visually so wireframes were created to represent the final app, see the wireframe links above.
For the front end I decided to use Bootstrap 4 due to its flexibility and wide community support/resources.
Bokchoi was chosen as the app name as its a particular favorite vegetable of mine and under represented. I went with a green theme in my front end to match that particular vegetable.
The next stage was to come up with a db schema.  See below for Schema details.  
In my local development environment I used sqlite3 and migrated to postgres for Heroku production.  
Basic authentication and pagination was added at the beginning of the project.
I then began adding various different posts and users making sure to exhaust all available options for posts in order to manually test the various options and filters.
A user likes post function was then added, this function blocks users from liking their own recipes as I dont see the point in that, also they can only like a recipe once.  An association table between User and Post was created to enable this functionality.  Routes were then created to filter all the results in many different combinations on the home page.  Depending on what the user selects from the main dropdown in the navigation they are then presented with another filter button with more options.  Javascript functions were created in order to make this work.  To help enable this functionality I created arrays with keywords which are cross referenced with the page titles, based on these arrays of keywords my functions can determine what filter options to populate into my dropdown button.  There is also routes for every user, so when a users name is clicked in one of their posts, the user will be shown a list of all that users recipes.  
For data visualization I explored a few different options but I decided that the Bokeh library would suit my needs well.  To implement this I used their documentation and took an example graph and altered it to fit my needs.  I then created a function to pull the data from my database which updates every time a post is added or updated.  Each post has a post count and like count represented with Material icons in the individual post view.  Hovering over recipe images on the home page also reveals a short recipe description.


## Testing_Automated
tests.py located in root of Project
to run tests, at root of project open command line and enter..'pipenv run python tests.py'
Unittest's created to text the accurate functionality of creating user account, creating a post and user liking a post.


## Testing_Manual
This app has been rigorously tested throughout the entire lifespan of the project both in my local environment and also on the live Heroku version. Any new front or back end code was tested and fixed if needed throughout.  Bootstrap helped a lot in making sure everything scaled down with minimal changes thanks to the rows and column classes and also the flexbox utilities.  For any additional changes not satisfied by changing column sizes was implemented using Media Queries for various different screen sizes.  For example card dimensions had to be altered in media queries to improve the UI, and also drop downs had to be altered on mobile views.  Any changes to db schema were continuously checked and bugs fixed before moving on.  DB Browser for sqlite helped to give a visual representation of my tables and data.  My Bokeh chart as well as showing stats also gave me the added bonus of confirming posts were being added as they transform on every entry/update/delete.  UI was tested on many different screen sizes and devices to make sure the app adjusts to all user devices.


## Version History

* 0.1
    * Initial Release

## License

MIT

## Acknowledgments

* Corey Schaefer (Tutorials on Flask)
https://www.youtube.com/user/Corey Schaefer

* Miguel Grinberg Flask Mega Tutorial
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers

* Anthony at Pretty Printed
https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ

* David Hamann
https://davidhamann.de/2018/02/11/integrate-bokeh-plots-in-flask-ajax/

* Anirudha Bhowmik registration form
https://bootsnipp.com/snippets/or3WG

* Cards
https://tympanus.net/Development/HoverEffectIdeas/index.html
