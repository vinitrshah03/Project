''' This file contains the configuration settings for the application. This is supposed to be kept secret and not shared publicly. '''

# ============= Google OAuth2 Configuration =============
GOOGLE_CLIENT_ID = "<your_google_client_id>"
GOOGLE_CLIENT_SECRET = "<your_google_client_secret>"
GOOGLE_REDIRECT_URI = "http://localhost:5000/google/callback"

# ========== SHODAN API CONFIGURATION ==========
SHODAN_API_KEY = "<your_api_key>"

# ========== MYSQL DATABASE CONFIGURATION ==========
MYSQL_HOST = "localhost"
MYSQL_USER = "<your_db_username>"
MYSQL_PASSWORD = "<your_db_password>"
MYSQL_DATABASE = "user_auth"
