import csv
import json
import traceback
import dicttoxml
from xml.dom.minidom import parseString
from pymongo import MongoClient
from bson import json_util
from flask import *
from flask_cors import CORS
import lxml.etree as ET

app = Flask(__name__)
CORS(app)

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client['BookFinder']
collection = db['Books']

search_query = ""

# API Calls and connections
@app.route('/search', methods=['GET'])
def get_user_query():
    try:
        search_query = request.args.get('query')

        if search_query:
            results = collection.find({"$text": {"$search": search_query}})
            response = cursor_to_dict(results)

            #TODO: call encode_to_xml() and pass response here
            encode_to_xml(response)

            return jsonify({
                "data": response, 
                "message": "QUERY RESPONSE RECEIVED SUCCESSFULLY!", 
                "success": True
            }), 200
        else:
            return jsonify(
                    {
                        "data": [],
                        "message": "MISSING SEARCH PARAMS!",
                        "success": False,
                    }
                ), 400
    except Exception as e:
        exception_details("get_user_query", e)

# Utility functions
def read_csv_to_dict(file_path, key_column_index=0):
    """
    Reads a CSV file and stores its contents in a dictionary.
    
    :param file_path: Path to the CSV file
    :param key_column_index: Index of the column to use as keys for the dictionary (default is 0, the first column)
    :return: Dictionary with each row grouped under a key
    """
    data_dict = {}
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the header row
            for row in reader:
                key = row[key_column_index]
                data_dict[key] = {headers[i]: row[i] for i in range(len(headers))}
        
        return data_dict
    except Exception as e:
        exception_details("read_csv_to_dict", e)

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
    xml_data = dicttoxml.dicttoxml(json_data, custom_root='Books', attr_type=False)
    dom = parseString(xml_data)
    pretty_xml = dom.toprettyxml(encoding='utf-8')

    # Output the XML to a file or print it
    output_file = "output.xml"
    with open(output_file, "wb") as file:  # Open file in binary mode for writing XML with encoding
        file.write(pretty_xml)

    print("Data has been converted from JSON to XML and saved to", output_file)
    xslt_transform()
    return ""

def xslt_transform():  

    # Paths to the XML and XSLT files
    xml_file = 'output.xml'
    xslt_file = 'transform.xslt'
    output_file = 'transformed_output.html'

    # Parse the XML and XSLT files
    xml_doc = ET.parse(xml_file)
    xslt_doc = ET.parse(xslt_file)

    # Apply the transformation
    transform = ET.XSLT(xslt_doc)
    result = transform(xml_doc)

    # Save the result to a file
    with open(output_file, 'wb') as f:
        f.write(ET.tostring(result, pretty_print=True))

    print(f"Transformed output saved to {output_file}")


def cursor_to_dict(cursor):
        """Converts a cursor to python dictionary
        Args:
            cursor (Cursor): Cursor Object
        Returns:
            dict: Python dictionary representation of input Cursor
        """

        try:
            # iterate over cursor to get a list of dicts
            cursor_dict = [doc for doc in cursor]

            # serialize to json string
            cursor_dict_string = json.dumps(cursor_dict, default=json_util.default)

            # json from json string
            cursor_dict = json.loads(cursor_dict_string)

            return cursor_dict

        except Exception as e:
            exception_details("cursor_to_dict", e)

def exception_details(function_name, exception):
        """
        The function "exception_details" prints the details of an exception, including the function
        name, exception details, and traceback information.
        
        Args:
          function_name: The name of the function where the exception occurred.
          exception: The exception parameter is the exception object that was raised during the
        execution of the function. It contains information about the type of exception and any
        additional details that may be available.
        """
        # code to handle the exception
        print("=====================================================================================")
        print("⚠️ Exception in function: ", function_name)
        print("-------------------------------------------------------------------------------------")
        print("Exception details:", exception)
        print("-------------------------------------------------------------------------------------")
        print("Traceback information:")
        traceback.print_exc()
        print("=====================================================================================")

# Database functions
def insert_records():
    """
    Reads data from specified CSV file. 
    Converts the records into dictionary form and inserts them into the database.
    """

    file_path = 'asset/books.csv'
    # create_tmp_csv()
    data = read_csv_to_dict(file_path)
    data_list = list(data.values())

    try:
        result = collection.insert_many(data_list)
        print("Records inserted successfully : ", result)
    
    except Exception as e:
        exception_details("insert_records", e)

if __name__ == '__main__':
    # insert_records()

    # Creating an index for Full Text Search
    # collection.create_index([
    #     ('title', 'text'),
    #     ('authors', 'text'),
    #     ('average_rating', 'text'),
    #     ('publication_year', 'text')
    # ], name='text_index')
    
    # print("search_query : ", search_query)
    # results = collection.find({"$text": {"$search": search_query}})

    # print("results execution : ", results.explain())

    app.run(debug=True)

