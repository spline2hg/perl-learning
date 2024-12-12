---

# Peer-to-Peer Learning Platform

A peer-to-peer learning platform that connects learners with educators to facilitate skill-based learning through live video sessions, messaging, and interactive classrooms.

## Features

- **User Roles**: Two types of users – Learners and Educators.
  - **Learners** can search for courses, join classrooms, and engage in live sessions with educators.
  - **Educators** can create classrooms, share their knowledge, and interact with learners.
  
- **Classrooms**: Create and join virtual classrooms to facilitate learning.
  
- **Live Video Sessions**: Conduct live video calls for real-time learning sessions between educators and learners.
  
- **Messaging**: Direct messaging feature within classrooms for discussion and support.

## Technologies Used

- **Backend**: Django
- **Database**: PostgreSQL
- **Video Calling**: WebRTC, Twilio, or other WebRTC-based libraries
- **Cloud Storage**: Cloudinary (for image/video storage)
- **Frontend**: HTML, CSS, JavaScript
- **Hosting**: Render

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- PostgreSQL (for the database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peer-to-peer-learning-platform.git
   cd peer-to-peer-learning-platform
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` :
   ```env
   ENVIRONMENT=development
   DATABASE_URL=postgresql://ps:<your_database_password>@<your_host>/<your_database_name>
   serverSecret=<your_server_secret>
   appID=<your_app_id>
   SECRET_KEY=<your_django_secret_key>
   CLOUDINARY_URL=cloudinary://<cloud_name>:<api_key>:<api_secret>
   MEETING_U=<your_meeting_id_here>
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```


## Usage

### As a Learner:
- Sign up and browse available classrooms.
- Join a classroom of your choice and participate in live video sessions with educators.
- Send and receive messages within the classroom for better collaboration.

## As an Educator:
- Create a new classroom and specify the skills you're teaching.
- Invite learners to join your classroom and start live sessions.
- Share educational resources and interact with learners in real-time.


 Thank you. This project may become a fresh breeze on a quiet morning, a moment of peace in a world full of noise. It’s in these rare, still moments that the true value of what’s meaningful becomes clear. Kindness, like this, is a collective healing that resonates beyond words.
