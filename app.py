from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
dbname = config('DB_NAME')
dbuser = config('DB_USER')
dbpass = config('DB_PASS')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{dbuser}:{dbpass}@localhost/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Article model 
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Type of article (e.g., 'recipe', 'blog', etc.)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    images = db.relationship('Image', backref='article', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    
    articles = db.relationship('Article', secondary='issue_article', lazy='subquery',
                            backref=db.backref('issues', lazy=True))

issue_article = db.Table('issue_article',
    db.Column('issue_id', db.Integer, db.ForeignKey('issue.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

def create_tables_and_sample_data():
    with app.app_context():
        db.create_all()
        
        # Create sample issues
        sample_issues = [
            Issue(title="Issue 1", publication_date="2022-01-01"),
            Issue(title="Issue 2", publication_date="2022-02-01"),
            Issue(title="Issue 3", publication_date="2022-03-01"),
            Issue(title="Issue 4", publication_date="2022-04-01"),
            Issue(title="Issue 5", publication_date="2022-05-01")
        ]
        db.session.bulk_save_objects(sample_issues)
        
        db.session.flush()  # Ensure issues are assigned IDs
        
        # Create sample articles and link them to issues
        sample_articles = [
            Article(title="Recipe 1", content="Content for recipe 1", type="recipe"),
            Article(title="Blog Post 1", content="Content for blog post 1", type="blog"),
            Article(title="News Article 1", content="Content for news article 1", type="news"),
            Article(title="Recipe 2", content="Content for recipe 2", type="recipe"),
            Article(title="Blog Post 2", content="Content for blog post 2", type="blog"),
            Article(title="News Article 2", content="Content for news article 2", type="news"),
            Article(title="Recipe 3", content="Content for recipe 3", type="recipe"),
            Article(title="Blog Post 3", content="Content for blog post 3", type="blog"),
            Article(title="News Article 3", content="Content for news article 3", type="news"),
            Article(title="Recipe 4", content="Content for recipe 4", type="recipe"),
            Article(title="Blog Post 4", content="Content for blog post 4", type="blog"),
            Article(title="News Article 4", content="Content for news article 4", type="news"),
            Article(title="Recipe 5", content="Content for recipe 5", type="recipe"),
            Article(title="Blog Post 5", content="Content for blog post 5", type="blog"),
            Article(title="News Article 5", content="Content for news article 5", type="news"),
        ]
        db.session.bulk_save_objects(sample_articles)
        db.session.flush()  # Ensure the articles are assigned IDs
        
        # Add images to some articles
        sample_images = [
            Image(article_id=1, url="http://example.com/image1.jpg", description="Image 1 description"),
            Image(article_id=2, url="http://example.com/image2.jpg", description="Image 2 description"),
            Image(article_id=3, url="http://example.com/image3.jpg", description="Image 3 description"),
            Image(article_id=4, url="http://example.com/image4.jpg", description="Image 4 description"),
            Image(article_id=5, url="http://example.com/image5.jpg", description="Image 5 description"),
        ]
        db.session.bulk_save_objects(sample_images)
        
        # Associate articles with issues
        sample_issue_article_mappings = [
            {'issue_id': 1, 'article_id': 1},
            {'issue_id': 1, 'article_id': 2},
            {'issue_id': 2, 'article_id': 3},
            {'issue_id': 2, 'article_id': 4},
            {'issue_id': 3, 'article_id': 5},
            {'issue_id': 3, 'article_id': 6},
            {'issue_id': 4, 'article_id': 7},
            {'issue_id': 4, 'article_id': 8},
            {'issue_id': 5, 'article_id': 9},
            {'issue_id': 5, 'article_id': 10},
        ]
        for mapping in sample_issue_article_mappings:
            db.session.execute(issue_article.insert().values(**mapping))
        
        db.session.commit()

# create_tables_and_sample_data()

@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit-article', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        new_article = Article(
            title=request.form['title'],
            content=request.form['content'],
            type=request.form['type']
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('submit.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)