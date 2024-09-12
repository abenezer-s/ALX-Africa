## Authentication System Documentation

### Overview

- **Registration**: Users can register with a username and email.
- **Login**: Users can log in using their credentials.
- **Logout**: Users can log out securely.
- **Profile Management**: Users can view and update their profile information.

### Testing Instructions

1. **Registration**:
   - Navigate to `/register`.
   - Fill out the form and submit.
   - Verify the user is redirected to the profile page.

2. **Login**:
   - Navigate to `/login`.
   - Enter credentials and submit.
   - Verify the user is logged in and redirected appropriately.

3. **Logout**:
   - Navigate to `/logout`.
   - Verify the user is logged out and redirected.

4. **Profile Update**:
   - Navigate to `/profile`.
   - Update profile information and submit.
   - Verify changes are saved and displayed.

## Blog Post Management Documentation

### Overview

- **List Posts**: Displays all blog posts with titles and brief snippets.
- **View Post**: Shows the full content of a single post.
- **Create Post**: Allows authenticated users to create new posts.
- **Edit Post**: Allows post authors to edit their posts.
- **Delete Post**: Allows post authors to delete their posts.

### Usage Instructions

1. **List Posts**:
   - URL: `/`
   - Accessible to all users.

2. **View Post**:
   - URL: `/posts/<int:pk>/`
   - Accessible to all users.

3. **Create Post**:
   - URL: `/posts/new/`
   - Only accessible to authenticated users.

4. **Edit Post**:
   - URL: `/posts/<int:pk>/edit/`
   - Only accessible to the post author.

5. **Delete Post**:
   - URL: `/posts/<int:pk>/delete/`
   - Only accessible to the post author.

### Testing Instructions

1. **List Posts**:
   - Navigate to `/`.
   - Verify all posts are listed with titles and snippets.

2. **View Post**:
   - Navigate to `/posts/<int:pk>/`.
   - Verify the full content of the post is displayed.

3. **Create Post**:
   - Navigate to `/posts/new/` (authenticated users only).
   - Fill out the form and submit.
   - Verify the new post appears in the list.

4. **Edit Post**:
   - Navigate to `/posts/<int:pk>/edit/` (post author only).
   - Update the form and submit.
   - Verify the changes are saved and displayed.

5. **Delete Post**:
   - Navigate to `/posts/<int:pk>/delete/` (post author only).
   - Confirm deletion.
   - Verify the post is removed from the list.

