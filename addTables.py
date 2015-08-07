import os
import pandas as pd
from app import models, db

basedir = os.path.abspath(os.path.dirname(__file__))

#print(os.path.join(basedir, 'static/art_api/art_list.csv'))
art_list = pd.read_csv(os.path.join(basedir, 'app/static/art_api/art_list.csv'))
#print(art_list.head())

# Add to database
for index, row in art_list.iterrows():

	a = models.Art(row['primary_image_id'], row['title'])
	db.session.add(a)

db.session.commit()