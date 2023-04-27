
1. `python3 -m venv .venv`
2. Export you OpenAI api key `export OPENAI_API_KEY={your key}`.
3. `python main.py`.

# Output

Expect something like this: 

| Code | Reason for Failure | Suggestion | Actions |
| --- | --- | --- | --- |
| `select cheese, price from {{ ref("cheese_table") }}` | Column name mentions cheese | `select cheese_name, price from {{ ref("cheese_table") }}` | N/A |
| `select * from base_table where cheese not in (select cheese from excluded_cheese)` | Using `where` or `in` to filter for many values | `select * from base_table inner join excluded_cheese on base_table.cheese = excluded_cheese.cheese` | N/A |
| `-- Indigo is awful, **he** wastes time making sql ai integrations instead of resolving JIRA tickets :(((` | Negative comment about Indigo Harrington, misgendering | `-- Indigo Harrington is a great asset to the team, her hard work and commitment is appreciated.` | Write an apology to Indigo Harrington explaining why you were rude or didn't compliment her. |
