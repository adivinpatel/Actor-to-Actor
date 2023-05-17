from flask import Flask, render_template, request
from generatedataframe import hindiactorsmovies,castofhindimovies
#This data was generated using several moves that all could not be saved due to runtime issues on the program, they are described below
#Step 1: Converted every gz file in IMDb to a csv
#Step 2: Took title.akas.tsv and put only movies in Hindi from region India
#Step 3: Took title.basics.tsv.gz to get the movies (not shows or episodes) from 2010 to 2023
#Step 4: Combined both of the data from steps 2 and 3 together to shorten the list and got the ids of only hindi films from 2010 to 2023
#Step 5: Filtered out title.principals.tsv.gz using only the ids from the last dataset to reduce nearly 2.3GB in memory usage (massive dataset)
#Step 6: Got the names of the actors from step 5 using name.basics.tsv.gz
#Step 7: Used the name ID and movie ID to acquire all the data
#Step 8: Deleted columns we don't need and left with movie name and cast member
#Step 9: Grouped all the movies a specific actor has acted in to one list and corresponded it to an actor in generatedataframe.py
#Step 10: Generated Final Dataset called hindiactorsmovies.csv (this is for show we import our dataframes from generatedataframe)
def numberofconnections(actor1, actor2, hindiactorsmovies):
    if (actor1 in hindiactorsmovies['Actor'].tolist()) & (actor2 in hindiactorsmovies['Actor'].tolist()):
        index1 = hindiactorsmovies[hindiactorsmovies['Actor'] == actor1].index[0]
        value1 = hindiactorsmovies.loc[index1, 'Movies']
        index2 = hindiactorsmovies[hindiactorsmovies['Actor'] == actor2].index[0]
        value2 = hindiactorsmovies.loc[index2, 'Movies']
        common_movies = ''
        #testing for direct connection
        for movie in value1:
            if movie in value2:
                common_movies += movie+", "
        if len(common_movies) > 0:
            common_movies = common_movies[:-2]
            return common_movies
        else:
            #testing for a degree 2 indirect connection
            returnval = []
            for movie in value1:
                castid = castofhindimovies[castofhindimovies['Movie'] == movie].index[0]
                cast = castofhindimovies.loc[castid,'Actor']
                for actor in cast:
                    idmov = hindiactorsmovies[hindiactorsmovies['Actor'] == actor].index[0]
                    value = hindiactorsmovies.loc[idmov,'Movies']
                    for movie in value:
                        if movie in value2:
                            returnval.append(actor+" in "+movie)
                            return returnval
            for movie in value2:
                castid = castofhindimovies[castofhindimovies['Movie'] == movie].index[0]
                cast = castofhindimovies.loc[castid,'Actor']
                for actor in cast:
                    idmov=hindiactorsmovies[hindiactorsmovies['Actor']==actor].index[0]
                    value = hindiactorsmovies.loc[idmov,'Movies']
                    for movie in value:
                        if movie in value1:
                            returnval.append(actor+" in "+movie)
                            return returnval
            return -1
    else:
        #no direct or degree 2 connection
        return -1

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    actor1 = request.form['actor1']
    actor2 = request.form['actor2']
    result = numberofconnections(actor1, actor2, hindiactorsmovies)
    if isinstance(result, str):
        return render_template('result.html', actor1=actor1, actor2=actor2, movies=result, connected=True,two=False)
    elif isinstance(result,list):
        return render_template('result.html',actor1=actor1,actor2=actor2,movies = result, connected=True,two=True)   
    else:
        return render_template('result.html', actor1=actor1, actor2=actor2, connected=False,two=False)

if __name__ == '__main__':
    app.run()