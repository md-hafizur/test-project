# Project Setup

This document provides instructions on how to set up and run this project locally.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Git

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**

    -   **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

    -   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create and apply database migrations:**

    Since migration files are not tracked in Git, you'll need to create them first.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The application will be accessible at `http://127.0.0.1:8000/`.
