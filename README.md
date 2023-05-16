# weatherDataAnalysis
This Python code analyzes weather data retrieved from the Met Office website. It performs the following tasks:

1. Retrieves weather data from the Met Office website based on the selected weather station.
2. Processes and cleans the data.
3. Calculates monthly averages for temperature, precipitation, and sunlight.
4. Generates line charts for the monthly averages using Matplotlib and Seaborn.
5. Converts the charts to base64-encoded PNG images.
6. Displays the charts and the selected weather station on a web page using Flask.

## Installation

1. Clone or download the repository.
2. Install the required dependencies by running the following command:
    pip install requests pandas matplotlib seaborn flask
## Usage

1. Run the Flask web application by executing the following command:
  python WeatherAnalysis.py
2. Open a web browser and navigate to `http://localhost:5000`.
3. Select a weather station from the dropdown list.
4. Click the "Submit" button to analyze the weather data and display the results.
5. The web page will show line charts representing the monthly averages for temperature, precipitation, and sunlight.

## Files

- `WeatherAnalysis.py`: The main Python script that sets up the Flask application and handles the routes.
- `templates/index.html`: The HTML template file that defines the structure of the web page.
- `static/styles.css`: The CSS file that contains the styles for the web page.
- `new_data.csv`: The CSV file that stores the processed weather data.

## Credits

This code was developed by [Ajeesh Kumar A]
