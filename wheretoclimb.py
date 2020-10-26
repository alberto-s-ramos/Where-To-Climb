from app import app, db
from app.models import User, Post, Thread
import logging

#print("hi there")

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Thread':Thread}