import pandas as pd
import polyline
import re
from itertools import permutations
from collections import defaultdict
from haversine import haversine, Unit

# Question 1: Reverse List by N Elements
def reverse_list_by_n(lst, n):
    result = []
    for i in range(0, len(lst), n):
        group = lst[i:i + n]
        for j in range(len(group) - 1, -1, -1):
            result.append(group[j])
    return result

# Test cases for Question 1
print(reverse_list_by_n([1, 2, 3, 4, 5, 6, 7, 8], 3))  # Output: [3, 2, 1, 6, 5, 4, 8, 7]
print(reverse_list_by_n([1, 2, 3, 4, 5], 2))  # Output: [2, 1, 4, 3, 5]
print(reverse_list_by_n([10, 20, 30, 40, 50, 60, 70], 4))  # Output: [40, 30, 20, 10, 70, 60, 50]

# Question 2: Group Strings by Length
def group_strings_by_length(strings):
    length_dict = {}
    for string in strings:
        length = len(string)
        if length not in length_dict:
            length_dict[length] = []
        length_dict[length].append(string)
    return dict(sorted(length_dict.items()))

# Test cases for Question 2
print(group_strings_by_length(["apple", "bat", "car", "elephant", "dog", "bear"]))  # Output: {3: ['bat', 'car', 'dog'], 4: ['bear'], 5: ['apple'], 8: ['elephant']}
print(group_strings_by_length(["one", "two", "three", "four"]))  # Output: {3: ['one', 'two'], 4: ['four'], 5: ['three']}

# Question 3: Flatten a Nested Dictionary
def flatten_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.update(flatten_dict(item, f"{new_key}[{i}]", sep=sep))
                else:
                    items[f"{new_key}[{i}]"] = item
        else:
            items[new_key] = v
    return items

# Test case for Question 3
nested_dict = {
    "road": {
        "name": "Highway 1",
        "length": 350,
        "sections": [
            {
                "id": 1,
                "condition": {
                    "pavement": "good",
                    "traffic": "moderate"
                }
            }
        ]
    }
}
print(flatten_dict(nested_dict))  # Output: {'road.name': 'Highway 1', 'road.length': 350, 'road.sections[0].id': 1, 'road.sections[0].condition.pavement': 'good', 'road.sections[0].condition.traffic': 'moderate'}

# Question 4: Generate Unique Permutations
def unique_permutations(lst):
    return list(set(permutations(lst)))

# Test case for Question 4
print(unique_permutations([1, 1, 2]))  # Output: [(1, 1, 2), (1, 2, 1), (2, 1, 1)]

# Question 5: Find All Dates in a Text
def find_all_dates(text):
    date_pattern = r'\b(\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{4}\.\d{2}\.\d{2})\b'
    return re.findall(date_pattern, text)

# Test case for Question 5
text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
print(find_all_dates(text))  # Output: ['23-08-1994', '08/23/1994', '1994.08.23']

# Question 6: Decode Polyline, Convert to DataFrame with Distances
def decode_polyline(polyline_str):
    coordinates = polyline.decode(polyline_str)
    df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
    df['distance'] = 0.0

    for i in range(1, len(df)):
        df.loc[i, 'distance'] = haversine(
            (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude']),
            (df.loc[i, 'latitude'], df.loc[i, 'longitude']),
            unit=Unit.METERS
        )

    return df

# Example polyline string test case
polyline_str = "m~w~(nqf@hR|IhQyDbAyLwFm@kFgA"
print(decode_polyline(polyline_str))  # Adjust with an actual polyline string

# Question 7: Matrix Rotation and Transformation
def rotate_and_transform(matrix):
    n = len(matrix)
    # Rotate the matrix by 90 degrees clockwise
    rotated = [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]

    # Create a new matrix for transformation
    transformed = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated[i]) - rotated[i][j]
            col_sum = sum(rotated[x][j] for x in range(n)) - rotated[i][j]
            transformed[i][j] = row_sum + col_sum

    return transformed

# Test case for Question 7
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(rotate_and_transform(matrix))  # Output: [[22, 19, 16], [23, 20, 17], [24, 21, 18]]

# Question 8: Time Check (placeholder function)
def check_timestamps(df):
    # Group by id and id_2
    grouped = df.groupby(['id', 'id_2'])
    results = {}

    for (id_value, id_2_value), group in grouped:
        # Convert timestamps to a datetime format
        group['start'] = pd.to_datetime(group['startDay'] + ' ' + group['startTime'])
        group['end'] = pd.to_datetime(group['endDay'] + ' ' + group['endTime'])

        # Check if the range covers 24 hours and spans all days of the week
        if (group['end'].max() - group['start'].min()).total_seconds() >= 86400:
            results[(id_value, id_2_value)] = True
        else:
            results[(id_value, id_2_value)] = False

    return pd.Series(results)


