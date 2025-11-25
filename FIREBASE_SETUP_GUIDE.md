# Firebase Setup Guide for LeSuccess Academy

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `harishproject-b43d4` (or your preferred name)
4. Enable Google Analytics (optional but recommended)
5. Click "Create project"

## Step 2: Enable Authentication

1. In your Firebase project, go to "Authentication" in the left sidebar
2. Click "Get started"
3. Go to "Sign-in method" tab
4. Enable "Email/Password" authentication
5. Optionally enable "Google" sign-in for better user experience

## Step 3: Create Firestore Database

1. Go to "Firestore Database" in the left sidebar
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location close to your users
5. Click "Done"

## Step 4: Get Firebase Configuration

1. Go to "Project settings" (gear icon)
2. Scroll down to "Your apps" section
3. Click "Web app" icon (</>)
4. Register your app with a nickname: `lesuccess-web`
5. Copy the Firebase configuration object

## Step 5: Create Service Account Key

1. Go to "Project settings" → "Service accounts" tab
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `serviceAccountKey.json`
5. Place it in your `backend/` folder

## Step 6: Update Configuration Files

### Update .env file (create in project root):
```env

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Update chat.html Firebase config:
✅ **COMPLETED** - Your Firebase configuration has been updated in `templates/chat.html` with the correct values:

## Step 7: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 8: Test the Setup

1. Start your Flask backend:
```bash
cd backend
python app.py
```

2. Open your browser and go to `http://127.0.0.1:5001/chat`
3. Try signing in with a test email/password
4. Test the AI chat functionality

## Security Rules for Firestore

Add these rules to your Firestore database for security:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own conversations
    match /conversations/{conversationId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.uid;
    }
    
    // Users can only access their own profile data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Troubleshooting

### Common Issues:

1. **Firebase initialization error**: Make sure `serviceAccountKey.json` is in the `backend/` folder
2. **Authentication errors**: Check that Email/Password is enabled in Firebase Auth
3. **CORS errors**: Ensure Flask-CORS is properly configured
4. **API key errors**: Verify your Gemini API key is correct

### Testing Authentication:

You can test user creation in Firebase Console:
1. Go to Authentication → Users
2. Click "Add user"
3. Enter email and password
4. Use these credentials to test login

## Next Steps

1. Set up user registration/login UI
2. Add user profile management
3. Implement conversation history
4. Add file upload for study materials
5. Set up push notifications for study reminders
