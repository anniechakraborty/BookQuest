import psycopg2
from psycopg2 import sql
import pandas as pd
import time

# Function to connect to the PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="bookfinder",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Function to insert data into the table
def insert_data_from_csv(csv_file_path, table_name):
    conn = connect_db()
    if conn is None:
        return
    cur = conn.cursor()
    query = 'SELECT * FROM books;'
    cur.execute(query)
    rows = cur.fetchall()
    if len(rows) == 0:
        try:
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)
            columns = ', '.join(df.columns)
            values_placeholders = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholders})"
            # Insert each row
            for row in df.itertuples(index=False, name=None):
                list_row = list(row)
                if pd.isna(list_row[3]):
                    list_row[3] = 2000
                cur.execute(insert_query, list_row)

            # Commit the transaction
            conn.commit()
            print("Data inserted successfully.")

        except Exception as e:
            print("Error inserting data:", e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        cur.close()
        conn.close()

# Updating the fields of the table
def execute_sql_commands(command):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(command)
        result = cur.fetchall()
        conn.commit()
        print(f"THE FOLLOWING COMMAND HAS BEEN EXEXCUTED SUCCESSFULLY! \n{command}")
        return result
    except Exception as e:
        print(f"ERROR EXECUTING THE COMMAND {command} : \n{e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()



# Main function to run the operations
if __name__ == "__main__":
    # Creating the table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Books (
        book_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        authors VARCHAR(255) NOT NULL,
        publication_year INTEGER,
        average_rating NUMERIC(10, 2),
        image_url VARCHAR(255)
    );
    '''
    start_time = time.time()
    # execute_sql_commands(create_table_query)
    end_time = time.time()
    execution_time = end_time - start_time
    # print("Table creation execution time : ", execution_time)

    # Update the datatypes of the columns
    update_query = "ALTER TABLE books ALTER COLUMN title TYPE TEXT;"
    # execute_sql_commands(update_query)
    update_query = "ALTER TABLE books ALTER COLUMN authors TYPE TEXT;"
    # execute_sql_commands(update_query)

    # Insert data
    file_path = 'asset/books.csv'
    insert_data_from_csv(file_path, 'books')

    # Creating a column of type tsvector to implemnet full text search
    # execute_sql_commands("ALTER TABLE books ADD COLUMN search_vector tsvector")
    update_command = '''
    UPDATE books
    SET search_vector = 
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(authors, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(average_rating::text, '')), 'C') ||
    setweight(to_tsvector('english', coalesce(publication_year::text, '')), 'D');
    '''
    start_time = time.time()
    # execute_sql_commands(update_command)
    end_time = time.time()
    execution_time = end_time - start_time
    # print("Execution time : ", execution_time)

    user_search = input("Enter your search term: ")
    search_query = f'''
    SELECT * FROM books
    WHERE search_vector @@ to_tsquery('english', '{user_search}');
    '''
    start_time = time.time()
    result = execute_sql_commands(search_query)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Records returned :", len(result))
    if len(result) > 0:
        for row in result:
            print(row)
    print("Execution time for the search operation : ", execution_time)