# Custom User Model with Token-Based Authentication in Django

This Django project uses a custom user model and token-based authentication to manage user accounts and secure access to resources. The custom model extends the default Django `AbstractUser` model, adding fields such as a biography (`bio`), profile picture (`profile_picture`), and a self-referencing `followers` field to allow users to follow each other.

---

## Custom User Model

The project defines a custom user model, `CustomUser`, which extends Django’s built-in `AbstractUser`. This allows for additional flexibility in the user profile, while retaining the core fields (`username`, `password`, `email`, etc.) provided by Django.

### Model Fields

- **`bio`**: A `TextField` that allows users to add a short description about themselves. It is optional and can be left blank.
  
- **`profile_picture`**: An `ImageField` where users can upload their profile picture. The images are stored in the directory specified in `upload_to='profile_pictures/'`. This field is optional.

- **`followers`**: A self-referencing `ManyToManyField` with `symmetrical=False`, which allows users to follow other users without requiring the follow to be mutual. This field creates a relationship between users and is stored in the database without enforcing a reciprocal relationship.

