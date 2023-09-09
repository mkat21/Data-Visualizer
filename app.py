from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a GUI
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set a folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a folder for storing analysis plots
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def generate_plot(file, x_column, y_column):
    try:
        data = pd.read_csv(file)
        # Debug print statements
        print("Data read successfully from CSV file.")
        print(data.head())  # Print the first few rows of data

        # Perform time series analysis here if needed
        # Example: Plot the time series data
        plt.figure(figsize=(12, 6))
        plt.plot(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title('Time Series Data Visualization')
        plot_path = f'{app.config["STATIC_FOLDER"]}/plot.png'
        plt.savefig(plot_path)
        plt.close()
        # Debug print statement
        print(f"Image saved as {plot_path}")
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        # Debug print statement
        print(f"Error: {str(e)}")

# Define a route for uploading time series data
@app.route('/', methods=['GET', 'POST'])
def upload_timeseries():
    if request.method == 'POST':
        file = request.files['file']
        x_column = request.form['x_column']
        y_column = request.form['y_column']
        if file and file.filename.endswith('.csv'):
            generate_plot(file, x_column, y_column)
            return redirect('/visualize')
        else:
            flash('Please upload a valid CSV file.', 'error')
    return render_template('index.html')

# Define a route for visualizing the time series data
@app.route('/visualize')
def visualize_timeseries():
    plot_path = f'{app.config["STATIC_FOLDER"]}/plot.png'
    return render_template('visualize.html', plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
