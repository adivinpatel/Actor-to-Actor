import pandas as pd
#this dataset is used to generate the hindi actors movie dataframe
castofhindimovies = pd.read_csv(r'data\castofhindimovies.csv')
hindiactorsmovies = castofhindimovies.groupby('Actor')['Movie'].agg(list).reset_index()
#movies in list by actors
hindiactorsmovies.columns = ['Actor', 'Movies']
#redefined to put actors in lists by movie
castofhindimovies = castofhindimovies.groupby('Movie')['Actor'].agg(list).reset_index()
