from openai import OpenAI
import json 
from dotenv import load_dotenv
import os
load_dotenv()

def rectify_statement(schema, recorded_statement):
    client = OpenAI(api_key=os.environ["API_KEY"])

    # Prepare the prompt for OpenAI ChatGPT
    prompt = (
        f"""
        Generate an SQL query for this Schema in { os.getenv('DB_TYPE')} Database to fetch data such that we can create bar or pie chart using the data
        """
        f"{schema} "
        "Now, rectify and enhance the following statement based on the schema: "
        f"'{recorded_statement}' "
        "Use the rectified and enhanced statement and convert it to an SQL query."
        "Only Return the SQL query and do not return an extra letter, no extra ` at the beginning or the end and remove the work sql from beginning"
    )

    print('Prompt: ', prompt)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in databases and language processing.."},
                {"role": "user", "content": prompt}
            ]
        )
        # Parse the response
        rectified_statement = completion.choices[0].message.content
        return rectified_statement
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
