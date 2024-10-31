# Book Quest 

### About
The "Book Quest" project aims to streamline and enhance the process of book discovery for users by leveraging the capabilities of popular NoSQL database **MongoDB's Full-Text Search**. It focuses on developing an efficient book searching web application. The core objective is to improve search efficiency, query complexity, and response speed, ensuring relevant results for the users.

In this project, we deep dive into the capabilities of MongoDB's Full Text Search and how it fares against popular SQL database **PostgreSQL** by comparing the effiency of query execution and the complexity of query searches supported by both.

✨ Keywords  :SQL, NoSQL, Full Text Search, query optimisation

### Pre-requisities
- Ensure that Python v3 and Pip are installed on the system. Run the following commands in the terminal to check the installed versions: <br/>
`python --version` <br/>
`pip --version` <br/>
If the commands throw an error, then please install Python by following the official documentation. Python version 3.4 and above automatically installs pip. For our project we have used the Python v3.10.5 and pip v24.0
- Add Python and Pip to the environment PATH variable. <br/>
	`C:\Users\<user name>\AppData\Local\Programs\Python\Python310\Scripts\` <br/>
  `C:\Users\<user name>\AppData\Local\Programs\Python\Python310\`
- Execute the following command to install the third party packages that need to be installed to run the program. <br/>
  `pip install dicttoxml pymongo bson lxml`
- Install Mongo Compass on your system by following the official documentation here. Add mongo to the environment variable PATH here: <br/>
  `C:\Program Files\MongoDB\Server\6.0\bin`

### Getting Started
- Initially, create a database in Mongo by launching the MongoDB Compass and connecting to the server. In our case we connect to the local server (local host) using the `mongodb://localhost:27017` connection string URI.
- Create a new database called BookFinder with a collection called Books.
- Clone / download this project and open it in the Command Prompt / Terminal of your device and run the command `py .\main.py`

### Project File Structure

| File / Folder name      | Purpose      |
| ------------- | ------------- |
| main.py | The python file that drives the whole logic of the project |
| output.xml | The XML file created by converting the query response to XML data. |
| books.dtd | The DTD grammar against which we check our generated XML file |
| newtransform.xslt | This is the XSLT stylesheet that is used to transform the XML to HTML |
| newtransformed_output.html | The HTMl file which is generated as the final output to the search query |

### Data Collection

We  sourced our dataset from Kaggle's GoodBooks-10k dataset which is composed of several CSV files, each containing specific types of information about the books and their interactions on the GoodReads platform. The primary file included in the dataset is books.csv that contains detailed metadata for each of the 10,000 books.