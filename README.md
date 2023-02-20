# campus-sustainability-game

A web app that uses gamification to promote engagement with sustainability on campus at the University of Exeter.
Streatham GO

## Build Instructions

### 1. Create a virtual env

```
python3 -m venv .env
```

### 2. Activate venv

For Mac:

```
source .env/bin/activate
```

For Window:

```
.env\Scripts\activate
```

### 3. Install Requirements

```
pip3 install -r requirements.txt
```

### 4. Run Tests (optional)

```
cd streatham_go
pytest
```

### 5. Migrate Database (only need to run if you have made changes to db or first run)

```
python3 manage.py migrate
```

### 5. Start Dev Server

```
python3 manage.py runserver
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

    -
