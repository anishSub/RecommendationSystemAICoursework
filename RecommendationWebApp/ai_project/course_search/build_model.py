# # course_search/build_model.py
# import pandas as pd
# import numpy as np
# import os
# import re
# import joblib
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import MinMaxScaler

# # 1. SETUP PATHS
# # Assumes udemy_data.csv is in the same folder
# current_dir = os.path.dirname(os.path.abspath(__file__))
# csv_path = os.path.join(current_dir, 'udemy_output_All_IT__Software_p1_p626.csv') # CHECK THIS NAME!
# pkl_data_path = os.path.join(current_dir, 'course_data.pkl')
# pkl_matrix_path = os.path.join(current_dir, 'tfidf_matrix.pkl')

# def build_and_save():
#     print("--- STARTING MODEL BUILDER ---")
    
#     # 2. LOAD DATA
#     if not os.path.exists(csv_path):
#         print(f"ERROR: Could not find CSV at {csv_path}")
#         print("Please rename your CSV to 'udemy_data.csv' or update the script.")
#         return

#     print("1. Loading CSV...")
#     df = pd.read_csv(csv_path)

#     # 3. FEATURE ENGINEERING (The stuff you were missing!)
#     print("2. Cleaning Titles & calculating Scores...")
    
#     # Clean Titles
#     def clean_title(title):
#         title = str(title).lower()
#         title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
#         stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'of', 'with', 'for', 'to', 'at', 'by', 'complete', 'course', 'tutorial'])
#         return " ".join([w for w in title.split() if w not in stop_words])

#     df['clean_title'] = df['title'].apply(clean_title)
    
#     # Normalize Numerical Features
#     df['price_detail__amount'] = df['price_detail__amount'].fillna(0)
#     scaler = MinMaxScaler()
    
#     # Create the columns expected by recommender.py
#     df['norm_price'] = scaler.fit_transform(df[['price_detail__amount']])
#     df['price_score'] = 1 - df['norm_price'] # 1.0 = Free, 0.0 = Expensive
    
#     df['log_subs'] = np.log1p(df['num_subscribers'])
#     df['norm_subs'] = scaler.fit_transform(df[['log_subs']])
#     df['norm_rating'] = scaler.fit_transform(df[['avg_rating']])
    
#     # 4. BUILD TF-IDF MATRIX
#     print("3. Building TF-IDF Matrix (The Brain)...")
#     tfidf = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = tfidf.fit_transform(df['clean_title'])

#     # 5. SAVE FILES
#     print("4. Saving to .pkl files...")
#     joblib.dump(df, pkl_data_path)
#     joblib.dump(tfidf_matrix, pkl_matrix_path)
    
#     print(f"SUCCESS! Models saved to:\n- {pkl_data_path}\n- {pkl_matrix_path}")

# if __name__ == "__main__":
#     build_and_save()