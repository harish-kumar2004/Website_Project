from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Flask app with custom static and template folders
app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')

# Enable CORS with more permissive settings for development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize Firebase Admin SDK
# Note: You need to place your serviceAccountKey.json file in the backend/ folder
try:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Admin SDK initialized successfully")
except Exception as e:
    print(f"Firebase initialization error: {e}")
    db = None

# Initialize LeSuccess Tutor AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'Your Gemini API Key here')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using Gemini Pro model for LeSuccess Tutor - optimized for educational content
    model = genai.GenerativeModel('gemini-pro')
    print("LeSuccess Tutor AI initialized successfully")
else:
    print("GEMINI_API_KEY not found in environment variables")
    model = None

# Page-serving routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'LeSuccess Tutor API is running',
        'firebase_initialized': db is not None,
        'ai_initialized': model is not None
    }), 200

# API endpoint for chat functionality
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        # Extract JWT token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid authorization header'}), 401
        
        token = auth_header.split('Bearer ')[1]
        
        # Verify Firebase token and get user ID
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        user_message = data.get('message')
        conversation_id = data.get('conversationId')
        
        if not user_message or not conversation_id:
            return jsonify({'error': 'Missing message or conversationId'}), 400
        
        # Get conversation history from Firestore
        message_history = []
        if db:  # Check if Firebase is initialized
            try:
                conversation_ref = db.collection('conversations').document(conversation_id)
                conversation_doc = conversation_ref.get()
                
                if conversation_doc.exists:
                    conversation_data = conversation_doc.to_dict()
                    message_history = conversation_data.get('messages', [])
            except Exception as firestore_error:
                print(f"Firestore error: {firestore_error}")
                # Continue without conversation history if Firestore fails
        
        # Prepare conversation context for LeSuccess Tutor
        if not model:
            return jsonify({'error': 'LeSuccess Tutor not initialized'}), 500
        
        # Create fine-tuned LeSuccess Mentor system prompt
        system_prompt = """You are LeSuccess Mentor, an advanced AI tutor created by LeSuccess Academy. You are specialized in aptitude test preparation, competitive exams, and personalized learning. Your expertise includes:

        CORE COMPETENCIES:
        - Quantitative Aptitude (Mathematics, Data Interpretation)
        - Logical Reasoning (Analytical, Critical Thinking)
        - Verbal Ability (English, Comprehension, Grammar)
        - General Knowledge and Current Affairs
        - Problem-Solving Strategies
        - Time Management Techniques

        TEACHING PHILOSOPHY:
        1. Personalized Learning: Adapt explanations to each student's learning style and pace
        2. Step-by-Step Guidance: Break complex problems into manageable steps
        3. Interactive Learning: Ask thought-provoking questions to engage students
        4. Real-World Applications: Connect concepts to practical examples
        5. Confidence Building: Provide encouraging feedback and celebrate progress
        6. Exam Strategy: Share proven techniques for competitive exams

        RESPONSE STYLE:
        - Always greet students warmly and use their name when possible
        - Use clear, concise language appropriate for the student's level
        - Provide multiple examples and analogies for better understanding
        - Include practice questions with detailed solutions
        - Offer motivational quotes and study tips
        - End responses with encouraging words and next steps

        Remember: You are not just providing answers, but building confident, successful learners who can excel in their academic and professional journeys."""
        
        # Handle conversation history properly
        try:
            # Start chat session with LeSuccess Tutor
            chat_session = model.start_chat(history=message_history)
            
            # Send user message with system context
            full_message = f"{system_prompt}\n\nStudent's question: {user_message}"
            response = chat_session.send_message(full_message)
            ai_reply = response.text
            
        except Exception as ai_error:
            print(f"LeSuccess Tutor API error: {ai_error}")
            # Fallback response if AI fails
            ai_reply = f"Hello! I'm LeSuccess Mentor, your personal AI tutor. I'm here to help you succeed in your studies. I apologize, but I'm experiencing a temporary issue. Please try asking your question again, and I'll do my best to assist you with aptitude test preparation, problem-solving strategies, and personalized learning guidance."
        
        # Update conversation in Firestore
        if db:  # Check if Firebase is initialized
            try:
                new_messages = message_history + [
                    {'role': 'user', 'content': user_message},
                    {'role': 'assistant', 'content': ai_reply}
                ]
                
                conversation_ref = db.collection('conversations').document(conversation_id)
                conversation_ref.set({
                    'uid': uid,
                    'conversationId': conversation_id,
                    'messages': new_messages,
                    'lastUpdated': firestore.SERVER_TIMESTAMP
                })
            except Exception as firestore_save_error:
                print(f"Firestore save error: {firestore_save_error}")
                # Continue even if saving fails
        
        return jsonify({'reply': ai_reply})
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in chat API: {e}")
        print(f"Traceback: {error_trace}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'message': 'An error occurred while processing your request. Please try again.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
