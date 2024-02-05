import pandas as pd
import requests
from implicit._nearest_neighbours import NNDescent
from implicit.evaluation import precision_at_k
from implicit.datasets import movielens
import ipywidgets as widgets
from IPython.display import display

# Define a function to fetch movie data from the OMDB API
def fetch_movie_data(movie_ids):
    api_key = "your_omdb_api_key_here"
    base_url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "i": ",".join(map(str, movie_ids))
    with requests.get(base_url, params=params) as response:
        data = response.json()
        movies = []
        for movie in data["Search"]:
            movie_data =(
                "movieId": int(movie["imdbID"].split("t")[1]),
                "title": movie["Title"],
                "year": int(movie["Year"][1:]),
            )
            movies.append(movie_data)
    return movies

# Fetch movie data from the OMDB API
movie_ids = list(range(1, 1001))
try:
    movie_data = fetch_movie_data(movie_ids)
except Exception as e:
    print(f"Error fetching movie data: {e}")
    movie_data = []

# Create a dataset using the MovieLens 100k dataset
data = movielens.load_movielens_100k()

# Use the NNDescent algorithm
algo = NNDescent()

# Train the algorithm on the entire dataset
algo.fit(data.build_full_trainset())

# Create a user rating form using ipywidgets
user_id_label = widgets.Label(value="Enter user ID:")
user_id_input = widgets.IntText()
num_recommendations_label = widgets.Label(value="Number of recommendations:")
num_recommendations_input = widgets.IntText(value=10)

user_id_widget = widgets.HBox([user_id_label, user_id_input])
num_recommendations_widget = widgets.HBox([num_recommendations_label, num_recommendations_input])

def on_user_id_change(change):
    user_id = change.new
    get_recommendations(user_id, num_recommendations_input.value)

user_id_input.observe(on_user_id_change, names="value")

def on_num_recommendations_change(change):
    num_recommendations = change.new
    get_recommendations(user_id_input.value, num_recommendations)

num_recommendations_input.observe(on_num_recommendations_change, names="value")

display(user_id_widget)
display(num_recommendations_widget)

def get_recommendations(user_id, num_recommendations):
    # Get the movies that the user has already rated
    # (In this example, we assume that the user has rated all movies)
    user_ratings = pd.DataFrame({"userId": [user_id] * len(movie_data), "movieId": list(range(1, 1001)), "rating": [3.0] * len(movie_data)})

    # Get the IDs of the movies that the user has not rated
    unrated_movie_ids = set(movie_data["movieId"]).difference(set(user_ratings["movieId"]))

    # Get recommendations for the user
    user_item_matrix = data.build_user_item_matrix()
    user_item_matrix[user_id] = user_ratings["rating"].values
    recommendations = algo.recommend(user_id, user_item_matrix[user_id], N=num_recommendations)

    # Convert the recommendations to a pandas DataFrame
    recommendations = pd.DataFrame(recommendations, columns=["movieId", "rating"]).set_index("movieId")
    recommendations["title"] = movie_data.set_index("movieId")["title"]
    recommendations = recommendations.reset_index().sort_values(by="rating", ascending=False)

    display(recommendations)