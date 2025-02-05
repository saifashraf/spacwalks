import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    """
    Reads an EVA dataset from a JSON file into a Pandas DataFrame.

    Parameters:
    input_file (str): The file path of the JSON dataset.

    Returns:
    pd.DataFrame: A DataFrame containing the parsed and cleaned data.
    """
    print(f'Reading JSON file: {input_file}')
    try:
        df = pd.read_json(input_file, convert_dates=['date'])  # Read JSON
        df['eva'] = df['eva'].astype(float)  # Convert 'eva' column to float
        df.dropna(inplace=True)  # Remove missing values
        df.sort_values('date', inplace=True)  # Sort by date
        return df
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def write_dataframe_to_csv(df, output_file):
    """
    Saves a Pandas DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to be saved.
    output_file (str): The file path where the CSV should be stored.

    Returns:
    None
    """
    try:
        print(f'Saving to CSV file: {output_file}')
        df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"Error saving to CSV file: {e}")

# Main code execution
print("--START--")

input_file = './eva-data.json'  # JSON file path
output_file = './eva-data.csv'  # CSV output file path
graph_file = './cumulative_eva_graph.png'  # Graph output file path

# Read the data from JSON file
eva_data = read_json_to_dataframe(input_file)

if eva_data is not None:
    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    
    # Convert duration (HH:MM) to decimal hours
    eva_data['duration_hours'] = eva_data['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1]) / 60)
    
    # Compute cumulative EVA time
    eva_data['cumulative_time'] = eva_data['duration_hours'].cumsum()

    # Plot cumulative EVA time
    plt.figure(figsize=(10, 5))
    plt.plot(eva_data['date'], eva_data['cumulative_time'], 'ko-', label='Cumulative EVA Time')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.title('Cumulative Extravehicular Activity (EVA) Time Over Years')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save and display the graph
    plt.savefig(graph_file)
    plt.show()

print("--END--")
