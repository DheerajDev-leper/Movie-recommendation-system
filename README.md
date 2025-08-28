# 🎬 Movie Recommendation System  

This project is a **content-based movie recommender system** built using Python, Pandas, Scikit-Learn, and Streamlit.  

It has two parts:  

1. **movie.py** → Preprocesses raw TMDB dataset, builds similarity matrix, and saves preprocessed files.  
2. **app.py** → Frontend web app built with Streamlit that lets you search for movies and get recommendations with posters.  

---

## 📂 Project Structure  

```
.
├── movie.py               # Preprocessing, feature extraction, and saving similarity model
├── app.py                 # Streamlit frontend for movie recommendation
├── tmdb_5000_movies.csv   # Movie dataset
├── tmdb_5000_credits.csv  # Credits dataset
├── movie_list.pkl         # Pickled preprocessed dataset (generated after running movie.py)
├── similarity.pkl         # Pickled similarity matrix (generated after running movie.py)
└── README.md
```

---

Extract the both csv file from dataset zip folder and save it in the main directory where the project is been saved.


## 🚀 Running the Project  

### Step 1: Data Preprocessing (Run `movie.py`)  

This step loads the raw CSVs, cleans them, generates feature vectors, computes similarity, and saves them as `.pkl` files.  

```bash
python movie.py
```

✔️ Outputs:  
- `movie_list.pkl` → preprocessed dataframe  
- `similarity.pkl` → similarity matrix  

---

### Step 2: Launch Frontend (Run `app.py`)  

Run the Streamlit web app:  

```bash
streamlit run app.py
```

It will open in your browser (default: http://localhost:8501).  

---

## 📖 File Explanations  

### **movie.py**  

- **load_data()** → Loads and merges movies & credits datasets.  
- **parse functions** → Extracts genres, keywords, cast, and director from JSON-like strings.  
- **preprocess_movies()** → Cleans data and creates `tags` column.  
- **stem_text()** → Applies Porter stemming for better similarity.  
- **create_similarity_matrix()** → Generates vector embeddings and cosine similarity.  
- **recommend()** → Returns top similar movies for a given title.  
- Saves processed data (`movie_list.pkl`, `similarity.pkl`).  

---

### **app.py**  

- Loads `movie_list.pkl` and `similarity.pkl`.  
- Provides **search dropdown** to select a movie.  
- Calls TMDB API to fetch **movie posters**.  
- Displays **Top 5 recommended movies** with posters.  
- Has **search bar & dropdown with custom colors** for better UI.  

---

## 🎥 Example  

**Search:** *Avatar*  
**Recommendations:**  
- John Carter  
- Guardians of the Galaxy  
- Star Trek  
- Thor  
- The Avengers  

Each with their posters displayed in the Streamlit app.  

---
