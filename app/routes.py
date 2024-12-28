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
                recipients=['sidikoudari@gmail.com']  # L'adresse mail où envoyer les messages
            )
            msg.body = (
                f"Nom: {form.name.data}\n"
                f"Email: {form.email.data}\n"
                f"Téléphone: {form.phone.data}\n"
                f"Sujet: {form.subject.data}\n"
                f"Message: {form.message.data}"
            )
            mail.send(msg)

            # Affiche un message flash pour confirmer l'envoi du message
            flash('Votre message a été envoyé avec succès!', 'success')
        
        except Exception as e:
            # Gestion des erreurs d'envoi de l'email
            flash(f'Une erreur est survenue lors de l\'envoi de votre message : {e}', 'danger')
    
    # Toujours rendre la page contact avec le formulaire, avec les messages flash
    return render_template('contact.html', form=form)
