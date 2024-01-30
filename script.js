const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const movieContainer = document.getElementById("movie-container");
const recommendationContainer = document.getElementById("recommendation-container");

// Replace this with your own API key
const apiKey = "your_api_key_here";

let searchHistory = [];

searchForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const searchTerm = searchBox.value.trim();

  if (!searchTerm) {
    return;
  }

  searchBox.value = "";

  try {
    const response = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${searchTerm}`);
    const data = await response.json();

    if (data.results.length === 0) {
      throw new Error("No movies found.");
    }

    displayMovies(data.results);
    searchHistory.push(searchTerm);
    saveSearchHistory();
  } catch (error) {
    alert(error.message);
  }
});

function displayMovies(movies) {
  movieContainer.innerHTML = "";

  movies.forEach((movie) => {
    const movieElement = document.createElement("div");
    movieElement.classList.add("movie");

    const moviePoster = document.createElement("img");
    moviePoster.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
    movieElement.appendChild(moviePoster);

    movieContainer.appendChild(movieElement);
  });
}

function displayRecommendations() {
  recommendationContainer.innerHTML = "";

  const recommendations = getSimilarMovies(searchHistory[searchHistory.length - 1]);

  if (recommendations.length === 0) {
    const noRecommendations = document.createElement("p");
    noRecommendations.textContent = "No recommendations available.";
    recommendationContainer.appendChild(noRecommendations);
    return;
  }

  recommendations.forEach((movie) => {
    const movieElement = document.createElement("div");
    movieElement.classList.add("movie");

    const moviePoster = document.createElement("img");
    moviePoster.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
    movieElement.appendChild(moviePoster);

    recommendationContainer.appendChild(movieElement);
  });
}

function getSimilarMovies(movie) {
  // This is a placeholder function. You can replace it with your own algorithm.
  return searchHistory.filter((item) => item !== movie).slice(0, 10);
}

function saveSearchHistory() {
  localStorage.setItem("searchHistory", JSON.stringify(searchHistory));
}

function loadSearchHistory() {
  const storedHistory = localStorage.getItem("searchHistory");

  if (storedHistory) {
    searchHistory = JSON.parse(storedHistory);
  }
}

loadSearchHistory();
displayRecommendations();