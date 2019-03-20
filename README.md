# Bokchoi

Online Recipe Book

## Description

Bokchoi is a web app built with flask.  Its purpose is to allow users find or create recipes.  Users can sign up and view recipes currently in the database and they can also create their own recipes to share with the world.  Recipes are divided into categories by ethnicity and food course ie starter/main/dessert.  There is also a live barchart showing the popularity of these categories.

## User stories
User creates Account
User signs in
User updates profile info and selects own avatar
User can view all recipes in database
User can like a recipe by other users but not their own
User can create, update or delete their own recipes
User can filter recipes based on ethnicity, ingredient category or course.  They can also filter all recipes by view count, most likes, time created

## Wireframes
https://wireframe.cc/Uassqo (small screens)
https://wireframe.cc/kuJecg (medium screens)
https://wireframe.cc/QHEGec (large screens)


### Dependencies

* HTML5, CSS3, Python Flask Framework, Bootstrap 4, Javascript, Bokeh


## Authors

Alan Smith (solanus@gmail.com)

## Deployed

https://github.com/alsmith808/bokchoi
https://bokchoi.herokuapp.com/


## Run locally
Clone or download git repo


## Development
The first thing I did was come up with an outline of how my app would appear visually so wireframes were created to represent the final app, see the wireframe links above.
For the front end I decided to use Bootstrap 4 due to its flexibility and wide community support/resources.
Bokchoi was chosen as the app name as its a particular favorite vegetable of mine and under represented. I went with a green theme in my front end to match that particular vegetable.
The next stage was to come up with a db schema.  See below for Schema details.  
In my local development environment I used sqlite3 for adding posts to the database.  
Basic authentication and pagination was added at the beginning of the project.
I then began adding various different posts and users making sure to exhaust all available options for posts
A user likes post function was then added, this function blocks users from liking their own recipes as I dont see the point in that, also they can only  like a recipe once.  An association table between User and Post was created to enable this functionality.  Routes were then created to filter all the results in many different combinations on the home page.  Depending on what the user selects from the main dropdown in the navigation they are then presented with another filter button with more options.  I made some javascript functions in order to make this work.  To enable this functionality I created arrays with keywords which are cross referenced with the page titles, based on these arrays of keywords my functions can determine what filter options to populate into my dropdown button.  There is also routes for every user, so when a users name is clicked in one of their posts, the user will be shown a list of all that users recipes.  
For data visualisation I explored a few different options but I decided that the Bokeh library would suit my needs well.  To implement this I used their documentation and took an example graph and altered it to fit my needs.  I then created a function to pull the data from my database which updates everytime a post is added or updated.  


## Pseudocode...
Click on new games
User inputs number of players between 1 and 5
User/Users input their name as unique identifier
User is presented with Fixture n
User inputs answer with forms
If answer is incorrect player gets second attempts
On correct answer or second wrong answer user goes to next Fixture
If last question in 1 player mode game finishes and score page is shown with option to view leaderboaerd
If multiplayer mode the next player then goes through the questions inputing their answers
When all players have enter answers game finishes, winner/draw screen is presented showing each players score


## Testing_Automated



## Testing_Manual
The app was continuosly tested manually in the browser throughout the lifecycle of the project.
It has also been made as responsive as possible and has been tested on various screen sizes and mobiles.


## Version History

* 0.1
    * Initial Release

## License

MIT

## Acknowledgments

* Corey Schafer (Tutorials on Flask)
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
