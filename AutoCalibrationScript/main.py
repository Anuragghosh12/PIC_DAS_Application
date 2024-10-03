import pandas as pd
from time import gmtime, strftime
import numpy as np

def main():
    curr_time = str(strftime('%Y%m%d', gmtime()))

    # Each voltage level should contribute to the total of 2400 samples
    samples_per_level = 3000  # Adjusted to contribute to 2400 total samples

    # Create voltage levels
    voltage_levels = (
        np.full(samples_per_level, -0.5).tolist() +
        np.full(samples_per_level, -0.3).tolist() +  # -300 mV
        np.full(samples_per_level, -0.2).tolist() +  # -200 mV
        np.full(samples_per_level, -0.1).tolist() +  # -100 mV
        np.full(samples_per_level, -0.05).tolist() + # -50 mV
        np.full(samples_per_level, -0.02).tolist() + # -20 mV
        np.full(samples_per_level, -0.01).tolist() + # -10 mV
        np.full(samples_per_level, -0.005).tolist() +# -5 mV
        np.full(samples_per_level, -0.002).tolist() +  # -5 mV
        np.full(samples_per_level, -0.001).tolist() +  # -5 mV
        np.full(samples_per_level, 0).tolist() +      # 0 V
        np.full(samples_per_level, 0.001).tolist() +  # -5 mV
        np.full(samples_per_level, 0.002).tolist() +  # -5 mV
        np.full(samples_per_level, 0.005).tolist() +  # 5 mV
        np.full(samples_per_level, 0.01).tolist() +   # 10 mV
        np.full(samples_per_level, 0.02).tolist() +   # 20 mV
        np.full(samples_per_level, 0.05).tolist() +   # 50 mV
        np.full(samples_per_level, 0.1).tolist() +    # 100 mV
        np.full(samples_per_level, 0.2).tolist() +    # 200 mV
        np.full(samples_per_level, 0.3).tolist() +     # 300 mV
        np.full(samples_per_level, 0.5).tolist() +

        np.full(samples_per_level, 0.3).tolist() +
        np.full(samples_per_level, 0.2).tolist() +  # -300 mV
        np.full(samples_per_level, 0.1).tolist() +  # -200 mV
        np.full(samples_per_level, 0.05).tolist() +  # -100 mV
        np.full(samples_per_level, 0.02).tolist() +  # -50 mV
        np.full(samples_per_level, 0.01).tolist() +  # -20 mV
        np.full(samples_per_level, 0.005).tolist() +  # -10 mV
        np.full(samples_per_level, 0.002).tolist() +  # -5 mV
        np.full(samples_per_level, 0.001).tolist() +  # -5 mV
        np.full(samples_per_level, 0).tolist() +  # 0 V
        np.full(samples_per_level, -0.001).tolist() +  # -5 mV
        np.full(samples_per_level, -0.002).tolist() +  # -5 mV
        np.full(samples_per_level, -0.005).tolist() +  # 5 mV
        np.full(samples_per_level, -0.01).tolist() +  # 10 mV
        np.full(samples_per_level, -0.02).tolist() +  # 20 mV
        np.full(samples_per_level, -0.05).tolist() +  # 50 mV
        np.full(samples_per_level, -0.1).tolist() +  # 100 mV
        np.full(samples_per_level, -0.2).tolist() +  # 200 mV
        np.full(samples_per_level, -0.3).tolist() +  # 300 mV
        np.full(samples_per_level, -0.5).tolist()
    )

    # Convert to a DataFrame
    df = pd.DataFrame(voltage_levels, columns=['Voltage (V)'])



    # Save the DataFrame to a CSV file
    curr_time += '_' + 'C002_' + '1' + '_P001_' + '2_data.csv'
    df.to_csv(curr_time, index=False)

if __name__ == "__main__":
    main()
