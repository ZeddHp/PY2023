import imdb

ia = imdb.IMDb()

movie = ia.get_movie('6084202')

# Get the director, writers, and stars
director = movie['director'][0]['name'] if 'director' in movie else ''
writers = [writer['name']
           for writer in movie['writers']] if 'writers' in movie else []
stars = [star['name'] for star in movie['cast'][:5]] if 'cast' in movie else []

print("Director:", director)
print("Writers:", writers)
print("Stars:", stars)

# Get the number of awards received and nominated
awards = movie.get('awards', {})
num_awards = awards.get('wins', 0)
num_nominations = awards.get('nominations', 0)

print("Number of Awards Received:", num_awards)
print("Number of Nominations:", num_nominations)

# Get the cast list
cast_list = []
for actor in movie['cast']:
    name = actor['name']
    role = actor.currentRole
    cast_list.append(f"{name} - {role}")

print("Cast List:")
for i, cast in enumerate(cast_list, 1):
    print(f"{i}. {cast}")
