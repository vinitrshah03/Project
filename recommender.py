''' This file contains functions for content-based and collaborative filtering recommendations,
    as well as a hybrid approach that combines both methods. '''

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

# dummy dataframe for testing purposes
data = pd.DataFrame({
    'item_id': [1, 2, 3, 4, 5],
    'title': ['Windows Vulnerability', 'Linux Exploit', 'Apache Log4j', 'MySQL Buffer Overflow', 'Adobe Flash Flaw'],
    'tags': ['windows security', 'linux kernel', 'apache java', 'mysql overflow', 'adobe plugin']
})

#  Content-Based Filtering 
def content_recommendation(user_input, top_n=3):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(data['tags'])
    user_vec = tfidf.transform([user_input])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    indices = similarities.argsort()[-top_n:][::-1]
    return data.iloc[indices][['item_id', 'title']].to_dict(orient='records')

# Collaborative Filtering (basic)
user_history = {}

def collaborative_recommendation(user_id, top_n=3):
    all_users = list(user_history.keys())
    if user_id not in user_history or len(all_users) <= 1:
        return []

    current_user_items = set(user_history[user_id])
    similarities = {}

    for other_user in all_users:
        if other_user == user_id:
            continue
        overlap = len(set(user_history[other_user]) & current_user_items)
        similarities[other_user] = overlap

    similar_users = sorted(similarities, key=similarities.get, reverse=True)
    recommendations = set()

    for similar_user in similar_users:
        items = set(user_history[similar_user])
        recommendations |= items - current_user_items
        if len(recommendations) >= top_n:
            break

    rec_ids = list(recommendations)[:top_n]
    return data[data['item_id'].isin(rec_ids)][['item_id', 'title']].to_dict(orient='records')

# Hybrid Approach (User-Behaviour Based + Search Based) 
def hybrid_recommend(user_id, user_input, context, top_n=5):
    content = content_recommendation(user_input, top_n)
    collab = collaborative_recommendation(user_id, top_n)
    
    # Combine recommendations from both approaches
    combined = {item['item_id']: item for item in content + collab}
    
    # Customize recommendations based on context (Shodan, CVE, or CPE)
    if context == 'shodan':
        recommended_items = fetch_items_for_context('shodan')
    elif context == 'cve':
        recommended_items = fetch_items_for_context('cve')
    elif context == 'cpe':
        recommended_items = fetch_items_for_context('cpe')
    else:
        recommended_items = list(combined.values())

    return recommended_items[:top_n]

# Dummy function to simulate fetching items from different sources (Shodan, CVE, CPE) 
def fetch_items_for_context(context: str) -> List[dict]:
    if context == 'shodan':
        return [
            {"item_id": 1, "title": "FTP"},
            {"item_id": 2, "title": "Apache Tomcat"},
            {"item_id": 3, "title": "Iphone X Device"},
            {"item_id": 4, "title": "SSH Server"},
            {"item_id": 5, "title": "Microsoft IIS"}
        ]
    elif context == 'cve':
        return [
            {"item_id": 1001, "title": "CVE-2021-2291"},
            {"item_id": 1002, "title": "CVE-2020-2551"},
            {"item_id": 1003, "title": "CVE-2020-0601"},
            {"item_id": 1004, "title": "CVE-2019-0708"},
            {"item_id": 1005, "title": "CVE-2025-1146"}
        ]
    elif context == 'cpe':
        return [
            {"item_id": 2001, "title": "cpe:2.3:a:libpng:libpng:0.8"},
            {"item_id": 2002, "title": "cpe:2.3:a:apache:tomcat:9.0.0:*:*:*:*:*:*:*"},
            {"item_id": 2003, "title": "cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*"},
            {"item_id": 2004, "title": "cpe:2.3:o:microsoft:iis:10.0:*:*:*:*:*:*:*"},
            {"item_id": 2005, "title": "cpe:2.3:a:oracle:mysql:8.0.18:*:*:*:*:*:*:*"}
        ]
    return []

def hybrid_recommend_for_search(user_id, user_input, context, top_n=5):
    recommendations = hybrid_recommend(user_id, user_input, context, top_n)
    items = fetch_items_for_context(context)
    
    recommended_items = []
    for item in recommendations:
        for fetched_item in items:
            if item['item_id'] == fetched_item['item_id']:
                recommended_items.append(fetched_item)
    
    return recommended_items

import mysql.connector
from mysql.connector import Error

def get_recent_search_based_recommendations(user_id, context, db_config, top_n=5):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT search_term 
            FROM search_history 
            WHERE user_id = %s AND search_type = %s
            ORDER BY timestamp DESC
            LIMIT 5
        """
        cursor.execute(query, (user_id, context))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return fetch_items_for_context(context)

        combined_input = ' '.join(row['search_term'] for row in results)
        return content_recommendation(combined_input, top_n)

    except Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        return fetch_items_for_context(context)

# New function to use in your Flask route
def get_final_recommendations(user_id, context, db_config, top_n=5):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM search_history WHERE user_id = %s AND search_type = %s",
            (user_id, context)
        )
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if count > 0:
            return get_recent_search_based_recommendations(user_id, context, db_config, top_n)
        else:
            return fetch_items_for_context(context)
    except Error as e:
        print(f"[ERROR] Failed to fetch recommendation fallback logic: {e}")
        return fetch_items_for_context(context)


# Hybrid Approach (User-Behaviour Based + Search Based) 
def hybrid_recommend(user_id, user_input, context, top_n=5):
    content = content_recommendation(user_input, top_n)
    collab = collaborative_recommendation(user_id, top_n)
    
    # Combine recommendations from both approaches
    combined = {item['item_id']: item for item in content + collab}

    # Use fallback if combined is empty
    if not combined:
        return fetch_items_for_context(context)

    return finalize_context_recommendations(list(combined.values()), context, top_n)

# Ensure we always return context-appropriate results 
def finalize_context_recommendations(recommendations: List[dict], context: str, top_n: int) -> List[dict]:

    context_defaults = fetch_items_for_context(context)
    context_ids = {item['item_id'] for item in context_defaults}

    filtered = [item for item in recommendations if item['item_id'] in context_ids]

    if not filtered:
        return context_defaults[:top_n]

    return filtered[:top_n]

def update_user_history(user_id, item_id):
    if user_id not in user_history:
        user_history[user_id] = []
    if item_id not in user_history[user_id]:
        user_history[user_id].append(item_id)

import re

def generate_recommendations(user_query=None, recent_searches=None):
    data = fetch_items_for_context() 
    df = pd.DataFrame(data)

    df['title'] = df['cpe']  # Show CPE ID in the recommendation box
    df['tags'] = df['cpe'].apply(lambda x: x.lower().replace("cpe:2.3:", "").replace(":", " "))

    # Filter based on recent searches or user query
    if recent_searches:
        pattern = '|'.join(map(re.escape, recent_searches))
        filtered = df[df['tags'].str.contains(pattern, case=False, na=False)]
    elif user_query:
        pattern = re.escape(user_query)
        filtered = df[df['tags'].str.contains(pattern, case=False, na=False)]
    else:
        filtered = df.head(5)

    return filtered[['title', 'tags']].head(5).to_dict(orient='records')