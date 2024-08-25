# Pristine Water Analysis

## Overview

Pristine Water Analysis is a web application designed to provide real-time water quality analysis using machine learning. Users can upload images of their water samples, which are processed and analyzed to determine the quality of the water. The application provides immediate feedback on whether the water is clean or contaminated.

## Features

- **User Authentication:** Sign up and log in to manage your uploads.
- **Image Upload:** Upload water sample images for analysis.
- **Real-Time Analysis:** Get instant results on water quality.
- **Alerts:** Display user notifications and error messages.

## Technologies Used

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Machine Learning:** OpenCV, NumPy
- **Database:** MySQL
- **Environment:** Python

## Setup

### Prerequisites

- Python 3.x
- MySQL Server
- Flask
- Required Python packages


## Usage

1. **Homepage**: Access the main page to upload water sample images and view results.
2. **Login/Signup**: Use the login and signup forms to manage user authentication.
3. **Upload**: Upload images of water samples to get analysis results.

## Code Structure

- **`main.py`**: Main Flask application file.
- **`models.py`**: Contains the `Model` class for image processing and prediction.
- **`templates/`**: Contains HTML templates for rendering the frontend.
- **`static/`**: Contains static files such as CSS, JavaScript, and images.

## Contributing

Contributions are welcome! Please submit a pull request with any improvements or bug fixes.

