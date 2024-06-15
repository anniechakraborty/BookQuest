import csv

def read_csv_to_dict(file_path, key_column_index=0):
    """
    Reads a CSV file and stores its contents in a dictionary.
    
    :param file_path: Path to the CSV file
    :param key_column_index: Index of the column to use as keys for the dictionary (default is 0, the first column)
    :return: Dictionary with each row grouped under a key
    """
    data_dict = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row
        # print(headers)
        for row in reader:
            key = row[key_column_index]
            data_dict[key] = {headers[i]: row[i] for i in range(len(headers))}
    
    return data_dict

file_path = 'asset/books.csv'
data = read_csv_to_dict(file_path)
# print(data)
