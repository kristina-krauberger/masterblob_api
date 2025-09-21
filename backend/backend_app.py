from os import remove

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {'id': 1, 'title': 'First post', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Second post', 'content': 'This is the second post.'},
]


def validate_post_data(new_post):
    """
    Validate a new blog post. Checks whether both 'title' and 'content' fields exist in the post dictionary.
    :param new_post: dict, new post entry to validate
    :return: bool, True if valid, False otherwise
    """
    if 'title' not in new_post or 'content' not in new_post:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    Handles blog post operations & supports two HTTP methods:
        - GET: Return a list of all existing posts.
        - POST: Add a new post if 'title' and 'content' are provided. A unique ID will be generated automatically.
    :return: JSON response containing posts or an error message with appropriate HTTP status codes (200, 201, or 400).
    """
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({'error': 'Invalid post data'}), 400

        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        POSTS.append(new_post)
        return jsonify(new_post), 201

    else:
        return jsonify(POSTS), 200


def find_post_by_id(post_id):
    """
    Find a blog post by its unique ID.
    :param post_id: int, the ID of the post to search for
    :return: dict if the post exists, None otherwise
    """
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post by ID.
    :param post_id: int, the ID of the post to update
    :return: JSON response with the updated post and HTTP 200 if successful,
             or JSON error message with HTTP 404 if the post does not exist
    """
    post = find_post_by_id(post_id)
    new_post = request.get_json()

    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    else:
        post['title'] = new_post.get('title', post['title'])
        post['content'] = new_post.get('content', post['content'])
        return jsonify(post), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its unique ID.
    :param post_id: int, the ID of the post to delete
    :return: JSON response with a success message and HTTP 200 if deleted,
             or JSON error message with HTTP 404 if the post does not exist
    """
    post = find_post_by_id(post_id)

    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    else:
        POSTS.remove(post)
        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200


@app.errorhandler(404)
def not_found_error(_):
    """
    Handle 404 Not Found errors. Triggered when a requested resource or route does not exist.
    :return: JSON response with error message and HTTP status 404
    """
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(405)
def method_not_allowed_error(_):
    """
    Handle 405 Method Not Allowed errors. Triggered when a valid route is accessed with an unsupported HTTP method.
    :return: JSON response with error message and HTTP status 405
    """
    return jsonify({'error': 'Method Not Allowed'}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
