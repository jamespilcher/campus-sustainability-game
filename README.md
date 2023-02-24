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

For Window:

```
.venv\Scripts\activate
```

### 3. Install Requirements

```
pip3 install -r requirements.txt
```

### 4. Create .env file

```
touch streatham_go/streatham_go/.env
```

open new file and add the following settings

- `DEBUG=[True|False]`
- `SECRET_KEY=[check discord]`
- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_HOST_USER=streathamgo@gmail.com`
- `EMAIL_HOST_PASSWORD=[check discord]`

### 5. Run Tests (optional)

```
cd streatham_go
pytest
```

### 6. Migrate Database (only need to run if you have made changes to db or first run)

```
cd streatham_go
python3 manage.py migrate
```

### 7. Start Dev Server

```
cd streatham_go
python3 manage.py runserver
```

## Adding new deps

If you have installed a new package via `pip3` (`pip` for windows), you MUST add this to the `requirements.txt` file

To do so (in base directory):

```
pip3 freeze > requirements.txt
```

## Summary of the Game

- Each day a building is selected to give out a given challenge (you find out at a certain time the day before):
  - Quiz questions
  - sustainable action
  - read an article and (locally)
- You only see the buildings challenge if your location is verified at said building (via GPS)
- You get points for the question which add to your 'xp' and total points is shown on the leaderboard

## MoSCoW

### Must have:

    - Challenges: Quiz questions
    - Promote Sustainability using gamification.
    - Location GPS.
    - Gamekeepers that monitor the state of the game.
    - Log in system.
    - A view where you can see which buildings are currently taken.
    - Leaderboards Team Scores per week.
    - Leaderboard of Team wins.
    - A list of multiple choice quiz questions.

### Should have:

    - Challenges
    - Stat tracking
    - Points decrease a factor of time since seeing the question
    - Gamekeepers monitor reports and set daily challenges.
    - A way of verifying what buildings people are in using GPS.

### Could have:

    - Challenges: Articles
    - Personified buildings
    - Different views on the leaderboard (last week, last month, total)
    - At home challenges that add to 'player points'
    - Individual/Friendship Stats, private character levelling.
    - Extra 'streak' points
    - Item shops (at certain a certain building?)
    - Double points at certain times of day

### Won't have:
