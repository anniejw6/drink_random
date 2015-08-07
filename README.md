# Numb3rs Randomizer

A flask application to help implement randomization for a Numb3rs-themed drinking game

Production: [numb3rs-rand.herokuapp.com](http://numb3rs-rand.herokuapp.com/) (In theory, this should always work.)

Staging: [numb3rs-rand-stage.herokuapp.com](http://numb3rs-rand-stage.herokuapp.com/) (Probably is broken.)

```python run.py ```

# Setup 
Create new virtual environment
``` 
python -m venv flask
```
Activate virtualenv
```
source flask/bin/activate
```
run `requirements.txt`
```
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt 
#alternatively: 
`cat requirements.txt | xargs -n 1 pip install`
```

# Databases
## Migrating
```
# Initialize
python managedb.py db init
# AFTER EVERY DATABASE CHANGE
python managedb.py db migrate
python managedb.py db upgrade
```

Download http://postgresapp.com/
Add to bash_profile: http://postgresapp.com/documentation/cli-tools.html
```
createdb appdb
python
from app import db
db.create_all()
quit()
```

# Heroku
Install Heroku toolbelt
```
heroku login
heroku create APP_NAME
git remote add REMOTE_NAME git@heroku.com:APP_NAME.git
```
First time you push
```
git push REMOTE_NAME master
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:promote HEROKU_POSTGRESQL_COLOR
heroku run python
from app import db
db.create_all()
quit()
```
Subsequent times
```
git push REMOTE_NAME master
```

