import pandas as pd
import datetime

# Question 9: Distance Matrix Calculation
def calculate_distance_matrix(df):
    unique_ids = pd.Index(df['id'].unique()).union(df['id_2'].unique())
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)

    for index, row in df.iterrows():
        distance_matrix.at[row['id'], row['id_2']] = row['distance']

    for id1 in distance_matrix.index:
        for id2 in distance_matrix.columns:
            if distance_matrix.at[id1, id2] == 0:
                continue
            for id3 in distance_matrix.columns:
                if distance_matrix.at[id2, id3] > 0:
                    distance_matrix.at[id1, id3] = max(distance_matrix.at[id1, id3],
                                                       distance_matrix.at[id1, id2] + distance_matrix.at[id2, id3])

    return distance_matrix

# Sample DataFrame for testing
data = {'id': ['A', 'A', 'B', 'B'],
        'id_2': ['B', 'C', 'A', 'C'],
        'distance': [10, 20, 10, 30]}
df_distances = pd.DataFrame(data)

# Calculate and print the distance matrix
distance_matrix = calculate_distance_matrix(df_distances)
print("Distance Matrix:\n", distance_matrix)

# Question 10: Unroll Distance Matrix
def unroll_distance_matrix(distance_matrix):
    unrolled_df = distance_matrix.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled_df

# Unroll and print the distance matrix
unrolled_df = unroll_distance_matrix(distance_matrix)
print("Unrolled Distance Matrix:\n", unrolled_df)

# Question 11: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id):
    reference_distance = unrolled_df[unrolled_df['id_start'] == reference_id]['distance'].mean()
    lower_bound = reference_distance * 0.9
    upper_bound = reference_distance * 1.1

    return unrolled_df[(unrolled_df['distance'] >= lower_bound) & (unrolled_df['distance'] <= upper_bound)]['id_start'].tolist()

# Test case for IDs within 10% threshold
print("IDs within 10% of A's average distance:\n", find_ids_within_ten_percentage_threshold(unrolled_df, 'A'))

# Question 12: Calculate Toll Rate
def calculate_toll_rate(unrolled_df):
    toll_rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate in toll_rates.items():
        unrolled_df[vehicle_type] = unrolled_df['distance'] * rate

    return unrolled_df

# Test case for toll rates
toll_df = calculate_toll_rate(unrolled_df)
print("Toll Rates:\n", toll_df)

# Question 13: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(toll_df, time_df):
    # Merge the toll DataFrame with the time DataFrame
    merged_df = toll_df.merge(time_df, on=['id_start', 'id_end'], how='left')

    def apply_time_discount(row):
        # Check for NaN values and handle them
        if pd.isna(row['start_time']) or pd.isna(row['end_time']):
            return row  # Skip processing if times are missing

        start_time = datetime.datetime.strptime(row['start_time'], '%H:%M:%S').time()
        end_time = datetime.datetime.strptime(row['end_time'], '%H:%M:%S').time()

        if row['start_day'] in ['Saturday', 'Sunday']:
            discount_factor = 0.7
        else:
            if start_time < datetime.time(10, 0):
                discount_factor = 0.8
            elif start_time < datetime.time(18, 0):
                discount_factor = 1.2
            else:
                discount_factor = 0.8

        for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
            row[vehicle_type] *= discount_factor

        return row

    return merged_df.apply(apply_time_discount, axis=1)

# Sample DataFrame for time-based toll rates
time_data = {
    'id_start': ['A', 'A', 'B'],
    'id_end': ['B', 'C', 'A'],
    'distance': [10, 20, 10],
    'start_day': ['Monday', 'Saturday', 'Sunday'],
    'start_time': ['09:00:00', '08:00:00', '11:00:00'],
    'end_day': ['Monday', 'Saturday', 'Sunday'],
    'end_time': ['10:00:00', '09:00:00', '12:00:00']
}

time_df = pd.DataFrame(time_data)

# Ensure all time values are string
time_df['start_time'] = time_df['start_time'].astype(str)
time_df['end_time'] = time_df['end_time'].astype(str)

# Calculate time-based toll rates
toll_df_with_time = calculate_time_based_toll_rates(toll_df, time_df)
print("Time-Based Toll Rates:\n", toll_df_with_time)

