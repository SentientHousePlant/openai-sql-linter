import openai
import os
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
import sys

console = Console()

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("sql_style.md", 'r') as file:
    style_policies = file.read()

with open("test_sql.sql", 'r') as file:
    sql_file = file.read()

prompt = f"""
You are a CI system designed to figure out if a file follows our companies sql styling policies.

If the file passes the styling policy then respond with PASSED.

If it doesnt then respond with FAILED followed by the failing line numbers and the reason why it failed and a detailed suggestion for how to fix it. Give the response as markdown with sections line number, reason for failure, suggestion. 
Make sure the table is valid markdown by using newlines.

Make sure the rows of your table is seperated by newlines so that it renders correctly.

Here are some policies regarding styling sql files, they must be strictly followed.

{style_policies}

And here is the content of a file:

{sql_file}
"""

print(prompt)

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0,
  max_tokens=150,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

response_text = response.choices[0].text

print(response_text)

console.print(Markdown(response_text))