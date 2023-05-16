import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, request

app = Flask(__name__)
def analyze_weather_data(url):
    # Perform weather data analysis using the URL
    response = requests.get(url)
    text_data = response.text

    # Split the text into lines and remove the first 6 lines
    lines = text_data.split('\n')[7:]
    lines = [item.replace("*", "").replace("#", "") for item in lines if "Provisional" not in item]
    header = 'Year  Month   tmax    tmin    af  rain    sun'
    lines.insert(0, header)
    converted_list = [','.join(item.split()) for item in lines]
    # Join the remaining lines back into a single string
    new_text_data = '\n'.join(converted_list)

    # Write the new text data to a file
    with open('new_data.csv', 'w') as file:
        file.write(new_text_data)

    # Rename Months
    month_mapping = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
        }
    
    # Parse the data using Pandas
    data = pd.read_csv('new_data.csv', na_values='---')

    # Calculate monthly averages
    monthly_averages = data.groupby(['Month']).agg({'tmax': 'mean', 'tmin': 'mean', 'rain': 'mean', 'sun': 'mean'}).rename(index=month_mapping)

    print(monthly_averages)
    
    # Create a figure and axes
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    
    # Plot the monthly averages
    sns.lineplot(data=monthly_averages, x=monthly_averages.index, y='tmax', label='Max Temperature')
    sns.lineplot(data=monthly_averages, x=monthly_averages.index, y='tmin', label='Min Temperature')
    
    # Set the chart title and axis labels
    ax1.set_title('Monthly Averages: Temperature')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Value(Degree Celcius)')

     # Convert the plot to a canvas
    canvas1 = FigureCanvas(fig1)
    buf1 = io.BytesIO()
    canvas1.print_png(buf1)

    # convert the PNG data to a data URL
    data1 = base64.b64encode(buf1.getvalue()).decode("utf-8")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=monthly_averages, x=monthly_averages.index, y='rain', label='Precipitation')
     # Set the chart title and axis labels
    ax2.set_title('Monthly Averages: Rain')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Value(mm)')

     # Convert the plot to a canvas
    canvas2 = FigureCanvas(fig2)
    buf2 = io.BytesIO()
    canvas2.print_png(buf2)

    # convert the PNG data to a data URL
    data2 = base64.b64encode(buf2.getvalue()).decode("utf-8")

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=monthly_averages, x=monthly_averages.index, y='sun', label='Hrs of Sunlight')
     # Set the chart title and axis labels
    ax3.set_title('Monthly Averages: Sunlight')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Value(hours)')

     # Convert the plot to a canvas
    canvas3 = FigureCanvas(fig3)
    buf3 = io.BytesIO()
    canvas3.print_png(buf3)

    # convert the PNG data to a data URL
    data3 = base64.b64encode(buf3.getvalue()).decode("utf-8")
    data_url1 = f"data:image/png;base64,{data1}"
    data_url2 = f"data:image/png;base64,{data2}"
    data_url3 = f"data:image/png;base64,{data3}"

    return data_url1,data_url2, data_url3

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_station = request.form['station']
        url = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/'+selected_station+'data.txt'
        image_url1, image_url2, image_url3 = analyze_weather_data(url)
        return render_template('index.html', selected_station=selected_station, image_url1 = image_url1, image_url2 = image_url2, image_url3 = image_url3)
    else:
        return render_template('index.html', selected_station=None)

if __name__ == '__main__':
    app.run(debug=True)
