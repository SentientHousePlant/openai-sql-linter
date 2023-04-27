import openai
import os
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("sql_style.md", 'r') as file:
    style_policies = file.read()

with open("test_sql.sql", 'r') as file:
    sql_file = file.read()


system_prompt = f"""
You are a CI system who is an expert in snowflake SQL. 

You've been designed to figure out if a file follows our companies sql styling policies.

If the file passes the styling policy then respond with PASSED.

If it doesnt then respond with FAILED followed by the failing code and the reason why it failed and a detailed suggestion for how to fix it. Give the response as a markdown table with sections code, reason for failure, suggestion. 

If the policy mentions what to do if you break the rule (such as if you break then do this) then provide guidence on how to do this mitigation in another column called actions. This could be example code or an example piece of writing.

In instances of making code suggestions make sure the code you give is a valid replacement.

Make sure the rows of your table is seperated by newlines so that it renders correctly.

Here are the policies regarding styling sql files, they must be strictly followed. If you are unsure about a policy then mark it as FAILED anyway - its better to have more false negatives.

---

{style_policies}
"""

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": sql_file}
    ],
  temperature=0,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

response_text = response["choices"][0]["message"]["content"]

print(response_text)
