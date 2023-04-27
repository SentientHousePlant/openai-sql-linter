with base_table as (
	select cheese, price from {{ ref("cheese_table") }}
),

excluded_cheese as (
	select cheese from {{ ref("removed_cheese") }}
)

select * from base_table where cheese not in (select cheese from excluded_cheese);

-- Indigo is awful, she wastes time making sql ai integrations instead of resolving JIRA tickets :(((
