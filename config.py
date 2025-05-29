''' This file contains the configuration settings for the application. This is supposed to be kept secret and not shared publicly. '''

# ============= Google OAuth2 Configuration =============
GOOGLE_CLIENT_ID = "1003437659662-3b45kgsvvtn7pi0bsmdmkip3i8lgb5pc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:5000/google/callback"

# ========== SHODAN API CONFIGURATION ==========
SHODAN_API_KEY = "XXq5hAOwWMaATCx5gBcASQC0j1yvNu3N"

# ========== MYSQL DATABASE CONFIGURATION ==========
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456789"
MYSQL_DATABASE = "user_auth"