# Flask Blog API

This is a simple RESTful API built with Flask for managing blog posts.

## Features
- **List Posts**: Retrieve all posts, with optional sorting by `title` or `content` (ascending or descending).
- **Add Post**: Add a new blog post with `title` and `content`. A unique ID is automatically generated.
- **Update Post**: Update an existing post by ID. Supports partial updates (title/content).
- **Delete Post**: Delete a post by ID.
- **Search Posts**: Search posts by title and/or content.

## Endpoints

### List Posts
`GET /api/posts`
- Optional query parameters: `sort`, `direction`

### Add Post
`POST /api/posts`
```json
{
  "title": "New Post",
  "content": "This is the content of the new post."
}
```

### Update Post
`PUT /api/posts/<id>`
```json
{
  "title": "Updated Title",
  "content": "Updated Content"
}
```

### Delete Post
`DELETE /api/posts/<id>`

### Search Posts
`GET /api/posts/search?title=keyword&content=keyword`

## Error Handling
- `400 Bad Request`: Invalid input or parameters
- `404 Not Found`: Post or route does not exist
- `405 Method Not Allowed`: Invalid method for the given route

## Installation

1. Clone this repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python backend_app.py
   ```

---

✅ Created by Kristina Krauberger
