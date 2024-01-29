from flask import Flask, render_template, request, redirect, url_for, abort
import os

app = Flask(__name__)

# Define the path to the 'posts' directory
POSTS_DIR = 'posts'

# Function to list all blog posts
def list_posts():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(POSTS_DIR, filename), 'r') as file:
                title = file.readline().strip()
                content = file.read()
                posts.append({'title': title, 'content': content, 'filename': filename})
    return posts

# Route for the home page
@app.route('/')
def home():
    posts = list_posts()
    return render_template('home.html', posts=posts)

# Route for creating a new post
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Sanitize the title for file name
        title = title.replace('/', '-').replace('\\', '-').replace(':', '-')
        
        try:
            # Save the post as a text file in the 'posts' directory
            with open(os.path.join(POSTS_DIR, f'{title}.txt'), 'w') as file:
                file.write(title + '\n')
                file.write(content)
            return redirect(url_for('home'))
        except Exception as e:
            # Print the error for debugging
            print(f"Error creating post: {e}")
            # You can add more error handling here if needed
            return "Error creating post. Please try again later."

    return render_template('create_post.html')

# Route for viewing a specific blog post
@app.route('/post/<string:filename>')
def view_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.isfile(filepath):
        abort(404)  # Return a 404 error if the post does not exist
    with open(filepath, 'r') as file:
        title = file.readline().strip()
        content = file.read()
    return render_template('post.html', title=title, content=content)

if __name__ == '__main__':
    app.run(debug=True)
