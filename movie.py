import pandas as pd
import numpy as np
import ast
import pickle

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# Data Preprocessing Functions
# -------------------------------
def load_data(movies_path: str, credits_path: str) -> pd.DataFrame:
    """Load and merge movie + credits datasets."""
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    return movies.merge(credits, on="title")


def parse_name_list(obj: str) -> list[str]:
    """Extract names from a JSON-like string column."""
    return [i["name"] for i in ast.literal_eval(obj)]


def parse_top_cast(obj: str, top_n: int = 3) -> list[str]:
    """Extract top N cast members."""
    names = []
    for idx, i in enumerate(ast.literal_eval(obj)):
        if idx < top_n:
            names.append(i["name"])
        else:
            break
    return names


def parse_director(obj: str) -> list[str]:
    """Extract director name from crew list."""
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            return [i["name"]]
    return []


def preprocess_movies(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare movie dataset for vectorization."""
    df = df[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
    df.dropna(inplace=True)

    # Apply parsing functions
    df["genres"] = df["genres"].apply(parse_name_list)
    df["keywords"] = df["keywords"].apply(parse_name_list)
    df["cast"] = df["cast"].apply(parse_top_cast)
    df["crew"] = df["crew"].apply(parse_director)

    # Clean text
    df["overview"] = df["overview"].apply(lambda x: x.split())
    for col in ["genres", "keywords", "cast", "crew"]:
        df[col] = df[col].apply(lambda x: [i.replace(" ", "") for i in x])

    # Combine all into a single "tags" column
    df["tags"] = df["overview"] + df["genres"] + df["keywords"] + df["cast"] + df["crew"]
    new_df = df[["movie_id", "title", "tags"]]
    new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())
    return new_df


# -------------------------------
# Feature Extraction & Similarity
# -------------------------------
ps = PorterStemmer()


def stem_text(text: str) -> str:
    """Apply stemming to text."""
    return " ".join([ps.stem(word) for word in text.split()])


def create_similarity_matrix(df: pd.DataFrame):
    """Create vector embeddings and similarity matrix."""
    df["tags"] = df["tags"].apply(stem_text)

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(df["tags"]).toarray()

    similarity = cosine_similarity(vectors)
    return df, similarity


# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(movie: str, df: pd.DataFrame, similarity: np.ndarray, top_n: int = 5) -> list[str]:
    """Recommend similar movies given a movie title."""
    if movie not in df["title"].values:
        return [f"Movie '{movie}' not found in database."]
    
    idx = df[df["title"] == movie].index[0]
    distances = similarity[idx]
    movie_indices = sorted(
        list(enumerate(distances)), key=lambda x: x[1], reverse=True
    )[1: top_n + 1]

    return [df.iloc[i[0]].title for i in movie_indices]


# -------------------------------
# Run & Save
# -------------------------------
if __name__ == "__main__":
    # Load & preprocess
    movies_df = load_data("tmdb_5000_movies.csv", "tmdb_5000_credits.csv")
    new_df = preprocess_movies(movies_df)
    new_df, similarity = create_similarity_matrix(new_df)

    # Example usage
    print("Recommendations for '10th & Wolf':")
    print(recommend("10th & Wolf", new_df, similarity))

    # Save model
    pickle.dump(new_df, open("movie_list.pkl", "wb"))
    pickle.dump(similarity, open("similarity.pkl", "wb"))
