
# MoodScape - A Mood-Based Movie Review Platform

## 📚Project for CSE370 (Database Systems)

**Project Title:** MoodScape – A Mood-Based Movie Review Platform  
**Course:** CSE370 - Database Systems  


---

## 🎯 Project Overview

MoodScape is a web application where users review movies based on emotions (moods) instead of only numerical ratings. The system demonstrates strong SQL usage including normalized schemas (3NF), foreign keys, many-to-many relationships, aggregate queries, CRUD operations, and role-based access control.

### Key Features
- **Mood-Based Reviews**: Users can tag movies with multiple mood tags (Happy, Emotional, Inspired, Tense, etc.)
- **Comprehensive Rating System**: 1-10 numerical ratings with written reviews
- **Advanced Search & Filter**: Search by title, genre, year, mood, or rating range
- **User Profiles**: Track review history, rating patterns, and mood preferences
- **Admin Panel**: Manage movies, users, and moderate content
- **Analytics**: Mood distribution charts and aggregate statistics

---

## 🛠 Technology Stack

**Frontend:** HTML + CSS   
**Backend:** Python Flask  
**Database:** MySQL (normalized to 3NF)  
**Charts:** Chart.js for mood distribution visualization  
**Authentication:** Flask sessions with password hashing

---



## 📁 Project Structure

```
moodscape/
├── backend/
│   ├── app.py                 # Flask application with CRUD routes
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── login.html         # User login
│   │   ├── register.html      # User registration
│   │   ├── search.html        # Search and filter movies
│   │   ├── profile.html       # User profile
│   │   ├── movies/
│   │   │   ├── list.html      # List all movies
│   │   │   ├── detail.html    # Movie details with reviews
│   │   │   ├── add.html       # Add movie (admin)
│   │   │   └── edit.html      # Edit movie (admin)
│   │   ├── reviews/
│   │   │   └── add.html       # Add/edit reviews
│   │   └── admin/
│   │       ├── dashboard.html # Admin dashboard
│   │       ├── users.html     # Manage users
│   │       └── requests.html  # User requests
│   └── static/
│       ├── css/
│       │   └── style.css      
│       └── js/
│           └── main.js        
├── database/
│   ├── schema.sql             # CREATE TABLE statements (3NF normalized)
│   ├── sample_data.sql        # Sample INSERT statements

└── README.md                  # Project documentation
```

---

## 🔧 Core Functionality

### User Features

#### 1. View Movies
- **Route**: `/movies`
- **Query**: Lists all movies with average ratings using aggregate functions

#### 2. Movie Details
- **Route**: `/movies/<movie_id>`
- **Features**: Summary, average rating, mood distribution (pie chart), user reviews
- **API**: `/api/mood-distribution/<movie_id>` returns JSON mood data

#### 3. Add Review + Rating + Moods
- **Route**: `/movies/<movie_id>/review`
- **Database Operations**:
  - INSERT/UPDATE Rating (one per user per movie constraint)
  - INSERT/UPDATE Review
  - DELETE existing UserMood + INSERT new UserMood entries

#### 4. Edit/Delete Review
- **Route**: `/movies/<movie_id>/review` (GET shows existing review)
- **Database Operations**:
  - DELETE FROM Rating, Review, UserMood
  - CASCADE deletes maintain referential integrity

#### 5. Search & Filter
- **Route**: `/search`
- **Features**: Search by title, genre, year, mood, rating range
- **Query**: Dynamic SQL with JOINs across multiple tables

#### 6. User Profile
- **Route**: `/profile`
- **Features**: Review history, rating patterns, most used moods
- **Query**: Complex aggregation with GROUP BY and COUNT(DISTINCT)

### Admin Features

#### 1. Manage Movies
- **Routes**: `/movies/add`, `/movies/<id>/edit`, `/movies/<id>/delete`
- **Features**: Full CRUD operations with referential integrity

#### 2. Manage Users
- **Route**: `/admin/users`
- **Features**: View all users, ban/unban users
- **Query**: LEFT JOIN with role tables and aggregate statistics



---
### Features Implemented
- ✅ User authentication & authorization
- ✅ Movie CRUD operations
- ✅ Review system with ratings
- ✅ Mood tagging system
- ✅ Search & filtering
- ✅ Admin dashboard
- ✅ Data visualization
- ✅ User profiles
- ✅ Database analytics









