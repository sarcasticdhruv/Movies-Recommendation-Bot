import pandas as pd
import requests
from surprise import Dataset
from surprise import KNNBasic
from surprise.model_selection import cross_validate

# Define a function to fetch movie data from the OMDB API
def fetch_movie_data(movie_ids):
    api_key = "your_omdb_api_key_here"
    base_url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "i": ",".join(map(str, movie_ids))}
    response = requests.get(base_url, params=params)
    data = response.json()
    movies = []
    for movie in data["Search"]:
        movie_data = {
            "movieId": int(movie["imdbID"].split("t")[1]),
            "title": movie["Title"],
            "year": int(movie["Year"][1:]),
        }
        movies.append(movie_data)
    return movies

# Fetch movie data from the OMDB API
movie_ids = list(range(1, 1001))
movie_data = fetch_movie_data(movie_ids)

# Create a Surprise dataset
data = Dataset.load_from_df(pd.DataFrame(movie_data), reader=Dataset.Reader(rating_scale=(1, 5)))

# Use the KNNBasic algorithm
algo = KNNBasic()

# Cross-validate the algorithm
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=3, verbose=True)

# Train the algorithm on the entire dataset
trainset = data.build_full_trainset()
algo.fit(trainset)

# Get recommendations for a user
user_id = 5
num_recommendations = 10

# Get the movies that the user has already rated
# (In this example, we assume that the user has rated all movies)
user_ratings = pd.DataFrame({"userId": [user_id] * len(movie_data), "movieId": list(range(1, 1001)), "rating": [3.0] * len(movie_data)})

# Get the IDs of the movies that the user has not rated
unrated_movie_ids = set(movie_data["movieId"]).difference(set(user_ratings["movieId"]))

# Get recommendations for the user
recommendations = algo.predict(user_id, unrated_movie_ids)
recommendations = pd.DataFrame(recommendations, columns=["movieId", "rating"])
recommendations["title"] = movie_data["title"]
recommendations = recommendations.sort_values(by="rating", ascending=False)[:num_recommendations]

print(recommendations)