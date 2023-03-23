## User Guide

The code base is made up of a few main directories. The root directory, and app directories

## Root directory

```
.
|
├── ...
├── ...
└── ...
```

This directory contains markdown files (such as this one), the requirements files and the github actions files (stored in `./github`).

## The `streatham_go/` directory

```
|
└── streatham_go
    |
    └── ...
```

This directory contains the media files, base templates, app directories, pytest configurration file, json data files.

## App directories

```
|
└── streatham_go
    |
    ├── app1
    ├── app2
    ├── app3
    └── ...
```

This is were related code lives. All pages that are to do with a similar topic are put in an app. For example, the login, register, logout etc... are all in the
accounts app. Apps can be created using `python3 manage.py startapp <app_name>`. More can be read about apps on the django docs.

Apps are structured as followes:

```
app
|
├── migrations
│    └── __init__.py
├── static
│    └── app/
│       └── ...
├── templates
│    └── app/
│       └── ...
├── tests
│    ├── ...
│    └── __init__.py
├── views
│    ├── ...
│    └── __init__.py
├── __init__.py
├── admin.py
├── models.py
└── urls.py
```

each app should roughly follow the above structure. It will have a migrations folder that is handled by django. A `static/<app_name>` folder where all static images go, A `templates/<app_name>` folder where all html templates go,
a tests directory where all tests go and a views directory where all views go. each subfolder (aside from templates and static) need an `__init__.py` file to tell python it is a package. Inside this file it must import all files
that are in that directory. Each app also contains an admin file where all models are rigistered to the admin page and a urls file where a list of url routes are stored

## The `streatham_go/streatham_go` directory

```
|
└── streatham_go
    |
    ├── ...
    └── streatham_go
        ├── .env
        ├── settings.py
        └── ...
```

This directory should not really be touched. It contains a `.env` file to convifgire the app, a `settings.py` file to configure the app settings, url file to set the url routes. Other than that,
not much in this directory should be touched.

## Adding new games

To add new games, first create the game in a html webpage located in `streatham_go/app/static/app/<game_name>.html`. Next go onto the admin page and create a new game entry in the Game model for this
game. The filename should be file filename (i.e the `<game_name>.html` part of the file). Next, Go onto the buildings models and edit the desired buldings to play the new game.
