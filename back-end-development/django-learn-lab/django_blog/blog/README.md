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

# Django Blog - Tagging and Search Features

## Overview

This document provides a guide on how to use the tagging and search features in ythe Django Blog project. These features allow users to tag blog posts for easier organization and enable searching through posts based on tags, titles, or content.

## Features

1. **Tagging System**
   - Add tags to blog posts.
   - View posts by clicking on tags.
   - Link multiple tags to a single post.
   
2. **Search Functionality**
   - Search for blog posts by title, content, or tags.
   - View posts that match search criteria on a dedicated search results page.

---

## How to Use the Tagging System

### 1. Adding Tags to Posts
When creating or editing a post, you'll see a **Tags** section where you can select multiple tags for your post:

- **Steps**:
  1. Go to the "Create Post" or "Edit Post" page.
  2. In the **Tags** field, select one or more tags from the list or type new tags that don't exist yet.
  3. Submit the form, and your post will be saved with the associated tags.

### 2. Viewing Posts by Tag
Once a post has tags, the tags will be displayed on the post detail page. Clicking on a tag will take you to a page that shows all posts associated with that tag.

- **Steps**:
  1. Go to a post's detail page.
  2. Find the list of tags under the post content.
  3. Click on any tag to view all posts that share the same tag.

---

## How to Use the Search Functionality

### 1. Searching for Posts
The search feature allows you to search for blog posts based on their title, content, or associated tags.

- **Steps**:
  1. In the site's navigation bar or sidebar, you'll find a search bar.
  2. Enter keywords related to the title, content, or tags of the posts you're looking for.
  3. Submit the search query.
  4. The search results page will display a list of posts matching the keywords.

---

## URL Patterns

### 1. Viewing Posts by Tag
You can access posts by tag via the URL pattern `/tags/<tag_name>/`. 

### 2. Searching for Posts
The search feature can be accessed via the `/search/` URL. 

---

## Testing Guidelines

1. **Tagging System**:
   - Create a post and assign one or more tags.
   - Edit a post to change its tags.
   - Ensure tags appear on the post's detail page and are clickable.
   - Verify that clicking a tag shows all associated posts.

2. **Search Functionality**:
   - Perform searches using different keywords (titles, content, tags).
   - Check that the search results page displays accurate results based on your query.
   - Verify that search results link to the correct posts.

---

## Conclusion

The tagging and search features enhance the usability of the blog by allowing content to be easily categorized and retrieved. Make sure to test these features thoroughly to ensure a seamless user experience.
