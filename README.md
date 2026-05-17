Project Documentation
Buddy Travel Planner

Buddy Travel Planner is a full-stack Django web application developed as part of a software development project. The application allows users to organize trips, manage itineraries, explore travel inspiration, and interact with dynamic travel-related features such as maps, weather forecasts, and reviews.


Author: Dana Dvorcakova
Date:   30/05/2026
Link:   https://travel-planner-sege.onrender.com
https://github.com/DanaDvorcakova/travel-planner
Database:  travel_planner_db


Overview

Buddy Travel Planner is a travel management and itinerary planning platform designed for travellers who want to organize trips efficiently while discovering inspiration from other users.

The application allows authenticated users to:
•	Create and manage trips
•	Build detailed itineraries
•	Save favourite destinations
•	Explore travel inspiration
•	View weather forecasts
•	Display trips on interactive maps
•	Leave reviews and ratings
•	Manage profiles and travel preferences
Public visitors can browse published travel inspiration trips without needing an account.


Table of Contents

1.  Objectives
2.  Features
3.  Technologies Used
4.  System Architecture
5.  Database Design
6.  ER Diagram
7.  Application Structure
8.  Models Explanation
9.  Views & Functionality
10. Frontend Features
11.  Application Screenshots
12. API Integrations
13. Authentication & Security
14. CRUD Operations
15. Responsive Design
16. Testing
17. Challenges Faced
18. Future Improvements
19. Installation Guide
20. Deployment
21. Conclusion



1. Objectives

The main objectives of the project are:
•	Build a modern full-stack Django web application
•	Implement complete CRUD functionality
•	Integrate external APIs
•	Create responsive UI/UX design
•	Store and manage travel data efficiently
•	Practice authentication and authorization
•	Use AJAX and JavaScript for dynamic features
•	Display geographical data using maps


2. Main Features

User Authentication
•   User registration 
•   Login/logout system 
•   Password reset functionality 
•   Profile management 

Trip Management
•   Create trips 
•   Edit trips 
•   Delete trips 
•   Publish/unpublish trips 
•   Search and filter trips 

Itinerary Planner
•   Add itinerary items 
•   Organize activities by date/time 
•   Automatic itinerary date shifting 
•   Geolocation support 

Saved Places
•   Save favorite locations 
•   Store coordinates 
•   Add saved places directly into trips 

Interactive Maps
•   Leaflet.js integration 
•   Dynamic map markers 
•   Google Maps links 
•   Route visualization 

Weather Forecast
•   Live weather data 
•   Forecast during trip dates 
•   Future trip weather support 

Country Information
•   Country details from REST Countries API 
•   Travel-related country information 

Reviews & Ratings
•   Leave reviews on published trips 
•   1–5 star rating system 
•   Average rating calculation 

Responsive UI
•   Mobile sidebar navigation 
•   Bootstrap responsive layout 
•   Interactive UI animations


3. Technologies Used

Backend
•   Python 
•   Django 
•   SQLite3 (development) 
•   PostgreSQL (deployment database) 

Frontend
•   HTML5 
•   CSS3 
•   Bootstrap 5 
•   JavaScript 

APIs & Services
•   OpenWeather API 
•   OpenCage Geocoding API 
•   REST Countries API 
•   Leaflet.js Maps 

Deployment
•   GitHub 
•   Render 


4. System Architecture

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
•   Maps 
•   Weather 
•   Country information


5. Database Design

The database consists of the following main entities:
•   User 
•   Profile 
•   Trip 
•   ItineraryItem 
•   SavedPlace 
•   Review 

Relationships are connected using Django ORM ForeignKeys and OneToOneFields.


6. ER Diagram

screenshots/erdiagram.png

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


7. Application Structure

travel-planner/
├── media/
│   ├── avatars/
│   ├── profile_pics/
│   ├── trips/
│   └── trip_photos/
│
├── screenshots/
│   ├── dashboard.png
│   ├── landingpage1.png
│   ├── profile.png
│   └── tripdetailpage1.png
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── inspiration/
│   └── js/
│       └── modules/
│
├── templates/
│   ├── components/
│   ├── registration/
│   └── trips/
│
├── travel_planner/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── trips/
│   ├── migrations/
│   ├── services/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── .env
└── README.md

8. Models Explanation

Profile Model
Extends Django’s built-in User model.

Features
•   User avatar
•   Biography
•   Travel style preferences

Special Feature
Automatically created using Django signals when a new user registers.

Trip Model
Stores trip information.

Fields
•   Title
•   Destination
•   Dates
•   Description
•   Image
•   Publication status

Features
•   Public/private trips
•   Average rating calculation
•   Timestamp tracking

SavedPlace Model
Stores favorite places saved by users.

Features
•   Coordinates storage
•   Place images
•   Future map support
•   Integration with itineraries

ItineraryItem Model
Represents activities/events inside trips.

Features
•   Date & time organization
•   Automatic geocoding
•   Map integration
•   Notes support

Review Model
Stores trip reviews and ratings.


Features
•   1–5 star ratings
•   One review per user per trip
•   Average rating calculation


9. Views & Functionality

Authentication Views
•   Signup 
•   Login 
•   Logout 
•   Password reset 

Dashboard
Displays:
•   User trips 
•   Trip statistics 
•   Upcoming trips 
•   Search and filters 

Trip Management
•   Add trip 
•   Edit trip 
•   Delete trip 
•   Trip details 

Saved Places
•   Save destinations 
•   Search places 
•   AJAX save functionality 

Itinerary Management
•   Add itinerary item 
•   Edit item 
•   Delete item 

Reviews
•   Add review 
•   Edit review 
•   Delete review


10. Frontend Features

Bootstrap UI
The application uses Bootstrap 5 together with custom CSS to create a modern, responsive, and mobile-friendly user interface.

Features include:
•	Responsive layouts 
•	Grid-based design 
•	Styled forms and cards 
•	Buttons, modals, and alerts 
•	Mobile-friendly navigation 

Responsive Design

The frontend automatically adapts to:
•	Desktop screens 
•	Tablets 
•	Mobile devices 

Responsive features include:
•	Mobile sidebar navigation 
•	Adaptive card layouts 
•	Responsive maps and images 
•	Flexible dashboard sections 

Interactive Maps

Leaflet.js is used to display:
•	Dynamic itinerary markers 
•	Trip locations 
•	Interactive popups 
•	Map filtering by itinerary day 

AJAX Functionality

AJAX is implemented to improve user experience without requiring full page reloads.
Used for:
•	Saving places dynamically 
•	Adding saved places into trips 
•	Displaying success/error feedback 
Search & Filtering

The frontend includes dynamic search and filtering features for:
•	Trips 
•	Saved places 
•	Destinations 
Pagination is also implemented to improve usability and performance.

JavaScript Interactions

JavaScript is used for interactive UI functionality, including:
•	Collapsible itinerary sections 
•	Show/hide controls 
•	Modal confirmations 
•	Dynamic map rendering 
•	Mobile sidebar toggling 

User Feedback Components

The application provides visual feedback through:
•	Toast notifications 
•	Validation messages 
•	Confirmation modals 
•	Loading and empty-state messages 


11. Application Screenshots

Landing page

screenshots/landingpage1.png
screenshots/landingpage2.png

The landing page is the main public page of the Buddy Travel Planner application. It introduces users to the platform through a responsive hero section with a background image, search functionality, and call-to-action buttons.
Users can browse popular destinations through a horizontal carousel and explore published trips shared by the community. Each trip card displays trip images, destinations, travel dates, ratings, and creator information.
The page also highlights key application features such as trip planning, itinerary management, interactive maps, and travel organization.
    
   
Dashboard

screenshots/dashboard.png

The dashboard is the main private area for authenticated users where they can manage and organize their trips. It provides quick access to trip information, statistics, and planning tools in a responsive and user-friendly layout.

The dashboard includes:
•	A personalized trip overview 
•	Upcoming trip countdown section 
•	Travel statistics cards 
•	Search and filtering functionality 
•	A responsive grid displaying user trips 
•	Edit and delete trip actions 
•	Pagination for improved usability 

Each trip card displays trip images, destinations, travel dates, and publication status (public or private). Users can quickly access trip details, edit existing trips, or remove trips using confirmation modals.

 
Add trip form

screenshots/addtripform.png

The Add Trip page allows authenticated users to create and save new travel plans through a responsive and user-friendly form interface.

The form includes:
•	Trip title and destination 
•	Start and end travel dates 
•	Trip description 
•	Cover image upload 
•	Public/private trip visibility option 

Validation is implemented to ensure correct date selection and required field completion. Error messages are displayed directly below invalid form fields to improve usability.

Users can:
•	Upload custom trip images 
•	Publish trips publicly or keep them private 
•	Save trip information directly to the database 

 


Trip detail page

screenshots/tripdetailpage1.png
screenshots/tripdetailpage2.png

The Trip Detail page displays complete information about a selected trip and serves as the main trip management and viewing interface.

The page includes:
•	Trip title, destination, and travel dates 
•	Trip cover image and description 
•	Interactive itinerary organized by travel days 
•	Weather forecast integration using the OpenWeather API 
•	Country information retrieved from the REST Countries API 
•	Interactive Leaflet.js map displaying itinerary locations 
•	User reviews and ratings system 

Trip owners can:
•	Edit or delete trips 
•	Publish or unpublish trips 
•	Manage itinerary items 
•	Access the itinerary planner 

Users can also leave reviews and ratings on published trips. The reviews section and “Jump to Reviews” button are only displayed for published trips, ensuring that reviews are available only on publicly shared content. The page includes responsive layouts, collapsible itinerary sections, modal confirmations, and dynamic JavaScript interactions for improved user experience.


Saved places page

screenshots/savedplaces.png

The Saved Places page allows users to store and manage destinations they would like to visit in the future.
Users can:
•	Search saved places 
•	Add custom places manually 
•	Search real-world locations using external APIs 
•	Add saved places directly into trips and itineraries 
•	Delete saved places using confirmation modals 
The page displays saved locations in a card-based layout containing:
•	Place image 
•	Place name and location 
•	Short description 
•	Trip integration controls 

AJAX functionality is used to dynamically add saved places to trips without reloading the page. Pagination and search filtering are implemented to improve usability and performance.
 

Itinerary planner

screenshots/itineraryplanner.png

The Itinerary Planner page allows users to organize and manage activities for a specific trip. It displays trip information, including destination and travel dates, and groups itinerary items by day using collapsible sections. 
Users can add, edit, and delete itinerary activities, while “Show All” and “Hide All” buttons improve navigation through the schedule. 
Confirmation modals are used before deleting itinerary items to prevent accidental removal. 


Profile

screenshots/profile.png

The Profile page allows users to manage their personal account and travel preferences. Users can update their username, email address, profile avatar, biography, and preferred travel style through a structured profile form.

The page displays user profile information, including:
•	Profile avatar 
•	Username 
•	Biography 
•	Travel style badge 

Users can upload profile images and customize their travel profile to personalize their experience within the application. 

Responsive Design
The application was designed using Bootstrap 5 and custom CSS to ensure responsive layouts across desktop, tablet, and mobile devices. Components such as navigation menus, cards, forms, maps, and dashboards automatically adapt to different screen sizes for improved usability and accessibility.


12. API Integrations

OpenWeather API
Used to display:
•   Current weather 
•   Forecasts during trips 

OpenCage API
Used for:
•   Geocoding locations 
•   Latitude/longitude conversion 

REST Countries API
Used to retrieve:
•   Country information 
•   Regional travel data 

Leaflet.js
Used for:
•   Interactive maps 
•   Place markers 
•   Dynamic map rendering



13. Authentication & Security

Security Features
•   Django authentication system 
•   CSRF protection 
•   Login required decorators 
•   Access control for unpublished trips 
•   User ownership validation 

Access Restrictions
Users can only:
•   Edit their own trips 
•   Delete their own reviews 
•   Access their own saved places


User Roles & Permissions

Guest User (Unauthenticated)
Can:
•	View landing page 
•	Browse published trips 
•	Search and filter trips 
•	View reviews 
•	View maps and weather information 
Cannot:
•	Create trips 
•	Leave reviews 
•	Save places 
•	Access dashboard features 

Authenticated Traveler (Registered User)
Can:
•	Create trips 
•	Edit own trips 
•	Delete own trips 
•	Publish or unpublish own trips 
•	Manage itinerary items 
•	Save favourite places 
•	Write reviews 
•	Edit or delete own reviews 
Cannot:
•	Edit trips created by other users 
•	Delete reviews created by other users 
•	Access Django admin panel 
•	View private trips belonging to other users 

Admin (Superuser)
Can:
•	Manage users 
•	Moderate reviews 
•	Edit or delete any trip 
•	Remove inappropriate content 
•	Unpublish trips 
•	Access Django admin dashboard


14. CRUD Operations

Feature           Create   Read    Update   Delete
Trips               ✓       ✓       ✓        ✓
Itinerary Items     ✓       ✓       ✓        ✓
Saved Places        ✓       ✓       ✓        ✓
Reviews             ✓       ✓       ✓        ✓
Profiles            ✓       ✓       ✓        -


15. Responsive Design

The application is fully responsive using Bootstrap 5.
Mobile Features
•   Collapsible sidebar
•   Responsive cards
•   Mobile navigation
•   Adaptive layouts


16. Testing 

Functional and Manual Testing
The application was tested throughout development to ensure all major functionality worked correctly.

Testing included:

•	Authentication testing 
•	CRUD functionality testing 
•	API integration testing 
•	Responsive design testing 
•	Access control testing 
•	JavaScript interaction testing 

Authentication Testing

Feature	      Expected Result	                  Result
User registration	New account created	            Pass
Login	            User redirected to dashboard	      Pass
Logout	      Session ended successfully	      Pass
Protected routes	Redirect unauthenticated users	Pass

CRUD Testing

Feature	      Create	Read	      Update	Delete
Trips		      Pass	      Pass	      Pass        Pass
Itinerary Items	Pass	      Pass	      Pass	      Pass
Saved Places	Pass	      Pass	      Pass	      Pass
Reviews	      Pass	      Pass	      Pass	      Pass

API Testing

API	                  Purpose	            Result
OpenWeather API	      Weather forecasts	      Pass
OpenCage API	      Geolocation coordinates	Pass
REST Countries API	Country information	Pass


Responsive Testing

The application was tested on:
•	Mobile devices 
•	Tablets 
•	Desktop screens 

Bootstrap 5 responsive utilities were used to ensure layouts adapted correctly across screen sizes.

Security Testing

The following security features were tested:
•	CSRF protection 
•	Login required decorators 
•	User ownership validation 
•	Private trip access restrictions 

Testing Summary

Testing confirmed that:
•	Core application features function correctly 
•	APIs integrate successfully 
•	Authentication and authorization work securely 
•	Responsive layouts display properly on different devices


Automated Unit Testing
The project includes automated unit and integration tests implemented using Django’s built-in TestCase framework. The test suite was designed to verify core application functionality, user permissions, validation handling, and external service integration.

The tests verify:
•	Authentication functionality 
•	CRUD operations 
•	Permissions and access control 
•	AJAX requests 
•	Form validation 
•	Django messages framework 
•	External API handling 
•	Trip detail rendering 
•	Edge cases and error handling 

Mocking was used for external APIs (weather, maps, and country information services) to prevent unnecessary live API requests during testing and to ensure reliable, isolated test execution.

Technologies Used for Testing
•	Django TestCase 
•	Django Client 
•	unittest.mock 
•	Reverse URL testing 
•	Coverage.py 

Example Test Areas

Test Category	      Description
Authentication Tests	Login, logout, signup, protected routes
Trip Tests	            Create, edit, delete, and view trips
Itinerary Tests	      Add, edit, and delete itinerary items
AJAX Tests	            Save place and add-to-trip functionality
Permission Tests	      Prevent unauthorized access
API Tests	            Weather and map API handling
Profile Tests	      User profile updates and validation
Validation Tests        Invalid form submissions and edge cases

Test Coverage
Code coverage analysis was performed using the coverage package to measure how much of the application is exercised by automated tests.

Coverage Summary
File	                        Coverage
trips/views.py	            75%
trips/forms.py	            97%
trips/models.py	            90%
travel_planner/settings.py	91%
manage.py	                  82%
Total Project Coverage	      82%

The final automated test suite achieved:
•	82% overall code coverage 
•	75% coverage of views.py 
•	100% coverage of tests.py 

Testing was performed using:
python manage.py test
coverage run manage.py test
coverage report


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
•   AI trip recommendations
•   Budget tracking
•   Flight integration
•   Hotel booking support
•   Drag-and-drop itinerary planner
•   Social features/following users
•   Notifications system
•   Dark mode
•   Real-time chat
•   Multi-language support


19. Installation Guide

Clone Repository
cd travel-planner
git clone https://github.com/DanaDvorcakova/travel-planner.git

Create Virtual Environment
python -m venv venv

Activate Environment
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run Migrations
python manage.py migrate

Create a Superuser
To access the Django admin panel, create a superuser account by running:
python manage.py createsuperuser

Start Server
python manage.py runserver

The server will run at http://127.0.0.1:8000/. Open this URL in your browser to access the app.
Admin Panel
You can access the Django admin panel at http://127.0.0.1:8000/admin/ and log in with the superuser credentials you just created.


20. Deployment on Render with PostgreSQL

Set Up PostgreSQL on Render
Create a PostgreSQL Database on Render
Go to the Render Dashboard.
Click on New > Database > PostgreSQL.
Choose the appropriate region and settings for your database.
After the database is created, Render will provide a Database URL which looks like this:
postgres://username:password@host:port/database_name

Configure PostgreSQL in Your Django Project
Install PostgreSQL Dependencies:
In your project directory, activate your virtual environment and install the PostgreSQL driver:
pip install psycopg2
Update settings.py for PostgreSQL:
Open settings.py in your travel_planner folder, and replace the default SQLite database configuration with PostgreSQL settings. Modify the DATABASES configuration like this:
import os
from dotenv import load_dotenv
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
This configuration uses environment variables to securely handle sensitive data, such as database credentials.

Create .env File for Environment Variables
Create a .env file at the root of your project to store your database credentials and other sensitive information. An example .env file:
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

Make sure to replace the placeholders (your_database_name, your_database_user, etc.) with the actual values provided by Render when you created the PostgreSQL database.
Install python-dotenv
To load environment variables from the .env file, you need to install the python-dotenv package:
pip install python-dotenv
This package will automatically load the environment variables when the application starts.

Apply Migrations
After setting up the database, you will need to run the migrations to create the necessary tables:
python manage.py migrate

Deploy the Application on Render
Create a New Web Service on Render
Go to the Render Dashboard and click New > Web Service.

Select your GitHub repository that contains your project.
Choose the Python environment and the correct branch (usually main or master).
Set the Build Command to:
pip install -r requirements.txt
Set the Start Command to:
gunicorn travel_planner.wsgi:application

Configure Environment Variables on Render
In the Environment Variables section on Render, add the same environment variables as in your .env file:
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
These variables will be used to configure the connection to your PostgreSQL database in the settings.py file.

Deploy the Application
Click Create Web Service to deploy your application. Render will automatically:
Pull your code from GitHub.
Install dependencies.
Set up the PostgreSQL database.
Start the app.

Access Your Application
Once the deployment is complete, Render will provide a URL where your app is hosted (e.g., https://your-app-name.onrender.com).



21. Conclusion

Buddy Travel Planner demonstrates full-stack web development concepts using Django, Bootstrap, JavaScript, and external APIs.

The application successfully combines:
•   User authentication
•   Database management
•   API integration
•   Interactive maps
•   Responsive design
•   AJAX functionality
•   CRUD operations

The project showcases both backend and frontend development skills while solving a real-world travel planning problem.

The project demonstrates practical implementation of full-stack web development principles while providing a modern and user-friendly travel planning experience.



