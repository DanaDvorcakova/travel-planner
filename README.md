




Good README screenshots make your project look much more professional.


Guest opens app → public landing page
User logs in → personalized landing page
User clicks Dashboard when they want CRUD/manage trips

travel_planner/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── travel_planner/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── trips/
│   ├── migrations/
│   │   └── __init__.py
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   │   base.html
│   │
│   ├── registration/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── password_reset_complete.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_done.html
│   │   └── password_reset_form.html
│   │
│   └── trips/
│       ├── add_itinerary_item.html
│       ├── add_saved_place.html
│       ├── add_trip.html
│       ├── dashboard.html
│       ├── delete_itinerary_item.html
│       ├── delete_trip.html
│       ├── edit_itinerary_item.html
│       ├── edit_review.html
│       ├── edit_trip.html
│       ├── home.html
│       ├── itinerary.html
│       ├── place_detail.html
│       ├── saved_places.html
│       ├── search_places.html
│       ├── trip_detail.html
│       └── trips_list.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   └── images/
│       ├── hero.jpg
│       ├── logo.png
│       ├── placeholder.jpg
│       │
│       └── inspiration/
│           ├── bali.jpg
│           ├── barcelona.jpg
│           ├── ny.jpeg
│           ├── paris.jpg
│           ├── rome.jpg
            └── tokyo.jpg

Example Screenshot Section
1. Landing Page

(Insert screenshot here)

Description

The landing page is the main public page of the application.
It allows users to:

Browse published travel inspirations
Search trips by destination
Filter trips by travel style
Navigate to authentication pages

The page is fully responsive and built using Bootstrap 5.

Type of Users:

Guest User (Unauthenticated)
Can:
•	view landing page 
•	browse published trips 
•	search/filter trips 
•	view reviews 
•	view maps/weather 
Cannot:
•	create trips 
•	review 
•	save places 
•	dashboard access 

Authenticated Traveler (Normal User)
Can:
•	create trips 
•	edit OWN trips 
•	delete OWN trips 
•	publish OWN trips 
•	manage itinerary 
•	save places 
•	write reviews 
•	edit/delete OWN reviews 
Cannot:
•	edit others’ trips 
•	delete others’ reviews 
•	access admin panel 
•	view private drafts of other users 


Admin (Django Admin / Superuser)
Can:
•	moderate content 
•	remove reviews 
•	remove trips 
•	manage users
•	edit/delete any trip 
•	unpublish inappropriate trips


2. Dashboard

(Insert screenshot here)

Description

The dashboard displays all trips created by the authenticated user.
Users can:

View trip statistics
Search and filter trips
Edit or delete trips
Access itinerary planning features

Pagination is implemented to improve performance and usability.

3. Trip Detail Page

(Insert screenshot here)

Description

The trip detail page displays complete information about a selected trip, including:

Trip overview
Interactive Leaflet map
Weather forecast
Country information
Itinerary items
User reviews and ratings

External APIs are integrated dynamically to provide real-time travel data.







Buddy Travel Planner

A full-stack travel planning web application built with Django that allows users to create personalized travel itineraries, save destinations, explore public trip inspirations, view interactive maps, check live weather forecasts, and review trips shared by the community.

The platform combines trip management, location services, mapping technologies, and social travel inspiration into a single responsive web application.


Table of Contents
1.	Objectives
2.	Features
3.	Technologies Used
4.	System Architecture
5.	Database Design
6.	ER Diagram
7.	Application Structure
8.	Models Explanation
9.	Views & Functionality
10.	Frontend Features
11.	 Application Screenshots
12.	API Integrations
13.	Authentication & Security
14.	CRUD Operations
15.	Responsive Design
16.	Challenges Faced
17.	Future Improvements
18.	Installation Guide
19.	Deployment
20.	Conclusion




1. Project Overview

Buddy Travel Planner is a travel management and itinerary planning platform designed for travelers who want to organize trips efficiently while discovering inspiration from other users.

The application allows authenticated users to:

Create and manage trips
Build detailed itineraries
Save favorite destinations
Explore travel inspiration
View weather forecasts
Display trips on interactive maps
Leave reviews and ratings
Manage profiles and travel preferences

Public visitors can browse published travel inspiration trips without needing an account.


2. Objectives

The main objectives of the project are:

Build a modern full-stack Django web application
Implement complete CRUD functionality
Integrate external APIs
Create responsive UI/UX design
Store and manage travel data efficiently
Practice authentication and authorization
Use AJAX and JavaScript for dynamic features
Display geographical data using maps


3. Main Features
User Authentication
•	User registration 
•	Login/logout system 
•	Password reset functionality 
•	Profile management 
Trip Management
•	Create trips 
•	Edit trips 
•	Delete trips 
•	Publish/unpublish trips 
•	Search and filter trips 
Itinerary Planner
•	Add itinerary items 
•	Organize activities by date/time 
•	Automatic itinerary date shifting 
•	Geolocation support 
Saved Places
•	Save favorite locations 
•	Store coordinates 
•	Add saved places directly into trips 
Interactive Maps
•	Leaflet.js integration 
•	Dynamic map markers 
•	Google Maps links 
•	Route visualization 
Weather Forecast
•	Live weather data 
•	Forecast during trip dates 
•	Future trip weather support 
Country Information
•	Country details from REST Countries API 
•	Travel-related country information 
Reviews & Ratings
•	Leave reviews on published trips 
•	1–5 star rating system 
•	Average rating calculation 
Responsive UI
•	Mobile sidebar navigation 
•	Bootstrap responsive layout 
•	Interactive UI animations



4. Technologies Used
Backend
•	Python 
•	Django 
•	SQLite3 (development) 
•	PostgreSQL (planned deployment database) 
Frontend
•	HTML5 
•	CSS3 
•	Bootstrap 5 
•	JavaScript 
APIs & Services
•	OpenWeather API 
•	OpenCage Geocoding API 
•	REST Countries API 
•	Leaflet.js Maps 
Deployment
•	GitHub 
•	Render 


5. System Architecture

The project follows the Django MVT (Model-View-Template) architecture.

Components:
Models
Handle database structure and relationships.

Views
Contain business logic and application functionality.

Templates
Render dynamic frontend pages using Django templating.

Static Files
Contain CSS, JavaScript, and images.

Services
Handle external API integrations:
•	Maps 
•	Weather 
•	Country information


6. Database Design

The database consists of the following main entities:
•	User 
•	Profile 
•	Trip 
•	ItineraryItem 
•	SavedPlace 
•	Review 

Relationships are connected using Django ORM ForeignKeys and OneToOneFields.


7. ER Diagram
┌──────────────────────────────────────┐
│                User                  │
├──────────────────────────────────────┤
│ PK  id                               │
│     username                         │
│     email                            │
│     password                         │
│     date_joined                      │
└─────────────────┬────────────────────┘
                  │ 1
                  │
                  │ 1
┌─────────────────▼────────────────────┐
│               Profile                │
├──────────────────────────────────────┤
│ PK  id                               │
│ FK  user_id                          │
│     avatar                           │
│     bio                              │
│     travel_style                     │
└──────────────────────────────────────┘



┌──────────────────────────────────────┐
│                User                  │
└─────────────────┬────────────────────┘
                  │ 1
                  │
                  │ *
┌─────────────────▼────────────────────┐
│                 Trip                 │
├──────────────────────────────────────┤
│ PK  id                               │
│ FK  user_id                          │
│     title                            │
│     destination                      │
│     start_date                       │
│     end_date                         │
│     description                      │
│     image                            │
│     is_published                     │
│     created_at                       │
│     updated_at                       │
└─────────────────┬────────────────────┘
                  │ 1
                  │
                  │ *
┌─────────────────▼────────────────────┐
│            ItineraryItem             │
├──────────────────────────────────────┤
│ PK  id                               │
│ FK  trip_id                          │
│     title                            │
│     location                         │
│     latitude                         │
│     longitude                        │
│     date                             │
│     time                             │
│     notes                            │
│     created_at                       │
└──────────────────────────────────────┘



┌──────────────────────────────────────┐
│                User                  │
└─────────────────┬────────────────────┘
                  │ 1
                  │
                  │ *
┌─────────────────▼────────────────────┐
│             SavedPlace               │
├──────────────────────────────────────┤
│ PK  id                               │
│ FK  user_id                          │
│     name                             │
│     location                         │
│     latitude                         │
│     longitude                        │
│     description                      │
│     image                            │
│     rating                           │
│     created_at                       │
└──────────────────────────────────────┘



┌──────────────────────────────────────┐
│                User                  │
└─────────────────┬────────────────────┘
                  │ 1
                  │
                  │ *
┌─────────────────▼────────────────────┐
│               Review                 │
├──────────────────────────────────────┤
│ PK  id                               │
│ FK  user_id                          │
│ FK  trip_id                          │
│     comment                          │
│     rating                           │
│     created_at                       │
└─────────────────┬────────────────────┘
                  │ *
                  │
                  │ 1
┌─────────────────▼────────────────────┐
│                 Trip                 │
└──────────────────────────────────────┘

Relationships Explanation
User → Profile
One-to-One relationship.
Each user has exactly one profile.

User → Trip
One-to-Many relationship.
One user can create many trips.

Trip → ItineraryItem
One-to-Many relationship.
One trip can contain multiple itinerary items.

User → SavedPlace
One-to-Many relationship.
Users can save many favorite places.

User → Review
One-to-Many relationship.
Users can write multiple reviews.

Trip → Review
One-to-Many relationship.
One trip can receive many reviews.



Search Places
      ↓
OpenCage API
      ↓
SavedPlace
      ↓
Add To Trip
      ↓
ItineraryItem
      ↓
Leaflet Map Display
      ↓
Weather + Country APIs
      ↓
Trip Detail Page



8. Application Structure

travel_planner/
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│   ├── registration/
│   └── trips/
│
├── travel_planner/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── trips/
│   ├── migrations/
│   ├── services/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
└── manage.py


9. Models Explanation

Profile Model
Extends Django’s built-in User model.

Features
•	User avatar
•	Biography
•	Travel style preferences

Special Feature
Automatically created using Django signals when a new user registers.


Trip Model
Stores trip information.

Fields
•	Title
•	Destination
•	Dates
•	Description
•	Image
•	Publication status

Features
•	Public/private trips
•	Average rating calculation
•	Timestamp tracking


SavedPlace Model
Stores favorite places saved by users.

Features
•	Coordinates storage
•	Place images
•	Future map support
•	Integration with itineraries


ItineraryItem Model
Represents activities/events inside trips.

Features
•	Date & time organization
•	Automatic geocoding
•	Map integration
•	Notes support


Review Model
Stores trip reviews and ratings.

Features
•	1–5 star ratings
•	One review per user per trip
•	Average rating calculation


10. Views & Functionality
Authentication Views
•	Signup 
•	Login 
•	Logout 
•	Password reset 

Dashboard
Displays:
•	User trips 
•	Trip statistics 
•	Upcoming trips 
•	Search and filters 

Trip Management
•	Add trip 
•	Edit trip 
•	Delete trip 
•	Trip details 

Saved Places
•	Save destinations 
•	Search places 
•	AJAX save functionality 

Itinerary Management
•	Add itinerary item 
•	Edit item 
•	Delete item 

Reviews
•	Add review 
•	Edit review 
•	Delete review


11. Application Screenshots

Landing page
Dashboard
Add trip form
Trip detail page
Interactive map
Saved places page
Itinerary planner
Weather section
Reviews section
Mobile responsive sidebar

Example Screenshot Section
Landing Page

(Insert screenshot here)

Description

The landing page is the main public page of the application.
It allows users to:

Browse published travel inspirations
Search trips by destination
Filter trips by travel style
Navigate to authentication pages

The page is fully responsive and built using Bootstrap 5.

Dashboard

(Insert screenshot here)

Description

The dashboard displays all trips created by the authenticated user.
Users can:

View trip statistics
Search and filter trips
Edit or delete trips
Access itinerary planning features

Pagination is implemented to improve performance and usability.

Trip Detail Page

(Insert screenshot here)

Description

The trip detail page displays complete information about a selected trip, including:

Trip overview
Interactive Leaflet map
Weather forecast
Country information
Itinerary items
User reviews and ratings

External APIs are integrated dynamically to provide real-time travel data.



12. Frontend Features
Bootstrap UI
Responsive and mobile-friendly design.

Sidebar Navigation
Dynamic sidebar for authenticated users.

Interactive Maps
Leaflet.js maps with markers and filtering.

AJAX Features
•	Save places without page reload
•	Add places to trips dynamically

Live Search
Real-time filtering using JavaScript.

Toast Notifications
User feedback messages for actions.


13. API Integrations
OpenWeather API
Used to display:
•	Current weather 
•	Forecasts during trips 

OpenCage API
Used for:
•	Geocoding locations 
•	Latitude/longitude conversion 

REST Countries API
Used to retrieve:
•	Country information 
•	Regional travel data 

Leaflet.js
Used for:
•	Interactive maps 
•	Place markers 
•	Dynamic map rendering


14. Authentication & Security
Security Features
•	Django authentication system 
•	CSRF protection 
•	Login required decorators 
•	Access control for unpublished trips 
•	User ownership validation 

Access Restrictions
Users can only:
•	Edit their own trips 
•	Delete their own reviews 
•	Access their own saved places


15. CRUD Operations

Feature	          Create   Read	   Update	Delete
Trips	            ✓	    ✓	    ✓	    ✓
Itinerary Items 	✓	    ✓	    ✓	    ✓
Saved Places	    ✓	    ✓	    ✓	    ✓
Reviews	            ✓	    ✓	    ✓	    ✓
Profiles	        ✓	    ✓	    ✓	    -


16. Responsive Design

The application is fully responsive using Bootstrap 5.

Mobile Features
•	Collapsible sidebar
•	Responsive cards
•	Mobile navigation
•	Adaptive layouts


17. Challenges Faced
API Integration
Handling external APIs and asynchronous requests.

Map Visualization
Managing dynamic map markers and coordinates.

Access Control
Restricting private trip visibility securely.

Dynamic Itinerary Updates
Automatically adjusting itinerary dates when trip dates change.


18. Future Improvements

Possible future features include:
•	AI trip recommendations
•	Budget tracking
•	Flight integration
•	Hotel booking support
•	Drag-and-drop itinerary planner
•	Social features/following users
•	Notifications system
•	Dark mode
•	Real-time chat
•	Multi-language support


19. Installation Guide
Clone Repository
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner

Create Virtual Environment
python -m venv venv

Activate Environment
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run Migrations
python manage.py migrate

Start Server
python manage.py runserver


20. Deployment
Planned Deployment
•	GitHub for version control
•	Render for hosting
•	PostgreSQL database for production
•	Environment Variable

The following API keys should be stored securely:
env
OPENCAGE_API_KEY=
OPENWEATHER_API_KEY=
SECRET_KEY=
DEBUG=False


21. Conclusion

Buddy Travel Planner demonstrates full-stack web development concepts using Django, Bootstrap, JavaScript, and external APIs.

The application successfully combines:
•	User authentication
•	Database management
•	API integration
•	Interactive maps
•	Responsive design
•	AJAX functionality
•	CRUD operations

The project showcases both backend and frontend development skills while solving a real-world travel planning problem.