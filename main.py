import csv
import json
import traceback
import dicttoxml
import webbrowser
import time
import os
from xml.dom.minidom import parseString
from pymongo import MongoClient
from bson import json_util
# from flask import *
# from flask_cors import CORS
import lxml.etree as ET

# app = Flask(__name__)
# CORS(app)

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client['BookFinder']
collection = db['Books']

# search_query = ""

# API Calls and connections
# @app.route('/search', methods=['GET'])
# def get_user_query():
    # try:
    #     search_query = request.args.get('query')

    #     if search_query:
    #         results = collection.find({"$text": {"$search": search_query}})
    #         response = cursor_to_dict(results)

    #         encode_to_xml(response)

    #         return jsonify({
    #             "data": response, 
    #             "message": "QUERY RESPONSE RECEIVED SUCCESSFULLY!", 
    #             "success": True
    #         }), 200
    #     else:
    #         return jsonify(
    #                 {
    #                     "data": [],
    #                     "message": "MISSING SEARCH PARAMS!",
    #                     "success": False,
    #                 }
    #             ), 400
    # except Exception as e:
    #     exception_details("get_user_query", e)

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
                # Skipping row if book_id, title or authors is missing
                # In case of null values in publication_year and average_ratings, use default value of 2000 and 3 respectively.
                if(row[0] == '' or row[0] == None or row[1] == '' or row[1] == None or row[2] == '' or row[2] == None):
                    continue
                elif(row[3] == '' or row[3] == None):
                    row[3] = str(2000)
                elif(row[4] == '' or row[4] == None):
                    row[4] = str(3)
                elif(row[5] == None):
                    row[5] = ''
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

def encode_to_xml(data):
    xml_data = dicttoxml.dicttoxml(data, custom_root='Books', attr_type=False)
    dom = parseString(xml_data)
    pretty_xml = dom.toprettyxml(encoding='utf-8')

    # Output the XML to a file or print it
    output_file = "outputs/output.xml"
    with open(output_file, "wb") as file:  # Open file in binary mode for writing XML with encoding
        file.write(pretty_xml)

    print("Data has been converted from JSON to XML and saved to ", output_file)

def xslt_transform():

    # Paths to the XML and XSLT files
    xml_file = 'outputs/output.xml'
    xslt_file = 'transform.xslt'
    output_file = 'outputs/transformed_output.html'

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
    # Opening the output file in browser
    abs_path = os.path.abspath(output_file)
    webbrowser.open('file://' + abs_path)

def validate_xml_with_dtd():
    xml_file = 'outputs/output.xml'
    dtd_file = 'books.dtd'
    # Parse the XML file
    try:
        with open(xml_file, 'rb') as f:
            xml_content = f.read()
        xml_doc = ET.XML(xml_content)
    except (ET.XMLSyntaxError, FileNotFoundError) as e:
        exception_details("validate_xml_with_dtd", e)
        return

    # Parse the DTD file
    try:
        dtd = ET.DTD(dtd_file)
    except FileNotFoundError as e:
        exception_details("validate_xml_with_dtd", e)
        return

    # Validate the XML against the DTD
    if dtd.validate(xml_doc):
        print("The XML file is valid!")
    else:
        print("The XML file is invalid!")
        print(dtd.error_log.filter_from_errors())

def cursor_to_dict(cursor):
        """
        Purpose:
            Converts a cursor to python dictionary. When we execute a  query, MongoDB doesn't immediately return the data.
            Instead it returns a cursor which is a pointer to the result set of the query,
            and can be used to iterate over the results one by one or in batches.
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
        Purpose:
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
    num_records = collection.count_documents({})
    # print("Records count : ", num_records)
    if(num_records == 0):
        insert_records()
        # Creating an index for Full Text Search
        collection.create_index([
            ('title', 'text'),
            ('authors', 'text'),
            ('average_rating', 'text'),
            ('publication_year', 'text')
        ], name='text_index')
    
    # Take user input for search here 
    search_query = input("Enter your search term: ")
    
    # print("Search Query : ", search_query)
    start_time = time.time()
    results = collection.find(
        { "$text": { "$search": search_query } },
        { "score": { "$meta": "textScore" } }
    ).sort(
        [("score", { "$meta": "textScore" })]
    )

    end_time = time.time()
    print("Execution time: " + str(end_time - start_time))
    print()
    print("Full Text Search analysis : ", results.explain())
    # An equivalent regex query to compare execution time and analyse query results
    regex_query = {
        "$or": [
            {"title": {"$regex": search_query, "$options": "i"}},
            {"authors": {"$regex": search_query, "$options": "i"}},
            {"rating": {"$regex": search_query, "$options": "i"}},
            {"year": {"$regex": search_query, "$options": "i"}}
        ]
    }

    start_time = time.time()
    regex_results = collection.find(regex_query)
    end_time = time.time()
    print("Execution time: " + str(end_time - start_time))
    print("\n\nRegex Search analysis : ", regex_results.explain())

    # convert data to dict and call encode to xml () here
    response = cursor_to_dict(results)
    print()
    # print("response : ", response)
    encode_to_xml(response)

    # Validate the generated XML file using DTD
    validate_xml_with_dtd()

    # Convert the XML to XSLT and display on web page
    xslt_transform()

    # app.run(debug=True)

    read_csv_to_dict('asset/books.csv')

