# campus-sustainability-game

A web app that uses gamification to promote engagement with sustainability on campus at the University of Exeter.
Streatham GO

## Build Instructions

**NOTE** for windows use `python` not `python3`

### 1. Create a virtual env

```
python3 -m venv .venv
```

### 2. Activate venv

For Mac:

```
source .venv/bin/activate
```

For Windows:

By default windows prevents you from being able to run scripts.
In order to by pass this you must first enter this command,
making sure that you are running the terminal as admin.

```
Set-ExecutionPolicy RemoteSigned
```

Then you may run this line.

```
.venv\Scripts\activate
```

After running the scripts, you may return to the original setting
by entering the following command:

```
Set-ExecutionPolicy RemoteSigned
```

### 3. Install Requirements

```
pip3 install -r requirements.txt
```

### 4. Create .env file

```
touch streatham_go/streatham_go/.env
```

open new file and add the following settings.
**NOTE** If using DEBUG=True, EMAIL\_\* settings not needed

- `DEBUG=[True|False]`
- `SECRET_KEY=[a secret key (can be anything)]`
- `GOOGLE_API_KEY=[google maps API key]`
- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_HOST_USER=streathamgo@gmail.com`
- `EMAIL_HOST_PASSWORD=[check discord]`

### 5. Migrate Database

```
cd streatham_go
python3 manage.py makemigrations
python3 manage.py migrate
```

### 6. Populate Database (IN ORDER)

```
python3 manage.py loaddata games.json
python3 manage.py loaddata buildings.json
python3 manage.py loaddate words.json
```

### 7. Run Tests (optional)

```
pytest
```

### 8. Start Dev Server

```
python3 manage.py runserver
```

## Adding new deps

If you have installed a new package via `pip3` (`pip` for windows), you MUST add this to the `requirements.txt` file

To do so (in base directory):

```
pip3 freeze > requirements.txt
```
