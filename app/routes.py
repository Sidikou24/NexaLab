from flask import render_template, redirect, url_for, flash
from app import app, db, mail
from app.forms import ContactForm
from app.models import Contact
from flask_mail import Message
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the .env file")

# Configurer la bibliothèque Generative AI pour utiliser la clé API
genai.configure(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Créer et sauvegarder les informations de contact dans la base de données
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()

        # Envoi de l'email
        try:
            msg = Message(
                subject=f"[Contact Form] {form.subject.data}",
                sender=form.email.data,
                recipients=['sidikoudari@gmail.com']  # Utiliser l'adresse mail souhaitée
            )
            msg.body = (
                f"Nom: {form.name.data}\n"
                f"Email: {form.email.data}\n"
                f"Téléphone: {form.phone.data}\n"
                f"Sujet: {form.subject.data}\n"
                f"Message: {form.message.data}"
            )
            mail.send(msg)
            #flash('Votre message a été envoyé avec succès!', 'success')
        except Exception as e:
            #flash('Une erreur est survenue lors de l\'envoi de votre message. Veuillez réessayer.', 'danger')
            print(f"Erreur lors de l'envoi de l'email : {e}")

        # Redirection après envoi du formulaire
        return redirect(url_for('services'))  

    return render_template('contact.html', form=form)



# Create a GenerativeModel instance
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize SQLite database
conn = sqlite3.connect('app.db')
c = conn.cursor()

# Create a table for storing conversations if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS conversations 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_message TEXT, bot_response TEXT)''')
conn.commit()

def save_conversation(user_message, bot_response):
    c.execute('INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)', 
              (user_message, bot_response))
    conn.commit()

def get_response(user_message):
    # Context for NexaCorp assistant
    context = (
        "You are an AI assistant working at Nexa Corporation (nexaCorp), a startup specializing in "
        "data, digital transformation, and technological innovation. NexaCorp offers a full range "
        "of services to help organizations thrive in the digital world. You only respond to questions "
        "related to IT and Nexa. Please answer accordingly."
        "Conversation will be in frech"
    )
    
    # Add the context to the user's message
    prompt = f"{context}\n\nUser: {user_message}\nAssistant:"
    
    # Generate response using Gemini model
    response = model.generate_content(prompt)
    
    # Save conversation in SQLite
    save_conversation(user_message, response.text)
    
    return response.text

if __name__ == '__main__':
    # Simple interaction loop for testing
    while True:
        user_message = input("You: ")
        if user_message.lower() in ['exit', 'quit']:
            break
        bot_response = get_response(user_message)
        print(f"Bot: {bot_response}")
