import requests
import pandas as pd
import matplotlib.pyplot as plt

# URLs for API
imbalance_url = "https://api-baltic.transparency-dashboard.eu/api/v1/export?id=imbalance_volumes&start_date=2024-08-01T00:00:00&end_date=2024-09-01T00:00:00&output_time_zone=CET&output_format=json&json_header_groups=0"
activations_url = "https://api-baltic.transparency-dashboard.eu/api/v1/export?id=normal_activations_total&start_date=2024-08-01T00:00:00&end_date=2024-09-01T00:00:00&output_time_zone=CET&output_format=json&json_header_groups=0"


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def process_data(imbalance_data, activations_data):
    imbalance_df = pd.DataFrame(imbalance_data["data"]["timeseries"])
    activations_df = pd.DataFrame(activations_data["data"]["timeseries"])

    # Convert to datetime
    imbalance_df["timestamp"] = pd.to_datetime(imbalance_df["from"])
    activations_df["timestamp"] = pd.to_datetime(activations_df["from"])

    # Extract data
    imbalance_df["imbalance"] = imbalance_df["values"].apply(lambda x: x[0])
    activations_df["upward"] = activations_df["values"].apply(lambda x: x[0])
    activations_df["downward"] = activations_df["values"].apply(lambda x: x[1])

    # Merge dataframes
    merged_df = pd.merge(
        imbalance_df[["timestamp", "imbalance"]],
        activations_df[["timestamp", "upward", "downward"]],
        on="timestamp",
    )

    return merged_df


def create_graph(data):
    plt.figure(figsize=(15, 10))
    plt.plot(data["timestamp"], data["imbalance"], label="Imbalance")
    plt.plot(data["timestamp"], data["upward"], label="Upward Adjustment")
    plt.plot(
        data["timestamp"], -data["downward"], label="Downward Adjustment"
    )  # Negate downward adjustments

    plt.title("Baltic Imbalance and Adjustments")
    plt.xlabel("Time")
    plt.ylabel("Volume (MWh)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("baltic_regulation.png")
    plt.close()


def analyze_regulation(data):
    correct_actions = 0
    total_actions = len(data)

    for _, row in data.iterrows():
        imbalance = row["imbalance"]
        upward = row["upward"]
        downward = row["downward"]

        if (imbalance > 0 and downward > 0) or (imbalance < 0 < upward):
            correct_actions += 1

    correctness_percentage = (correct_actions / total_actions) * 100
    return correctness_percentage


def main():
    # Fetch data
    imbalance_data = fetch_data(imbalance_url)
    activations_data = fetch_data(activations_url)

    # Process data
    merged_data = process_data(imbalance_data, activations_data)

    # Create graph
    create_graph(merged_data)
    print("Graph has been saved as 'baltic_regulation.png'")

    # Analyze regulation
    correctness = analyze_regulation(merged_data)
    print(f"Regulation actions were correct {correctness:.2f}% of the time.")

    # Print some statistics
    print("\nData Statistics:")
    print(merged_data.describe())


if __name__ == "__main__":
    main()
