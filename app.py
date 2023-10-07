import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the datasets
land_data = pd.read_csv('land_data.csv')
crop_suitability_data = pd.read_csv('crop_suitability_data.csv')

# Define a function to encode soil type
def encode_soil_type(soil_type):
    if soil_type == 'Sandy':
        return 0
    elif soil_type == 'Loamy':
        return 1
    elif soil_type == 'Clayey':
        return 2
    else:
        return -1

# Apply soil type encoding to the 'Soil_Type' column in land_data
land_data['Soil_Type'] = land_data['Soil_Type'].apply(encode_soil_type)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_temperature = float(request.form['temperature'])
    user_rainfall = float(request.form['rainfall'])
    user_soil_type = request.form['soil_type'].strip()
    user_soil_type = encode_soil_type(user_soil_type)

    user_land_characteristics = {
        'Temperature': user_temperature,
        'Rainfall': user_rainfall,
        'Soil_Type': user_soil_type,
    }

    def suggest_crop(land_characteristics):
        suitable_crops = []
        for _, crop_data in crop_suitability_data.iterrows():
            min_temp = crop_data['Min_Temperature']
            max_temp = crop_data['Max_Temperature']
            min_rainfall = crop_data['Min_Rainfall']
            max_rainfall = crop_data['Max_Rainfall']
            suitable_soil_types = crop_data['Soil_Type'].split(',')
            if (
                    min_temp <= land_characteristics['Temperature'] <= max_temp and
                    min_rainfall <= land_characteristics['Rainfall'] <= max_rainfall and
                    str(land_characteristics['Soil_Type']) in suitable_soil_types
            ):
                suitable_crops.append(crop_data['Crop_Name'])
        return suitable_crops

    suggested_crops = suggest_crop(user_land_characteristics)

    if suggested_crops:
        return render_template('result.html', suggested_crops=suggested_crops)
    else:
        return render_template('result.html', message="No suitable crops found.")

if __name__ == '__main__':
    app.run(debug=True)
