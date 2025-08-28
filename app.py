import pickle 
import streamlit as st 
import requests 

# --- Page Config ---
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Modern UI ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Remove default Streamlit spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Remove gaps between elements */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    
    /* Fix white space issues */
    .main .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Custom font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Selection container */
    # .selection-container {
    #     background: transparent;
    #     padding: 2rem;
    #     border-radius: 20px;
    #     box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    #     margin: 2rem auto 3rem auto;
    #     border: 1px solid #e5e7eb;
    #     max-width: 800px;
    # }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div > div {
        background-color: #f9fafb !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
        color: #1f2937 !important;
        min-height: 3rem !important;
        height: auto !important;
        line-height: 1.5 !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Fix selectbox input text color and height */
    .stSelectbox input {
        color: #1f2937 !important;
        background-color: transparent !important;
        height: auto !important;
        min-height: 1.5rem !important;
        line-height: 1.5 !important;
        padding: 0 !important;
        font-size: 1rem !important;
    }
    
    /* Fix selectbox displayed value */
    .stSelectbox > div > div > div > div {
        color: #1f2937 !important;
        line-height: 1.5 !important;
        height: auto !important;
        padding: 0 !important;
        font-size: 1rem !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Fix selectbox placeholder text */
    .stSelectbox input::placeholder {
        color: #6b7280 !important;
        line-height: 1.5 !important;
    }
    
    /* Fix dropdown arrow */
    .stSelectbox svg {
        color: #374151 !important;
        fill: #374151 !important;
    }
    
    /* Fix dropdown options */
    .stSelectbox > div > div > div > div {
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    /* Fix dropdown menu */
    [data-baseweb="select"] {
        background-color: white !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: white !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        height : 50px;
    }
    
    /* Fix dropdown list items */
    [data-baseweb="menu"] {
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    [data-baseweb="menu"] li {
        background-color: white !important;
        color: #1f2937 !important;
        padding: 0.75rem !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #f3f4f6 !important;
        color: #667eea !important;
    }
    
    /* Fix selected option */
    [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Movie card styling */
    .movie-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
        height: auto;
        display: flex;
        flex-direction: column;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .movie-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1f2937;
        margin-top: 1rem;
        text-align: center;
        line-height: 1.3;
        min-height: 2.6rem;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0;
        background: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    .movie-poster {
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1rem;
        aspect-ratio: 2/3;
        width: 100%;
    }
    
    .movie-poster img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Results section */
    .results-header {
        text-align: center;
        margin: 3rem 0 2rem 0;
    }
    
    .results-title {
        font-size: 2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .results-subtitle {
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .selection-container {
            padding: 1.5rem;
            margin: 1rem;
        }
    }
    
    /* Hide Streamlit branding and reduce spacing */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove extra padding from Streamlit containers */
    .css-1d391kg, .css-1v0mbdj {
        padding: 0 !important;
    }
    
    /* Fix container spacing */
    .css-12oz5g7 {
        padding-top: 0 !important;
    }
    
    /* Remove default margins */
    .css-1outpf7 {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Fetch Movie Poster from TMDB ---
@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Image"

# --- Recommendation Function ---
def recommend(movie, movies_data, similarity_matrix):
    try:
        # Handle different data structures
        if hasattr(movies_data, 'iloc'):  # DataFrame
            movie_titles = movies_data['title'] if 'title' in movies_data.columns else movies_data.iloc[:, 1]
            movie_indices = movie_titles[movie_titles == movie].index
        else:  # Dictionary or other format
            movie_titles = [item['title'] if isinstance(item, dict) else item for item in movies_data]
            movie_indices = [i for i, title in enumerate(movie_titles) if title == movie]
        
        if len(movie_indices) == 0:
            st.error(f"Movie '{movie}' not found in database.")
            return [], []
            
        index = movie_indices[0]
        
        # Calculate similarity distances
        distances = sorted(
            list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1]
        )
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:6]:  # top 5 recommendations
            movie_idx = i[0]
            
            # Handle different data structures for movie details
            if hasattr(movies_data, 'iloc'):  # DataFrame
                if 'movie_id' in movies_data.columns:
                    movie_id = movies_data.iloc[movie_idx]['movie_id']
                elif 'id' in movies_data.columns:
                    movie_id = movies_data.iloc[movie_idx]['id']
                else:
                    movie_id = movie_idx  # fallback to index
                
                if 'title' in movies_data.columns:
                    movie_title = movies_data.iloc[movie_idx]['title']
                else:
                    movie_title = movies_data.iloc[movie_idx, 1]  # assume title is second column
            else:  # Dictionary or list format
                movie_data = movies_data[movie_idx]
                if isinstance(movie_data, dict):
                    movie_id = movie_data.get('movie_id', movie_data.get('id', movie_idx))
                    movie_title = movie_data.get('title', f'Movie {movie_idx}')
                else:
                    movie_id = movie_idx
                    movie_title = str(movie_data)
            
            recommended_movie_names.append(movie_title)
            recommended_movie_posters.append(fetch_poster(movie_id))
        
        return recommended_movie_names, recommended_movie_posters
        
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        st.error(f"Debug info - Movies data type: {type(movies_data)}")
        if hasattr(movies_data, 'columns'):
            st.error(f"DataFrame columns: {list(movies_data.columns)}")
        elif hasattr(movies_data, '__len__'):
            st.error(f"Data length: {len(movies_data)}")
            if len(movies_data) > 0:
                st.error(f"First item type: {type(movies_data[0])}")
                if isinstance(movies_data[0], dict):
                    st.error(f"First item keys: {list(movies_data[0].keys())}")
        return [], []

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        movies = pickle.load(open("movie_list.pkl", "rb"))
        similarity = pickle.load(open("similarity.pkl", "rb"))
        return movies, similarity
    except FileNotFoundError:
        st.error("Data files not found. Please ensure 'movie_list.pkl' and 'similarity.pkl' are in the correct directory.")
        return None, None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# --- Main UI ---
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🎬 CineMatch</h1>
        <p class="main-subtitle">Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    movies, similarity = load_data()
    
    if movies is None or similarity is None:
        st.stop()
    
    # Selection container
    st.markdown('<div class="selection-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Handle different data structures for movie list
        try:
            if hasattr(movies, 'iloc') and 'title' in movies.columns:
                movie_list = movies["title"].values
            elif hasattr(movies, 'iloc'):
                movie_list = movies.iloc[:, 1].values  # assume title is second column
            else:  # List or dictionary format
                movie_list = [item['title'] if isinstance(item, dict) else str(item) for item in movies]
        except Exception as e:
            st.error(f"Error processing movie list: {str(e)}")
            movie_list = []
        
        if len(movie_list) == 0:
            st.error("No movies found in database.")
            st.stop()
            
        selected_movie = st.selectbox(
            "🎭 Choose a movie you enjoyed:",
            movie_list,
            help="Select a movie to get personalized recommendations based on similar themes, genres, and characteristics."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button
        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        with button_col2:
            recommend_button = st.button("✨ Get Recommendations", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations section
    if recommend_button and selected_movie:
        with st.spinner("🔍 Finding perfect matches for you..."):
            names, posters = recommend(selected_movie, movies, similarity)
        
        if names and posters:
            st.markdown("""
            <div class="results-header">
                <h2 class="results-title">🌟 Recommended for You</h2>
                <p class="results-subtitle">Movies similar to your selection</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create responsive columns
            cols = st.columns(5, gap="medium")
            
            for idx, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-poster">
                            <img src="{posters[idx]}" alt="{names[idx]}" style="width: 100%; height: auto; border-radius: 12px;">
                        </div>
                        <div class="movie-title">{names[idx]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Sorry, we couldn't generate recommendations. Please try again.")

if __name__ == "__main__":
    main()