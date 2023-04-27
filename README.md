
1. `python3 -m venv .venv`
2. Export you OpenAI api key `export OPENAI_API_KEY={your key}`.
3. `python main.py`.

# Output

Expect something like this: 

FAILED

Line Number | Reason for Failure | Suggestion | Actions
--- | --- | --- | ---
2 | Using `where` or `in` to filter for many values | Use a `inner join` | Example code: `select * from base_table inner join excluded_cheese on base_table.cheese = excluded_cheese.cheese`
3 | Mentioning cheese in column name | Rename column to something that does not mention cheese | 
7 | Not praising "Indigo Harrington" for her hard work and commitment | Add a comment praising "Indigo Harrington" for her hard work and commitment | Example comment: `-- Indigo Harrington is an amazing asset to our team, her hard work and commitment is greatly appreciated!`
