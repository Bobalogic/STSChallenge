import openai
import sqlite3

openai.api_key = "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"

table1 = "sensors"
table2 = "sensor_values"
columns1 = ["id", "name", "type", "office", "building", "room", "units"]
columns2 = ["sensor", "timestamp", "value"]
noResults = ["No results found"]


def getQuery(text):
    prompt = """You are a language model that can generate SQL queries. \
                Please provide a natural language input text, \
                and I will generate the corresponding SQL query query for you, \
                Which will be compatible with SQLite. \
                The table names are {} and {} and the corresponding \ columns are {} and {}. \nInput: {}\nSQL Query:""".format(
        table1, table2, columns1, columns2, text
    )
    # Get the sql query of the prompt
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301", messages=[{"role": "user", "content": prompt}]
    )
    sql_query = request["choices"][0]["message"]["content"]

    try:
        # Connect to database
        conn = sqlite3.connect("IoTroopers.db", check_same_thread=False)
        cursor = conn.cursor()

        print(sql_query)
        # Verify if it's a SELECT query
        if sql_query[:6].lower() == "select":
            cursor.execute(sql_query)
            result = cursor.fetchall()
            # Check if there are any results
            if not result:
                result = noResults
        # If it's not a SELECT query, no results
        else:
            result = noResults

    except sqlite3.Error as e:
        result = noResults
    finally:
        cursor.close()
        conn.close()

    if result != noResults:
        print(result)
        secondPrompt = """I queried a database with this prompt: '{}' and the answear was: '{}'. 
                    Present the information better, in a more straightforward and readable way. Only the phrase""".format(text, result)
        # Get the sql query of the prompt
        request = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0301",
            messages = [{"role": "user", "content": secondPrompt}]
        )
        result = request["choices"][0]["message"]["content"]

    return result


'''
# TEST
'''
results = getQuery("select all offices")

print(results)
