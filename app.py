''' This file contains all the important routes and functions for the web application.'''

from flask import Flask, request
from flask import render_template, url_for, redirect, session
import requests, os
from config import *
from recommender import *

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key

# -------------------- General Declarations --------------------
FACEBOOK_PAGE_URL = "https://www.facebook.com/<your_fb_page>"
INSTAGRAM_PAGE_URL = "https://www.instagram.com/<your_insta_page>"

# OAuth Endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# ---------------------- MySQL Connection ----------------------
db_config = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE
}

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = db.cursor(dictionary=True)

# ---------------------- Redirection ----------------------

@app.route('/clean_redirect')
def clean_redirect():
    next_page = request.args.get("next", "home")
    return redirect(url_for(next_page))

# ---------------------- Register --------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    from flask import flash
    from werkzeug.security import generate_password_hash

    next_page = request.args.get("next")

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('clean_redirect', next=next_page or 'login'))
        except mysql.connector.IntegrityError:
            flash("Email already exists. Try another one.", "danger")

    return render_template('register.html')

# ---------------------- LOGIN --------------------------

def login_is_required(function):
    from functools import wraps
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login", next=request.url))
        return function(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import flash
    from werkzeug.security import check_password_hash

    next_page = request.args.get("next")

    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user"] = user  # Store full user dictionary in session
            session["user_id"] = user["id"] 
            flash("Login successful!", "success")
            return redirect(url_for('clean_redirect', next=next_page or 'home')) 
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

# ---------------------- LOGOUT --------------------------

@app.route("/logout")
def logout():
    from flask import flash

    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

# ---------------- GOOGLE LOGIN ----------------

@app.route("/login/google")
def login_google():
    from requests_oauthlib import OAuth2Session

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI, scope=["openid", "email", "profile"])
    auth_url, _ = google.authorization_url(GOOGLE_AUTH_URL, access_type="offline", prompt="select_account")
    return redirect(auth_url)

@app.route("/google/callback")
def google_callback():
    from requests_oauthlib import OAuth2Session
    from werkzeug.security import generate_password_hash

    try:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP in development
        google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI)
        token = google.fetch_token(
            GOOGLE_TOKEN_URL,
            client_secret=GOOGLE_CLIENT_SECRET,
            authorization_response=request.url,
        )

        # Fetch user info
        response = google.get(GOOGLE_USER_INFO_URL)
        user_info = response.json()

        if response.status_code == 200 and user_info:
            email = user_info.get("email")
            name = user_info.get("name", "Google User")

            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                # Use a dummy secure hash (this password will never be used for login)
                dummy_password = generate_password_hash("google-oauth-user")
                cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                            (name, email, dummy_password))
                db.commit()
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()

            # Store user info in session
            session["user"] = user_info
            session["user_id"] = user["id"]
            session.permanent = True

            print(f"Google OAuth Successful: {user_info}")
            return redirect(url_for("home"))


        else:
            return redirect(url_for("index"))

    except Exception as e:
        print(f"Google OAuth Error: {e}") 
        return redirect(url_for("index"))

# ---------------- Home ----------------

@app.route('/home/')
@login_is_required
def home():
    user = session.get("user", {})
    username = user.get("username") or user.get("name") or "Guest"
    data = f"Welcome {username}!"
    return render_template('home.html', data=data)

# ---------------- Index ----------------

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Services ----------------

@app.route('/services/')
@login_is_required
def services():
    return render_template('services.html')

# ---------------- Downloads ----------------
@app.route("/downloads")
@login_is_required
def downloads():
    return render_template("downloads.html")

# ---------------- Contact ----------------

@app.route('/contact/')
def contact():
    return render_template('contact.html')

# ---------------- FACEBOOK & INSTAGRAM FOLLOW REDIRECTS ----------------

@app.route("/follow/facebook")
def follow_facebook():
    return redirect(FACEBOOK_PAGE_URL)

@app.route("/follow/instagram")
def follow_instagram():
    return redirect(INSTAGRAM_PAGE_URL)

# ---------------- Input Sanitization ----------------

def check_input(user_input: str) -> str:
    unwanted_chars = set("<>'\"\\;-()[]{}+=*%$#@!^&")
    is_safe = True if not set(user_input) & unwanted_chars else False
    return is_safe

# ---------------- Vulnerability Searching using Shodan ----------------

@app.route('/vuln/search/', methods=["POST", "GET"])
@login_is_required
def search_exploit():
    import shodan
    api = shodan.Shodan(SHODAN_API_KEY)

    user_id = session.get('user_id', None)
    recommendations = get_recent_search_based_recommendations(user_id, context='shodan', db_config=db_config)

    error_message = None

    if request.method == "POST":
        search_query = request.form['search']
        
        # Save the search history to the database
        save_search_history(user_id, search_query, 'shodan', db_config)
        
        try:
            results = api.exploits.search(search_query)
            return render_template('searchShodan.html', data=results['matches'], recommendations=recommendations)
        except Exception as e:
            error_message = f"Error occurred while fetching results: {e}"
            return render_template('searchShodan.html', recommendations=recommendations, error_message=error_message)
    else:
        return render_template('searchShodan.html', recommendations=recommendations, error_message=error_message)

# ---------------- CVE and CPE Scanning using Shodan ----------------

# Find CVE/CPE data using specific ID
def fetch_cve_data(query: str, query_type: str = "cve"):
    import pandas as pd
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    if query_type == "cve":
        url = f"https://cvedb.shodan.io/cve/{query}"
    elif query_type == "cpe":
        url = f"https://cvedb.shodan.io/cves?cpe23={query}"
    else:
        raise ValueError("query_type must be either 'cve' or 'cpe'")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return pd.DataFrame()
    
    data = response.json()
    
    if query_type == "cpe":
        if isinstance(data, dict) and "cves" in data:
            data = data["cves"]
        else:
            data = []
    else:
        data = [data]
    
    if not data:
        print("No CVE data found.")
        return pd.DataFrame()
    
    cve_list = []
    for cve in data:
        published_datetime = cve.get("published_time", "N/A")

        if published_datetime != "N/A" and "T" in published_datetime:
            date_part, time_part = published_datetime.split("T")
        else:
            date_part, time_part = published_datetime, "N/A"

        cve_list.append({
            "CVE ID": cve.get("cve_id", "N/A"),
            "Description": cve.get("summary", "N/A"),
            "Published Date": date_part,
            "Published Time": time_part,
            "CVSS Score": cve.get("cvss", "N/A"),   
            "CVSS Version": cve.get("cvss_version", "N/A"),
            "CVSS v2": cve.get("cvss_v2", "N/A"),
            "CVSS 3": cve.get("cvss_v3", "N/A"),
            "EPSS": cve.get("epss", "N/A"),
            "EPSS Ranking": cve.get("ranking_epss", "N/A"),
            "Ransomware Campaign": cve.get("ransomware_campaign", "N/A"),
        })
    
    return pd.DataFrame(cve_list)

@app.route('/vuln/cve/', methods=["POST", "GET"])
@login_is_required
def cve():
    user_id = session.get('user_id', None)
    recommendations = get_recent_search_based_recommendations(user_id, context='cve', db_config=db_config)

    error_message = None

    if request.method == "POST":
        search_query = request.form['cve']
        
        save_search_history(user_id, search_query, 'cve', db_config)

        try:
            cve_df = fetch_cve_data(search_query, "cve")
            cve_data = cve_df.to_dict(orient="records")
            return render_template('vuln_cve.html', data=cve_data, recommendations=recommendations)
        except Exception as e:
            error_message = f"Error occurred while fetching CVE data: {e}"
            return render_template('vuln_cve.html', recommendations=recommendations, error_message=error_message)
    else:
        return render_template('vuln_cve.html', data=[], recommendations=recommendations, error_message=error_message)

# ----------------- CPE Search ------------------
@app.route('/vuln/cpe/', methods=["POST", "GET"])
@login_is_required
def cpe():
    user_id = session.get('user_id')
    error_message = None
    data = []

    recommendations = get_final_recommendations(user_id, 'cpe', db_config)

    if request.method == "POST":
        search_query = request.form.get('cpe')

        if not search_query:
            error_message = "Please enter a CPE ID."
            return render_template('vuln_cpe.html', data=data, recommendations=recommendations, error_message=error_message)

        # Save search query to database
        save_search_history(user_id, search_query, 'cpe', db_config)

        try:
            cve_cpe_df = fetch_cve_data(search_query, "cpe")
            data = cve_cpe_df.to_dict(orient="records")
        except Exception as e:
            error_message = f"Error occurred while fetching CPE data: {e}"

    return render_template('vuln_cpe.html', data=data, recommendations=recommendations, error_message=error_message)


# ---------------- Password Checker Tool ----------------

@app.route('/password/checker/', methods = ["POST", "GET"])
@login_is_required
def password_checker_tool():
    def length_checker(x):
        #checking the basic length of password (8 characters minimum)
        if 8<=len(x):
            if len(x)<128: #checking if password is not too long (128 characters maximum)
                return "STRONG"
            else: #feedback for user
                return "password is TOO LONG! It should be of atmost 128 characters."
        else: #feedback for user
            return "password is TOO SHORT! It should be of atleast 8 characters."

    def commonpwd_checker(x):
        import pwnedpasswords

        if pwnedpasswords.check(x):
            return "password is WEAK! This password is commonly used."
        else:
            return "STRONG"


    def numeric_checker(x):
        if x.isnumeric(): #checking if all chars in password are numbers
            return "password is WEAK! Every character cannot be a number."
        else:
            #checking the number of occurences of numbers in the password 
            n_count = 0
            for _ in x:
                for i in range(0,10):
                    if _==str(i):
                        n_count+=1         
            if n_count>=2: 
                return "STRONG"
            else: #feedback for user 
                return "password is WEAK! Add atleast 2 numbers in the password."

    def special_checker(x):
        spl = ' !@#$%^&*()_-+=~`|/?><.:;{}[]' #characters like ',",\ have not been included as per basic/common password security measures and input sanitization
        
        #checking the number of occurences of special chars in the password
        s_count = 0
        for _ in x:
            for j in spl:
                if _==j:
                    s_count+=1
        if s_count>=2:
            return "STRONG"
        else: #feedback for user 
            return "password is WEAK! Add atleast 2 special characters."
        
    def upperalpha_checker(x):
        alpha = 'abcdefghijklmnopqrstuvwxyz'

        #checking if all characters are uppercase alphabets
        if x.isupper():
            return "password is WEAK! Every alphabet cannot be in uppercase"
        else:
            #checking for number of occurences of uppercase alphabets
            u_count = 0
            for _ in x:
                for j in alpha.upper():
                    if _==j:
                        u_count+=1
            if u_count>=2:
                return "STRONG"
            else: #feedback for user 
                return "password is WEAK! Add atleast 2 uppercase alphabets."
            
    def loweralpha_checker(x):
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        #checking if all chars are lowercase alphabets

        if x.islower():
            return "password is WEAK! Every alphabet cannot be in lowercase"
        else:
            #checking for number of occurences of lowercase alphabets
            l_count = 0
            for _ in x:
                for k in alpha:
                    if _==k:
                        l_count+=1
            if l_count>=2:
                return "STRONG"
            else:
                return "password is WEAK! Add atleast 2 lowercase alphabets."
            
    def password_checker(x):
        if type(x)==str: #checking for data type of password for further detailed error handling (if required)
            if length_checker(x)=="STRONG": #length check
                if commonpwd_checker(x)=="STRONG": #common dictionary check
                    if special_checker(x)=="STRONG": #special characters check
                        if numeric_checker(x)=="STRONG": #numbers check
                            if upperalpha_checker(x)=="STRONG": #uppercase chars check
                                if loweralpha_checker(x)=="STRONG": #lowercase chars check
                                    return render_template('passwords.html',data = "password is STRONG!")
                                else:
                                    return render_template('passwords.html',data = loweralpha_checker(x))
                            else:
                                return render_template('passwords.html',data = upperalpha_checker(x))
                        else:
                            return render_template('passwords.html',data = numeric_checker(x))
                    else:
                        return render_template('passwords.html',data = special_checker(x))
                else:
                    return render_template('passwords.html',data = commonpwd_checker(x))
            else:
                return render_template('passwords.html',data = length_checker(x))
        else:
            return render_template('passwords.html',data = "Invalid data type!")

    if request.method == "POST":
        pswd = request.form['password'] 
        return password_checker(pswd)
    else:
        return render_template('passwords.html')

# ----------------- Keylogger ------------------
@app.route('/start_keylogger', methods=['POST'])
@login_is_required
def start_keylogger():
    import subprocess

    try:
        subprocess.Popen(['python', 'keylogger.py'])
        return redirect(url_for('downloads'))
    except Exception as e:
        print(f"Error starting keylogger: {e}")
        return "An error occurred while starting the keylogger.", 500
    
@app.route('/fetch_log')
@login_is_required
def fetch_log():
    try:
        import socket
        dev_name = socket.gethostname()
        for _ in dev_name: 
            if _ == '\ / : * ? " < > |':
                dev_name.replace(_,"_")
        with open('C:/<your_file_path>/Desktop/{0}_KEYLOG.txt'.format(dev_name), 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return str(e)
    
# -------------------- Downloading Files --------------------
@app.route("/download/<filename>")
@login_is_required
def download_file(filename):
    from flask import send_from_directory

    DOWNLOADS_FOLDER = os.path.join(os.getcwd(), "downloads")
    app.config["DOWNLOADS_FOLDER"] = DOWNLOADS_FOLDER

    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)

    return send_from_directory(app.config["DOWNLOADS_FOLDER"], filename, as_attachment=True)

# ----------------- Save Search History ------------------
def save_search_history(user_id, search_query, search_type, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    query = "INSERT INTO search_history (user_id, search_term, search_type) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, search_query, search_type))
    db.commit()
    cursor.close()
    db.close()

# ----------------- Fetch Recent Searches ------------------
def get_recent_search_based_recommendations(user_id, context, db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT search_term 
    FROM search_history 
    WHERE user_id = %s AND search_type = %s 
    ORDER BY timestamp DESC 
    LIMIT 5
    """
    
    cursor.execute(query, (user_id, context))
    recommendations = cursor.fetchall()

    cursor.close()
    connection.close()

    return [rec['search_term'] for rec in recommendations] 

import re

def get_final_recommendations(user_id, search_type, db_config):
    recent_searches = []

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            SELECT search_term FROM search_history
            WHERE user_id = %s AND search_type = %s
            ORDER BY timestamp DESC LIMIT 5
        """
        cursor.execute(query, (user_id, search_type))
        recent_searches = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching search history: {e}")

    # Get all CPE entries (list of dicts with 'cpe' key)
    all_cpe_dicts = fetch_items_for_context('cpe')
    cleaned_cpes = [item['cpe'] for item in all_cpe_dicts if isinstance(item, dict) and 'cpe' in item]

    # Case 1: No recent searches → return default CPE recommendations
    if not recent_searches:
        return [{"title": cpe, "tags": cpe.lower()} for cpe in cleaned_cpes[:5]]

    # Case 2: Use recent history to filter recommendations
    results = []
    for cpe in cleaned_cpes:
        tags = cpe.lower().replace("cpe:2.3:", "").replace(":", " ")
        if any(re.search(re.escape(query), tags, re.IGNORECASE) for query in recent_searches):
            results.append({"title": cpe, "tags": tags})

    # Fill up to 5 if less than 5 matches
    if len(results) < 5:
        for cpe in cleaned_cpes:
            if cpe not in [r["title"] for r in results]:
                results.append({"title": cpe, "tags": cpe.lower()})
            if len(results) >= 5:
                break

    return results[:5]
