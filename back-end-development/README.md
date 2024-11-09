# Backend Web Development

Welcome to my ALX Bootcamp Backend Web Development journey! In this repository, I will be showcasing the skills, tools, and projects I’ve worked on throughout the program, which has deepened my understanding of backend web development.

### 🚀 Skills Acquired
During the bootcamp, I learned a variety of backend technologies and concepts that have strengthened my understanding of building scalable and efficient web applications. Below is a summary of the skills I have acquired:

- **Django**: Mastered Django framework for building robust web applications with Python.
- **RESTful APIs**: Developed and consumed RESTful APIs, applying the principles of HTTP methods, status codes, and request/response structures.
- **Django REST Framework (DRF)**: Specialized in DRF to create advanced, customizable APIs with authentication, permissions, and serializers.
- **Postman**: Utilized Postman to test and debug APIs, ensuring endpoints are working as expected.
- **Version Control**: Gained experience with Git and GitHub to manage and track changes to projects.
- **Collaborative Work**: Worked alongside other developers and communicated effectively to complete tasks, share ideas, and solve problems.

### 🛠 Tools & Technologies Used
- **Django**  
- **Django REST Framework (DRF)**
- **Postman**
- **SQLite / PostgreSQL (Database)**
- **Git/GitHub (Version Control)**
- **Python (Programming Language)**

### 🧑‍💻 Capstone Project: E-Learning API
For my final project during the bootcamp, I developed an **E-Learning API** to support the backend functionality of an online learning platform. This API allows users to interact with various resources like courses, programs, and user profiles. Details of the porject can be found [here](https://github.com/abenezer-s/e_learning_api.git)
#### Features:
- **Course Management**: Users can create, update, delete, and view courses.
- **Lesson Management**: Each course can have multiple lessons with content and video links.
- **User Authentication**: Secure user login and registration, including JWT token-based authentication for protected routes.
- **Course Enrollment**: Users can enroll in courses and track their progress.
- **Admin Dashboard**: Admin users can manage users, courses, and track user activity.
- **Search Functionality**: Users can search for courses based on keywords and categories.

#### Technologies Used:
- **Django**: To build the core backend logic.
- **Django REST Framework (DRF)**: To expose the backend as a RESTful API.
- **JWT Authentication**: For secure user authentication and API access control.
- **SQLite/PostgreSQL**: As the primary database for storing course, lesson, and user data.
- **Postman**: Used extensively to test and document the API endpoints.

### 📦 Getting Started

To get started with this project locally, follow the steps below:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/elearning-api.git
    cd elearning-api
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
    ```

3. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations to set up the database:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Test the API** using Postman or your preferred tool by visiting `http://127.0.0.1:8000/api/` for the API documentation and to test various endpoints.

### 📝 API Endpoints (Example)

Here are some of the key endpoints available in the E-Learning API:

- **POST /api/auth/register/**: User registration.
- **POST /api/auth/login/**: User login and JWT token generation.
- **GET /api/courses/**: List all courses.
- **POST /api/courses/**: Create a new course (Admin).
- **GET /api/courses/{id}/**: Retrieve details of a specific course.
- **POST /api/courses/{id}/enroll/**: Enroll in a course (Authenticated users).
- **GET /api/courses/{id}/lessons/**: Get lessons for a specific course.
- **POST /api/courses/{id}/lessons/**: Add lessons to a course (Admin).

### 💬 Connect with Me
During the bootcamp, I connected with fellow students, mentors, and instructors to learn from each other and grow as a developer. I encourage you to explore the work of others and collaborate wherever possible.

If you would like to get in touch or have any questions, feel free to connect with me via:

- **GitHub**: [github.com/your-username](https://github.com/your-username)
- **LinkedIn**: [linkedin.com/in/your-username](https://linkedin.com/in/your-username)
- **Email**: your.email@example.com

---

Thank you for checking out my ALX Bootcamp Backend Web Development repository! I am excited to continue building upon these skills and contributing to meaningful projects in the future.