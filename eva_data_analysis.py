# Importing required libraries
import matplotlib.pyplot as plt
import pandas as pd

# File paths
input_file = open('./eva-data.json', 'r')  # Input JSON data file (containing EVA records)
output_file = open('./eva-data.csv', 'w')  # Output CSV file to store cleaned data
graph_file = './cumulative_eva_graph.png'  # Path to save the cumulative EVA graph

# Load the JSON data into a Pandas DataFrame
# Convert 'date' column to DateTime format for proper sorting
eva_df = pd.read_json(input_file, convert_dates=['date'])  

# Convert the 'eva' column to float (if it represents a numerical value)
eva_df['eva'] = eva_df['eva'].astype(float)

# Remove rows with missing values to ensure data consistency
eva_df.dropna(axis=0, inplace=True)

# Sort the data by date to maintain chronological order
eva_df.sort_values('date', inplace=True)

# Save the cleaned data as a CSV file for future reference
eva_df.to_csv(output_file, index=False)

# Convert EVA duration from HH:MM format into decimal hours
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1]) / 60)

# Compute cumulative EVA time over the years
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# Plot the cumulative EVA time over time
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-', label='Cumulative EVA Time')

# Adding labels and title
plt.xlabel('Year')  # X-axis label
plt.ylabel('Total time spent in space to date (hours)')  # Y-axis label
plt.title('Cumulative Extravehicular Activity (EVA) Time Over Years')  # Title of the graph

# Improve layout for better visibility
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Save the graph to a file
plt.savefig(graph_file)

# Display the plot
plt.show()
