from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name must be present")
        elif Author.query.filter(Author.name == name).first():
            raise ValueError('Name already in use')
        
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) < 10 or len(phone_number) > 10:
            raise ValueError("Phone number less")
        

    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait):
            raise ValueError("No clickbait found")
        return title
    
    @validates('content', "summary")
    def validate_content_summary(self, key, str):
        if(key == "content"):
            if len(str) <= 250:
                 raise ValueError("Content too short")
        
        if(key == "summary"):
            if len(str) >= 250:
                 raise ValueError("Post summary must be less than or equal to 250 characters long.")
        
        return str
        
    # @validates("content")
    # def validate_content(self, key, content):
    #     if len(content) < 250:
    #         raise ValueError("Content too short")
        
    # @validates("summary")
    # def validate_summary(self, key, summary):
    #     if len(summary) >= 250:
    #         raise ValueError("Summary too long test. More than 250 chars.")
        
    @validates("category")
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be fiction of non-fiction")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
