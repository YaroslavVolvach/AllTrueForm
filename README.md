AllTrueForm

AllTrueForm is a project for managing support requests, built with a modern technology stack. It includes a backend written in Python using FastAPI and a React-based frontend.

Instructions for Running

To set up and run the project, follow these steps: 1. Clone the repository and navigate to the project directory:
git clone git@github.com:YaroslavVolvach/AllTrueForm.git
cd alltrueform 2. Create a .env file in the root directory of the project with the following content:
DATABASE_URL=postgresql://user:password@localhost:5432/alltrueform
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
Replace user, password, and localhost:5432/alltrueform with your actual database credentials. 3. Run the following command:
make init
This command will:

    •	Build the Docker containers for the frontend and backend.
    •	Apply the database migrations automatically.
    •	Create a default admin user.

    4.	Access the application in your browser:

    •	Frontend: http://localhost
    •	Backend API: http://localhost:8000

About the Project

AllTrueForm is designed to streamline the process of submitting and managing support requests. It allows users to:
• Register and manage their accounts.
• Submit detailed support requests with issue descriptions and reproduction steps.
• View, sort, and manage support requests efficiently.

Technologies Used

This project uses the following technologies:
• Backend: Python, FastAPI, PostgreSQL, Alembic for database migrations.
• Frontend: React, Redux, Axios for HTTP requests, and React Router for routing.
• Docker: For containerization and easy deployment.
