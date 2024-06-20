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

def encode_to_xml(json_data):
    #write here
    return ""

if __name__ == '__main__':
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)
    db = client['BookFinder']
    collection = db['Books']
    document = {
        "title": "1984",
        "author": "George Orwell",
        "year_published": 1949
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    print(f"Document inserted with _id: {result.inserted_id}")

    # Example operation: Find a document
    found_document = collection.find({"title": "1984"})
    print("Found document:", found_document)

    file_path = 'asset/books.csv'
    data = read_csv_to_dict(file_path)

