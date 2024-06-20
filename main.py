import csv
from pymongo import MongoClient

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
        for row in reader:
            key = row[key_column_index]
            data_dict[key] = {headers[i]: row[i] for i in range(len(headers))}
    
    return data_dict

def create_tmp_csv():
    # Code to create a temp CSV
    # Define the header and data
    header = ['book_id', 'authors', 'title', 'average_rating', 'image_url']
    data = [
        [1, 'Suzanne Collins', 'The Hunger Games (The Hunger Games, #1)', 4.34, 'https://images.gr-assets.com/books/1447303603m/2767052.jpg'],
        [2, 'J.K. Rowling, Mary GrandPré', "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)", 4.44, 'https://images.gr-assets.com/books/1474154022m/3.jpg'],
        [3, 'Stephenie Meyer', 'Twilight (Twilight, #1)', 3.57, 'https://images.gr-assets.com/books/1361039443m/41865.jpg'],
        [4, 'Harper Lee', 'To Kill a Mockingbird', 4.25, 'https://images.gr-assets.com/books/1361975680m/2657.jpg']
    ]

    # Specify the file name
    filename = 'asset/books_temp.csv'

    # Write data to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8')  as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        writer.writerows(data)   # Write the data

    print(f"CSV file '{filename}' created successfully.")

def encode_to_xml(json_data):
    #write here
    return ""

def insert_records(collection):
    file_path = 'asset/books.csv'
    # create_tmp_csv()
    data = read_csv_to_dict(file_path)
    data_list = list(data.values())
    result = collection.insert_many(data_list)
    print("Records inserted successfully : ", result)

if __name__ == '__main__':
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)
    db = client['BookFinder']
    collection = db['Books']

    insert_records(collection)


    # Example operation: Find a document
    # found_document = collection.find({"title": "1984"})
    # print("Found document:", found_document)

