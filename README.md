# Yatube Social Network

This is an application with a user interface. It implements user registration and authentication. Authorized user can write and edit his posts (text + photo), write comments to the posts, subscribe to the pages of other users. Posts can be linked to a thematic group. Available for viewing: 
- a list of all posts on the home page,
- list of posts of a certain author, 
- list of the posts of a certain topic group,
- authorized user's newsfeed - posts by authors from subscriptions.

Each page displays the 10 most recent posts, pagination is implemented. The list of posts on the main page is kept in the cache and is updated every 20 seconds.

Tests are written for the whole project with the help of Unittest library.
```
YaTube/yatube/posts/tests/
```

## Tech Stack:
- Python 3.9
- Django 2.2
- Unittest

## How to start a project

Clone the repository and go to it on the command line:

```
git clone https://github.com/maxuver/Social_network_Yatube.git
```

```
cd yatube
```

Create and activate a virtual environment:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Install dependencies from the requirements.txt file:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Perform migrations:

```
python manage.py migrate
```

Start the project:

```
python manage.py runserver
```
