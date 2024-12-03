import numpy as np
import pandas as pd

# Define the array of voltage levels
voltage_levels = [5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0]  # Example voltage levels

# Number of samples for each voltage level
num_samples = 3000

# Create an empty DataFrame to store the samples
data = pd.DataFrame()

# Generate samples for each voltage level
for voltage in voltage_levels:
    samples = np.full((num_samples,), voltage)  # Generate 3000 identical values
    data = pd.concat([data, pd.DataFrame({"Voltage Level": [voltage] * num_samples, "Sample": samples})], ignore_index=True)

# Save the DataFrame to an Excel file
output_file = "voltage_samples.xlsx"
data.to_excel(output_file, index=False)

print(f"Voltage samples saved to {output_file}")  # Confirmation for saving excel
