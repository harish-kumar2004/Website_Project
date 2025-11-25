# LeSuccess Placement Academy - Flask Integration

This project integrates static HTML frontend files with a Python Flask backend to create a fully functional web application for "LeSuccess Placement Academy." The application features a hybrid architecture where most pages are served as static templates, while the chat.html page provides real-time AI chat functionality.

## Project Structure

```
LeSuccess_Project/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── env_example.txt        # Environment variables template
│   └── serviceAccountKey.json # Firebase service account key (you need to add this)
├── static/
│   ├── assets/
│   ├── css/
│   ├── icons/
│   ├── images/
│   ├── js/
│   └── videos/
└── templates/
    ├── index.html
    ├── chat.html
    ├── about.html
    ├── courses.html
    ├── blog.html
    └── contact.html
```

## Setup Instructions

### 1. Install Python Dependencies

Navigate to the backend folder and install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Authentication and Firestore Database
3. Generate a service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file as `serviceAccountKey.json` in the `backend/` folder

### 3. Google Gemini API Setup

1. Get a Gemini API key from https://makersuite.google.com/app/apikey
2. Create a `.env` file in the `backend/` folder:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### 4. Firebase Configuration

Update the Firebase configuration in `templates/chat.html`:

```javascript
const firebaseConfig = {
    apiKey: "your-api-key-here",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};
```

### 5. Update Gemini Model Name

In `backend/app.py`, replace `YOUR_FINE_TUNED_MODEL_NAME_HERE` with your actual fine-tuned Gemini model name.

### 6. Run the Application

```bash
cd backend
python app.py
```

The application will be available at `http://127.0.0.1:5001`

## Features

### Static Pages
- **Home Page** (`/`) - Landing page with hero section and features
- **About** (`/about`) - Information about the academy
- **Courses** (`/courses`) - Available courses and programs
- **Blog** (`/blog`) - Latest articles and updates
- **Contact** (`/contact`) - Contact information and form

### Dynamic Chat Interface
- **AI Tutor Chat** (`/chat`) - Real-time AI chat functionality
- Firebase Authentication integration
- Google Gemini AI integration
- Conversation history stored in Firestore

## API Endpoints

### POST /api/chat
Handles AI chat requests with the following requirements:

**Headers:**
- `Authorization: Bearer <firebase_jwt_token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
    "message": "User's message",
    "conversationId": "unique_conversation_id"
}
```

**Response:**
```json
{
    "reply": "AI's response"
}
```

## Technology Stack

- **Backend:** Python Flask
- **Database:** Google Firebase (Firestore)
- **Authentication:** Firebase Authentication
- **AI Model:** Google Gemini API
- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Real-time Communication:** Fetch API with JWT authentication

## Security Features

- JWT token verification for API requests
- Firebase Authentication integration
- CORS enabled for cross-origin requests
- Secure API endpoints with proper error handling

## Development Notes

- The application uses Flask's `url_for` syntax for all internal links
- Static assets are served from the `static/` folder
- Templates are rendered from the `templates/` folder
- All navigation menus include links to the AI Tutor chat interface
- The chat interface includes proper error handling and user feedback

## Troubleshooting

1. **Firebase Authentication Issues:** Ensure your Firebase project has Authentication enabled and the service account key is properly configured.

2. **Gemini API Errors:** Verify your API key is correct and the model name is properly set.

3. **CORS Issues:** The Flask-CORS extension is configured to handle cross-origin requests.

4. **Template Rendering:** Ensure all HTML files use Flask's `url_for` syntax for internal links.

## Production Deployment

For production deployment, consider:

1. Using environment variables for all sensitive configuration
2. Setting up proper logging and monitoring
3. Implementing rate limiting for API endpoints
4. Using a production WSGI server like Gunicorn
5. Setting up proper SSL/TLS certificates
6. Configuring Firebase security rules for Firestore
