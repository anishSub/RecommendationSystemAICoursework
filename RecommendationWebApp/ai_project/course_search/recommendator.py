import pandas as pd
import numpy as np
import os
import joblib  # <--- WE USE THIS NOW
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# 1. SETUP PATHS
# We look for the .pkl files instead of the .csv
pkl_data_path = os.path.join(os.path.dirname(__file__), 'course_data.pkl')
pkl_matrix_path = os.path.join(os.path.dirname(__file__), 'tfidf_matrix.pkl')

# 2. GLOBAL VARIABLES
df = None
tfidf_matrix = None

def load_data():
    """Loads the PRE-COMPILED model files (Fast Startup)."""
    global df, tfidf_matrix
    
    if df is not None:
        return

    print("AI ENGINE: Loading Pre-compiled Models...")
    try:
        # Load the Dataframe (This ALREADY contains 'clean_title', 'norm_price', etc.)
        df = joblib.load(pkl_data_path)
        
        # Load the Matrix (This ALREADY is the TF-IDF matrix)
        tfidf_matrix = joblib.load(pkl_matrix_path)
        
        print("AI ENGINE: Model Loaded Successfully!")
        
    except FileNotFoundError:
        print("ERROR: .pkl files not found! Please copy them to the course_search folder.")

def recommend(query, N=10):
    """The Final Model 5 Logic"""
    if df is None:
        load_data()
        
    try:
        # 1. Find Seed Course
        # We search the ORIGINAL title for user friendliness
        matches = df[df['title'].str.contains(query, case=False)]
        if matches.empty:
            return []
        
        idx = matches.index[0]
        
        # 2. Calculate Scores
        # We use the loaded matrix directly
        text_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
        
        # These columns exist because we saved them in the .pkl file
        sub_scores = df['norm_subscribers'].values
        rating_scores = df['norm_rating'].values
        price_scores = df['price_score'].values 
        
        # 3. Weighted Sum (Your Tuned Weights)
        final_scores = (text_scores * 0.40) + \
                       (sub_scores * 0.10) + \
                       (rating_scores * 0.10) + \
                       (price_scores * 0.40)
        
        # 4. Filters
        final_scores[text_scores < 0.3] = 0 
        
        keyword_mask = df['title'].str.contains(query, case=False, regex=False)
        final_scores = final_scores * keyword_mask

        if np.all(final_scores == 0):
            return []
        
        # 5. Get Results
        top_indices = final_scores.argsort()[::-1][1:N+1]
        
        raw_results = df.iloc[top_indices].reset_index()[['index', 'title', 'url', 'price_detail__amount', 'avg_rating', 'num_subscribers']].to_dict('records')
        
        cleaned_results = []
        for r in raw_results:
            r['id'] = r.pop('index')
            cleaned_results.append(r)
            
        return cleaned_results

    except Exception as e:
        print(f"Error in recommend: {e}")
        return []

def get_course_by_id(course_id):
    """Fetches details for the Detail Page."""
    if df is None:
        load_data()
    try:
        course = df.iloc[int(course_id)]
        
        # Clean Date Logic
        raw_date = str(course['published_time'])
        try:
            dt_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
            clean_date = dt_obj.strftime("%B %d, %Y")
        except ValueError:
            clean_date = raw_date.split("T")[0]

        return {
            'id': int(course_id),
            'title': course['title'],
            'url': course['url'],
            'price': course['price_detail__amount'],
            'rating': round(course['avg_rating'], 1),
            'subscribers': course['num_subscribers'],
            'published_time': clean_date,
        }
    except IndexError:
        return None

def get_popular_courses(N=6):
    """Fetches popular courses for the Home Page."""
    if df is None:
        load_data()
    try:
        top_indices = df['num_subscribers'].argsort()[::-1][:N]
        raw_results = df.iloc[top_indices].reset_index()[['index', 'title', 'url', 'price_detail__amount', 'avg_rating', 'num_subscribers']].to_dict('records')
        
        cleaned_results = []
        for r in raw_results:
            r['id'] = r.pop('index')
            cleaned_results.append(r)
        return cleaned_results
    except Exception as e:
        return []