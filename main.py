import pandas as pd

# Load the datasets
land_data = pd.read_csv('land_data.csv')
crop_suitability_data = pd.read_csv('crop_suitability_data.csv')

# Check if merged_data is empty
if land_data.empty or crop_suitability_data.empty:
    print("No valid data. Check your datasets.")
else:
    # Define a function to encode categorical variables (Soil_Type in this case)
    def encode_soil_type(soil_type):
        if soil_type == 'Sandy':
            return 0
        elif soil_type == 'Loamy':
            return 1
        elif soil_type == 'Clayey':
            return 2
        else:
            return -1  # Handle unknown categories if needed


    # Apply the encoding to the 'Soil_Type' column in land_data
    land_data['Soil_Type'] = land_data['Soil_Type'].apply(encode_soil_type)


    # Define a function to suggest a suitable crop based on land characteristics
    def suggest_crop(land_characteristics):
        suitable_crops = []

        # Iterate through crop suitability data to find suitable crops
        for index, crop_data in crop_suitability_data.iterrows():
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


    # Get user input for land characteristics
    user_temperature = float(input("Enter the land's average temperature (in Celsius): "))
    user_rainfall = float(input("Enter the land's average annual rainfall (in mm): "))
    user_soil_type = input("Enter the soil type (Sandy, Loamy, or Clayey): ").strip()
    user_soil_type = encode_soil_type(user_soil_type)

    # Create a dictionary with user-provided land characteristics
    user_land_characteristics = {
        'Temperature': user_temperature,
        'Rainfall': user_rainfall,
        'Soil_Type': user_soil_type,
    }

    # Suggest suitable crops based on user-provided land characteristics
    suggested_crops = suggest_crop(user_land_characteristics)

    if suggested_crops:
        print("Suggested Suitable Crops:")
        for crop in suggested_crops:
            print(crop)
    else:
        print("No suitable crops found for the provided land characteristics.")

# Debugging prints to check values
print("Land Characteristics:", user_land_characteristics)
print("Crop Suitability Data:")
print(crop_suitability_data)
