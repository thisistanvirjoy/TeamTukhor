import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime

# Load your tree canopy data from two CSV files
data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')

# Merge the two datasets based on a common key (e.g., 'timestamp')
merged_data = pd.merge(data1, data2, on='timestamp', how='inner')

# Ensure the 'timestamp' column is correctly parsed as datetime
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'])

# Prepare your features and target variable
X = merged_data[['feature1_x', 'feature2_x', 'feature1_y', 'feature2_y']]  # Use appropriate feature columns
y = merged_data['target_column_x']  # Replace with your target variable

# Create and train a linear regression model
model = LinearRegression()
model.fit(X, y)

# ...

# Define the current date and calculate the date 5 years from now
current_date = datetime.datetime.now()
future_date = current_date + datetime.timedelta(days=5*365)  # Assuming 365 days per year

# Create a DataFrame for the future prediction
future_data = pd.DataFrame({'timestamp': [future_date]})

# Replace 'feature1_x', 'feature2_x', 'feature1_y', 'feature2_y' with your actual feature names
future_data['feature1_x'] = 220 # Your feature values for tree canopy data 1
future_data['feature2_x'] = 180# Your feature values for tree canopy data 1
future_data['feature1_y'] = 180 # Your feature values for tree canopy data 2
future_data['feature2_y'] =  160# Your feature values for tree canopy data 2

# Use the trained model to make predictions for the future
future_prediction = model.predict(future_data[['feature1_x', 'feature2_x', 'feature1_y', 'feature2_y']])

# Display the predicted result
print("Predicted tree canopy after 5 years:", future_prediction[0])
