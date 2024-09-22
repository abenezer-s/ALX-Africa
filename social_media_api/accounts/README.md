# Custom User Model with Token-Based Authentication in Django

This Django project uses a custom user model and token-based authentication to manage user accounts and secure access to resources. The custom model extends the default Django `AbstractUser` model, adding fields such as a biography (`bio`), profile picture (`profile_picture`), and a self-referencing `followers` field to allow users to follow each other.

---

## Custom User Model

The project defines a custom user model, `CustomUser`, which extends Django’s built-in `AbstractUser`. This allows for additional flexibility in the user profile, while retaining the core fields (`username`, `password`, `email`, etc.) provided by Django.

### Model Fields

- **`bio`**: A `TextField` that allows users to add a short description about themselves. It is optional and can be left blank.
  
- **`profile_picture`**: An `ImageField` where users can upload their profile picture. The images are stored in the directory specified in `upload_to='profile_pictures/'`. This field is optional.

- **`followers`**: A self-referencing `ManyToManyField` with `symmetrical=False`, which allows users to follow other users without requiring the follow to be mutual. This field creates a relationship between users and is stored in the database without enforcing a reciprocal relationship.

# Post and Comment API Documentation

## Overview

This project implements a basic API where users can create, read, update, and delete posts and comments. The API includes models for `Post` and `Comment`, serialization logic, CRUD views, and additional enhancements like pagination and filtering.

## Step-by-Step Breakdown

### 1. Post and Comment Models

Two models, `Post` and `Comment`, were created in a new app called `posts`.

- **Post Model**: Represents a blog post with fields like:
  - `author`: ForeignKey to the `User` model.
  - `title`: Title of the post.
  - `content`: Body of the post.
  - `created_at`: Timestamp when the post was created.
  - `updated_at`: Timestamp when the post was last updated.

- **Comment Model**: Represents comments on posts with fields like:
  - `post`: ForeignKey to the `Post` model.
  - `author`: ForeignKey to the `User` model.
  - `content`: Body of the comment.
  - `created_at`: Timestamp when the comment was created.
  - `updated_at`: Timestamp when the comment was last updated.

```python

# Follow and Feed Features

## Overview

This update adds functionality for user follow relationships and a personalized content feed. Users can follow or unfollow others, and view a feed that displays posts from the users they follow.

### 1. Follow Management Endpoints

#### Follow a User
- **URL**: `/follow/<int:user_id>/`
- **Method**: `POST`
- **Description**: Allows a user to follow another user.
- **Permissions**: Authenticated users only.

**Example Request**:
```bash
POST /follow/3/
Headers: Authorization: Token <user_token>

POST /unfollow/3/
Headers: Authorization: Token <user_token>

# Social Media API Documentation

## Features:
- Like and Unlike posts
- Notification system for interactions (likes, comments, new followers, etc.)

---

## API Endpoints

### **1. Like and Unlike Posts**

#### **Like a Post**
- **Endpoint:** `POST /posts/<int:pk>/like/`
- **Description:** Allows an authenticated user to like a post.
- **Request:**
    ```json
    {
      "Authorization": "Bearer <token>"
    }
    ```
- **Response:**
    - `201 Created`: The post has been liked.
    - `400 Bad Request`: User has already liked the post.
    ```json
    {
      "message": "You have already liked this post."
    }
    ```

#### **Unlike a Post**
- **Endpoint:** `POST /posts/<int:pk>/unlike/`
- **Description:** Allows an authenticated user to unlike a post.
- **Request:**
    ```json
    {
      "Authorization": "Bearer <token>"
    }
    ```
- **Response:**
    - `200 OK`: The post has been unliked.
    - `404 Not Found`: User hasn't liked the post before.
    ```json
    {
      "message": "You haven't liked this post."
    }
    ```

---

### **2. Notifications**

#### **Get Notifications**
- **Endpoint:** `GET /notifications/`
- **Description:** Retrieves the unread notifications for the authenticated user.
- **Request:**
    ```json
    {
      "Authorization": "Bearer <token>"
    }
    ```
- **Response:**
    - `200 OK`: Returns a list of unread notifications.
    ```json
    [
      {
        "id": 1,
        "actor": "user123",
        "verb": "liked your post",
        "target": "Post #12",
        "timestamp": "2024-09-22T12:34:56",
        "is_read": false
      }
    ]
    ```

#### **Mark Notification as Read**
- **Endpoint:** `POST /notifications/<int:notification_id>/read/`
- **Description:** Marks the specified notification as read.
- **Request:**
    ```json
    {
      "Authorization": "Bearer <token>"
    }
    ```
- **Response:**
    - `200 OK`: Notification marked as read.
    ```json
    {
      "message": "Notification marked as read."
    }
    ```

---