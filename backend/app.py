

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import date
import os
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = '123456'


DB_CONFIG = {
    'host': 'localhost',
    'database': 'moodscape_db',
    'user': 'root',
    'password': '',  # Change this to your MySQL password
    'port': 3307
}


# DATABASE CONNECTION UTILITY


def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# AUTHENTICATION ROUTES


@app.route('/')
def index():
    """Home page - redirect to movies list"""
    return redirect(url_for('list_movies'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                # Query to get user with role information
                query = """
                    SELECT u.*, 
                           CASE 
                               WHEN a.UserID IS NOT NULL THEN 'admin'
                               WHEN n.UserID IS NOT NULL THEN 'user'
                               ELSE 'unknown'
                           END AS role
                    FROM Users u
                    LEFT JOIN Admin a ON u.UserID = a.UserID
                    LEFT JOIN NormalUser n ON u.UserID = n.UserID
                    WHERE u.Email = %s AND u.IsActive = 1
                """
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['PasswordHash'], password):
                    session['user_id'] = user['UserID']
                    session['user_name'] = user['Name']
                    session['user_role'] = user['role']
                    flash('Login successful!', 'success')
                    return redirect(url_for('list_movies'))
                else:
                    flash('Invalid email or password', 'error')
                    
            except Error as e:
                flash(f'Login error: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if user exists
                cursor.execute("SELECT UserID FROM Users WHERE Email = %s", (email,))
                if cursor.fetchone():
                    flash('Email already registered', 'error')
                    return render_template('register.html')
                
                # Hash password and insert user
                password_hash = generate_password_hash(password)
                query = """
                    INSERT INTO Users (Name, Email, PasswordHash, JoinDate, IsActive)
                    VALUES (%s, %s, %s, %s, 1)
                """
                cursor.execute(query, (name, email, password_hash, date.today()))
                user_id = cursor.lastrowid
                
                # Add to NormalUser role
                cursor.execute("INSERT INTO NormalUser (UserID) VALUES (%s)", (user_id,))
                
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
                
            except Error as e:
                conn.rollback()
                flash(f'Registration error: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# MOVIE CRUD ROUTES


@app.route('/movies')
def list_movies():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Get movies with average ratings
            query = """
                SELECT m.MovieID, m.Name, m.Summary, m.ReleaseYear, g.GenreName,
                       AVG(r.NumRating) AS AverageRating,
                       COUNT(r.NumRating) AS TotalRatings
                FROM Movie m
                JOIN Genre g ON m.GenreID = g.GenreID
                LEFT JOIN Rating r ON m.MovieID = r.MovieID
                GROUP BY m.MovieID, m.Name, m.Summary, m.ReleaseYear, g.GenreName
                ORDER BY m.Name
            """
            cursor.execute(query)
            movies = cursor.fetchall()
            
            return render_template('movies/list.html', movies=movies)
            
        except Error as e:
            flash(f'Error loading movies: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('movies/list.html', movies=[])

@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie details with reviews and mood distribution"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Get movie details
            query = """
                SELECT m.*, g.GenreName,
                       AVG(r.NumRating) AS AverageRating,
                       COUNT(r.NumRating) AS TotalRatings
                FROM Movie m
                JOIN Genre g ON m.GenreID = g.GenreID
                LEFT JOIN Rating r ON m.MovieID = r.MovieID
                WHERE m.MovieID = %s
                GROUP BY m.MovieID
            """
            cursor.execute(query, (movie_id,))
            movie = cursor.fetchone()
            
            if not movie:
                flash('Movie not found', 'error')
                return redirect(url_for('list_movies'))
            
            # Get reviews
            query = """
                SELECT rv.*, u.Name AS UserName, r.NumRating
                FROM Review rv
                JOIN Users u ON rv.UserID = u.UserID
                LEFT JOIN Rating r ON rv.UserID = r.UserID AND rv.MovieID = r.MovieID
                WHERE rv.MovieID = %s
                ORDER BY rv.CreatedAt DESC
            """
            cursor.execute(query, (movie_id,))
            reviews = cursor.fetchall()
            
            # Get mood distribution
            query = """
                SELECT mc.MoodName, COUNT(*) AS MoodCount
                FROM UserMood um
                JOIN MoodCategory mc ON um.MoodID = mc.MoodID
                WHERE um.MovieID = %s
                GROUP BY mc.MoodName
                ORDER BY MoodCount DESC
            """
            cursor.execute(query, (movie_id,))
            moods = cursor.fetchall()
            
            # Get user's rating if logged in
            user_rating = None
            if 'user_id' in session:
                query = "SELECT NumRating FROM Rating WHERE UserID = %s AND MovieID = %s"
                cursor.execute(query, (session['user_id'], movie_id))
                result = cursor.fetchone()
                if result:
                    user_rating = result['NumRating']
            
            return render_template('movies/detail.html', 
                                 movie=movie, reviews=reviews, 
                                 moods=moods, user_rating=user_rating)
            
        except Error as e:
            flash(f'Error loading movie details: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('list_movies'))

@app.route('/movies/add', methods=['GET', 'POST'])
def add_movie():
    """Add new movie (Admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            name = request.form['name']
            summary = request.form['summary']
            release_year = request.form['release_year']
            genre_id = request.form['genre_id']
            
            try:
                query = """
                    INSERT INTO Movie (Name, Summary, ReleaseYear, GenreID)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (name, summary, release_year, genre_id))
                conn.commit()
                flash('Movie added successfully!', 'success')
                return redirect(url_for('list_movies'))
                
            except Error as e:
                conn.rollback()
                flash(f'Error adding movie: {e}', 'error')
        
        # Get genres for dropdown
        cursor.execute("SELECT GenreID, GenreName FROM Genre ORDER BY GenreName")
        genres = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('movies/add.html', genres=genres)
    
    return redirect(url_for('list_movies'))


@app.route('/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Edit movie (Admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            name = request.form['name']
            summary = request.form['summary']
            release_year = request.form['release_year']
            genre_id = request.form['genre_id']
            
            try:
                query = """
                    UPDATE Movie 
                    SET Name = %s, Summary = %s, ReleaseYear = %s, GenreID = %s
                    WHERE MovieID = %s
                """
                cursor.execute(query, (name, summary, release_year, genre_id, movie_id))
                conn.commit()
                flash('Movie updated successfully!', 'success')
                return redirect(url_for('movie_detail', movie_id=movie_id))
                
            except Error as e:
                conn.rollback()
                flash(f'Error updating movie: {e}', 'error')
        
        # Get movie and genres
        cursor.execute("SELECT * FROM Movie WHERE MovieID = %s", (movie_id,))
        movie = cursor.fetchone()
        
        cursor.execute("SELECT GenreID, GenreName FROM Genre ORDER BY GenreName")
        genres = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('movies/edit.html', movie=movie, genres=genres)
    
    return redirect(url_for('list_movies'))

@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """Delete movie (Admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Movie WHERE MovieID = %s", (movie_id,))
            conn.commit()
            flash('Movie deleted successfully!', 'success')
            
        except Error as e:
            conn.rollback()
            flash(f'Error deleting movie: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('list_movies'))

# USER PROFILE ROUTES


@app.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('login'))  
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Get user profile data
            query = """
                SELECT u.UserID, u.Name, u.Email, u.JoinDate,
                       COUNT(DISTINCT r.MovieID) AS MoviesReviewed,
                       COUNT(DISTINCT rv.ReviewID) AS ReviewsWritten,
                       AVG(r2.NumRating) AS AverageRatingGiven,
                       COUNT(DISTINCT um.MoodID) AS DifferentMoodsUsed
                FROM Users u
                LEFT JOIN Rating r ON u.UserID = r.UserID
                LEFT JOIN Review rv ON u.UserID = rv.UserID
                LEFT JOIN Rating r2 ON u.UserID = r2.UserID
                LEFT JOIN UserMood um ON u.UserID = um.UserID
                WHERE u.UserID = %s
                GROUP BY u.UserID
            """
            cursor.execute(query, (session['user_id'],))
            user_profile = cursor.fetchone()
            
            # Get movies reviewed by user
            query = """
                SELECT m.MovieID, m.Name, m.ReleaseYear, g.GenreName,
                       r.NumRating, rv.ReviewText, rv.CreatedAt
                FROM Rating r
                JOIN Movie m ON r.MovieID = m.MovieID
                JOIN Genre g ON m.GenreID = g.GenreID
                LEFT JOIN Review rv ON r.UserID = rv.UserID AND r.MovieID = rv.MovieID
                WHERE r.UserID = %s
                ORDER BY rv.CreatedAt DESC
            """
            cursor.execute(query, (session['user_id'],))
            reviewed_movies = cursor.fetchall()    
            # Get user's most common moods
            query = """
                SELECT mc.MoodName, COUNT(*) AS UsageCount
                FROM UserMood um
                JOIN MoodCategory mc ON um.MoodID = mc.MoodID
                WHERE um.UserID = %s
                GROUP BY mc.MoodName
                ORDER BY UsageCount DESC
            """
            cursor.execute(query, (session['user_id'],))
            user_moods = cursor.fetchall()
            
            return render_template('profile.html', 
                                 user_profile=user_profile,
                                 reviewed_movies=reviewed_movies,
                                 user_moods=user_moods)
            
        except Error as e:
            flash(f'Error loading profile: {e}', 'error')
        finally:
            cursor.close()
            conn.close()   
    return redirect(url_for('list_movies'))


# ADMIN ROUTES


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Get statistics
            cursor.execute("SELECT COUNT(*) AS TotalUsers FROM Users WHERE IsActive = 1")
            stats = cursor.fetchone()
            
            cursor.execute("SELECT COUNT(*) AS TotalMovies FROM Movie")
            stats.update(cursor.fetchone())
            
            cursor.execute("SELECT COUNT(*) AS TotalReviews FROM Review")
            stats.update(cursor.fetchone())
            
            return render_template('admin/dashboard.html', stats=stats)
            
        except Error as e:
            flash(f'Error loading admin dashboard: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('list_movies'))

@app.route('/admin/users')
def admin_users():
    """Manage users (Admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT u.UserID, u.Name, u.Email, u.JoinDate, u.IsActive,
                       CASE 
                           WHEN a.UserID IS NOT NULL THEN 'Admin'
                           WHEN n.UserID IS NOT NULL THEN 'User'
                           ELSE 'Unknown'
                       END AS Role,
                       COUNT(DISTINCT r.MovieID) AS MoviesReviewed
                FROM Users u
                LEFT JOIN Admin a ON u.UserID = a.UserID
                LEFT JOIN NormalUser n ON u.UserID = n.UserID
                LEFT JOIN Rating r ON u.UserID = r.UserID
                GROUP BY u.UserID
                ORDER BY u.JoinDate DESC
            """
            cursor.execute(query)
            users = cursor.fetchall()
            
            return render_template('admin/users.html', users=users)
            
        except Error as e:
            flash(f'Error loading users: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_dashboard'))

# REVIEW CRUD ROUTES


@app.route('/movies/<int:movie_id>/review', methods=['GET', 'POST'])
def add_review(movie_id):
    """Add or update review and rating"""
    if 'user_id' not in session:
        flash('Please login to add a review', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            rating = int(request.form['rating'])
            review_text = request.form.get('review_text', '')
            moods = request.form.getlist('moods')  # Multiple mood selections
            
            try:
                # Insert or update rating
                query = """
                    INSERT INTO Rating (UserID, MovieID, NumRating)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE NumRating = VALUES(NumRating)
                """
                cursor.execute(query, (session['user_id'], movie_id, rating))
                
                # Insert or update review
                if review_text.strip():
                    query = """
                        INSERT INTO Review (UserID, MovieID, ReviewText)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE ReviewText = VALUES(ReviewText)
                    """
                    cursor.execute(query, (session['user_id'], movie_id, review_text))
                
                # Delete existing moods for this movie by this user
                cursor.execute("DELETE FROM UserMood WHERE UserID = %s AND MovieID = %s", 
                             (session['user_id'], movie_id))
                
                # Insert new moods
                for mood_id in moods:
                    query = "INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES (%s, %s, %s)"
                    cursor.execute(query, (session['user_id'], movie_id, int(mood_id)))
                
                conn.commit()
                flash('Review added/updated successfully!', 'success')
                return redirect(url_for('movie_detail', movie_id=movie_id))
                
            except Error as e:
                conn.rollback()
                flash(f'Error adding review: {e}', 'error')
        
        # Get movie details and available moods
        cursor.execute("SELECT MovieID, Name FROM Movie WHERE MovieID = %s", (movie_id,))
        movie = cursor.fetchone()
        
        cursor.execute("SELECT MoodID, MoodName FROM MoodCategory ORDER BY MoodName")
        moods = cursor.fetchall()
        
        # Get existing review if any
        query = """
            SELECT r.NumRating, rv.ReviewText, GROUP_CONCAT(um.MoodID) AS UserMoods
            FROM Rating r
            LEFT JOIN Review rv ON r.UserID = rv.UserID AND r.MovieID = rv.MovieID
            LEFT JOIN UserMood um ON r.UserID = um.UserID AND r.MovieID = um.MovieID
            WHERE r.UserID = %s AND r.MovieID = %s
        """
        cursor.execute(query, (session['user_id'], movie_id))
        existing_review = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('reviews/add.html', movie=movie, moods=moods, 
                             existing_review=existing_review)
    
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/movies/<int:movie_id>/review/delete', methods=['POST'])
def delete_review(movie_id):
    """Delete user's review for a movie"""
    if 'user_id' not in session:
        flash('Please login to delete a review', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Delete rating, review, and moods for this user and movie
            cursor.execute("DELETE FROM Rating WHERE UserID = %s AND MovieID = %s", 
                         (session['user_id'], movie_id))
            cursor.execute("DELETE FROM Review WHERE UserID = %s AND MovieID = %s", 
                         (session['user_id'], movie_id))
            cursor.execute("DELETE FROM UserMood WHERE UserID = %s AND MovieID = %s", 
                         (session['user_id'], movie_id))
            
            conn.commit()
            flash('Review deleted successfully!', 'success')
            
        except Error as e:
            conn.rollback()
            flash(f'Error deleting review: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('movie_detail', movie_id=movie_id))


# SEARCH AND FILTER ROUTES


@app.route('/search')
def search():
    """Search and filter movies"""
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    year = request.args.get('year', '')
    mood = request.args.get('mood', '')
    min_rating = request.args.get('min_rating', '')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Build dynamic query
            base_query = """
                SELECT DISTINCT m.MovieID, m.Name, m.Summary, m.ReleaseYear, g.GenreName,
                       AVG(r.NumRating) AS AverageRating,
                       COUNT(r.NumRating) AS TotalRatings
                FROM Movie m
                JOIN Genre g ON m.GenreID = g.GenreID
                LEFT JOIN Rating r ON m.MovieID = r.MovieID
            """
            
            joins = ""
            conditions = []
            params = []
            
            if mood:
                joins += " JOIN UserMood um ON m.MovieID = um.MovieID JOIN MoodCategory mc ON um.MoodID = mc.MoodID"
                conditions.append("mc.MoodName = %s")
                params.append(mood)
            
            if query:
                conditions.append("(m.Name LIKE %s OR m.Summary LIKE %s)")
                params.extend([f'%{query}%', f'%{query}%'])
            
            if genre:
                conditions.append("g.GenreName = %s")
                params.append(genre)
            
            if year:
                conditions.append("m.ReleaseYear = %s")
                params.append(year)
            
            if min_rating:
                conditions.append("r.NumRating >= %s")
                params.append(float(min_rating))
            
            # Combine query
            full_query = base_query + joins
            if conditions:
                full_query += " WHERE " + " AND ".join(conditions)
            
            full_query += " GROUP BY m.MovieID ORDER BY AverageRating DESC"
            
            cursor.execute(full_query, params)
            movies = cursor.fetchall()
            
            # Get filter options
            cursor.execute("SELECT DISTINCT GenreName FROM Genre ORDER BY GenreName")
            genres = cursor.fetchall()
            
            cursor.execute("SELECT DISTINCT MoodName FROM MoodCategory ORDER BY MoodName")
            moods = cursor.fetchall()
            
            return render_template('search.html', movies=movies, genres=genres, 
                                 moods=moods, query=query, genre=genre, 
                                 year=year, mood=mood, min_rating=min_rating)
            
        except Error as e:
            flash(f'Search error: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('search.html', movies=[])




@app.route('/admin/requests')
def admin_requests():
    """Manage user requests (Admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('list_movies'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT r.*, u.Name AS UserName
                FROM Request r
                JOIN Users u ON r.UserID = u.UserID
                WHERE r.Status = 'PENDING'
                ORDER BY r.CreatedAt DESC
            """
            cursor.execute(query)
            requests = cursor.fetchall()
            
            return render_template('admin/requests.html', requests=requests)
            
        except Error as e:
            flash(f'Error loading requests: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_dashboard'))


# API ROUTES FOR MOOD DATA


@app.route('/api/mood-distribution/<int:movie_id>')
def api_mood_distribution(movie_id):
    """API endpoint to get mood distribution for a movie"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT mc.MoodName, COUNT(*) AS count
                FROM UserMood um
                JOIN MoodCategory mc ON um.MoodID = mc.MoodID
                WHERE um.MovieID = %s
                GROUP BY mc.MoodName
                ORDER BY count DESC
            """
            cursor.execute(query, (movie_id,))
            moods = cursor.fetchall()
            
            return jsonify(moods)
            
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    
    return jsonify([])


# MAIN APPLICATION ENTRY


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)