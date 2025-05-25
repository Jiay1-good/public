# Personalized Diet Recommendation and Analysis

This project provides a web application for personalized diet recommendations based on user input such as height, weight, age, gender, and activity level. It calculates BMI, BMR, and TDEE, and suggests daily macronutrient intake and general dietary advice.

## Project Structure

- `server.py`: Flask backend application that handles API requests for diet recommendations.
- `recommendation.py`: Contains the core logic for calculating BMI, BMR, TDEE, and generating macronutrient and dietary recommendations.
- `requirements.txt`: Lists the Python dependencies required for the backend.
- `Web/`: Contains the frontend files.
    - `index.html`: The main HTML file for the web application.
    - `app.js`: JavaScript file for handling form submission, API calls, and displaying results.
    - `styles.css`: CSS file for styling the web application.

## Running the Project

Follow these steps to set up and run the project locally:

1.  **Clone the repository** (if applicable, otherwise navigate to the project directory).

2.  **Install Backend Dependencies**:
    Navigate to the project root directory in your terminal and install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Backend Server**:
    From the project root directory, run the Flask server:
    ```bash
    python server.py
    ```
    The server should start and listen on `http://localhost:5001`.

4.  **Run the Frontend**:
    You can serve the frontend files using a simple HTTP server. Navigate to the `Web` directory in your terminal:
    ```bash
    cd Web
    ```
    Then, start a Python HTTP server (Python 3):
    ```bash
    python3 -m http.server 8080
    ```
    This will serve the frontend files on `http://localhost:8080`.

5.  **Access the Application**:
    Open your web browser and go to `http://localhost:8080` to access the Personalized Diet Recommendation application.

6.  **Use the Application**:
    Fill in the form with your details and click "Calculate Recommendation" to get your personalized diet recommendations.

## Dependencies

The backend requires the following Python packages, listed in `requirements.txt`:

- flask
- flask-cors
- numpy
- pandas
- tensorflow
- Pillow
- matplotlib
- requests
- beautifulsoup4
- fake-useragent

The frontend uses Bootstrap 5 for styling and components.

## Notes

- Ensure both the backend (`server.py`) and frontend HTTP server are running simultaneously for the application to work correctly.
- The backend runs on port 5001, and the frontend is served on port 8080. If these ports are occupied, you may need to change them in the respective files (`server.py` and the HTTP server command) and update the API endpoint URL in `Web/app.js` accordingly.