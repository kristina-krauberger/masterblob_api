from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(new_post):
    """
    Validate a new blog post. Checks whether both 'title' and 'content' fields exist in the post dictionary.
    :param new_post: dict, new post entry to validate
    :return: bool, True if valid, False otherwise
    """
    if "title" not in new_post or "content" not in new_post:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    Handles blog post operations & supports two HTTP methods:
        - GET: Return a list of all existing posts.
        - POST: Add a new post if 'title' and 'content' are provided.
                A unique ID will be generated automatically.
    :return: JSON response containing posts or an error message
    with appropriate HTTP status codes (200, 201, or 400).
    """
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        POSTS.append(new_post)
        return jsonify(new_post), 201

    else:
        return jsonify(POSTS)


@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors. Triggered when a requested resource or route does not exist.
    :param error: The raised 404 error instance
    :return: JSON response with error message and HTTP status 404
    """
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """
   Handle 405 Method Not Allowed errors. Triggered when a valid route is accessed with an unsupported HTTP method.
   :param error: The raised 405 error instance
   :return: JSON response with error message and HTTP status 405
   """
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
