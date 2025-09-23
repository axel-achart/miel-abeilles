import pandas as pd
from beehive import generate_population

#init the data
flowers_df = pd.read_csv('data/flowers.csv')
flower_positions = list(zip(flowers_df['x'], flowers_df['y']))
hive_position = (500,500)

bees = generate_population(100, flower_positions, hive_position)