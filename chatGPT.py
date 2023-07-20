import openai
import sqlite3

openai.api_key = "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"

table1 = "sensors"
table2 = "sensor_values"
columns1 = ['id', 'name', 'type', 'office', 'building', 'room', 'units']
columns2 = ['sensor', 'timestamp', 'value']


def getQuery(text):

    prompt = """You are a language model that can generate SQL queries. \
                Please provide a natural language input text, \
                and I will generate the corresponding SQL query query for you, \
                Which will be compatible with SQLite. \
                The table names are {} and {} and the corresponding \ columns are {} and {}. \nInput: {}\nSQL Query:""".format(table1, table2, columns1, columns2, text)

    request = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0301",
        messages = [{"role": "user", "content": prompt}]
    )
    sql_query = request["choices"][0]["message"]["content"]

    try:
        # Verify if the sensor already exists
        conn = sqlite3.connect("IoTroopers.db", check_same_thread=False)
        cursor = conn.cursor()

        print(sql_query)
        cursor.execute(sql_query)
        result = cursor.fetchall()

    except sqlite3.Error as e:
        # Handle any potential errors that might occur during the database operation
        print("Error: ", e)

    finally:
        cursor.close()
        conn.close()

    return result

results = getQuery("What is the highest temperature in all offices in the last 20 minutes and what is the office?")

for i in results:
    print(i)