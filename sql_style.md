# dbt Style Guide

## Model File Naming and Coding

- Schema, table and column names should be in `snake_case`.

- Limit use of abbreviations that are related to domain knowledge. An onboarding
  employee will understand `current_order_status` better than `current_os`.

- Use names based on the _business_ terminology, rather than the source terminology.

- Each model should have a primary key that can identify the unique row, and should be named `<object>_id`, e.g. `account_id` – this makes it easier to know what `id` is being referenced in downstream joined models.

- If a surrogate key is created, it should be named `<object>_sk`.

- Columns should be ordered in categories, where identifiers are first and date/time fields are at the end.  

- Date/time columns should be named according to these conventions:
  - Timestamps: `<event>_at`  
    Format: UTC  
    Example: `created_at`
  
  - Dates: `<event>_date`  
    Format: Date  
    Example: `created_date`

- Booleans should be prefixed with `is_` or `has_`.  
  Example: `is_active_customer` and `has_admin_access`

- Price/revenue fields should be in decimal currency (e.g. `19.99` for $19.99; many app databases store prices as integers in cents). If non-decimal currency is used, indicate this with suffix, e.g. `price_in_cents`.

- Avoid using reserved words (such as [these](https://docs.snowflake.com/en/sql-reference/reserved-keywords.html) for Snowflake) as column names.

- Consistency is key! Use the same field names across models where possible.  
Example: a key to the `customers` table should be named `customer_id` rather than `user_id`.

## CTEs

For more information about why we use so many CTEs, check out [this glossary entry](https://docs.getdbt.com/terms/cte).

- Where performance permits, CTEs should perform a single, logical unit of work.

- CTE names should be as verbose as needed to convey what they do.

- CTEs with confusing or noteable logic should be commented with SQL comments as you would with any complex functions, and should be located above the CTE.

- CTEs fall in to two main categories:
  | Term    | Definition                                                                                                                                                             |
  |---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | Import  | Used to bring data into a model. These are kept relatively simple and refrain from complex operations such as joins and column transformations.                        |
  | Logical | Used to perform a logical step with the data that is brought into the model toward the end result. |

- All `{{ ref() }}` or `{{ source() }}` statements should be placed within import CTEs so that dependent model references are easily seen and located.

- Where applicable, opt for filtering within import CTEs over filtering within logical CTEs. This allows a developer to easily see which data contributes to the end result.

- SQL should end with a simple select statement. All other logic should be contained within CTEs to make stepping through logic easier while troubleshooting.
  Example: `select * from final`

- SQL and CTEs within a model should follow this structure:
  - `with` statement
  - Import CTEs
  - Logical CTEs
  - Simple select statement

### Example SQL with CTEs

  ``` sql
   -- Jaffle shop went international!
  with

  -- Import CTEs
  regions as (
      select * from {{ ref('stg_jaffle_shop__regions') }}
  ),

  nations as (
      select * from {{ ref('stg_jaffle_shop__nations') }}
  ),
  
  suppliers as (
      select * from {{ ref('stg_jaffle_shop__suppliers') }}
  ),
  
  -- Logical CTEs
  locations as (
      select
          {{ dbt_utils.generate_surrogate_key([
              'regions.region_id',            
              'nations.nation_id'
          ]) }} as location_sk,
          regions.region_id,
          regions.region,
          regions.region_comment,
          nations.nation_id,
          nations.nation,
          nations.nation_comment
      from regions
      left join nations
          on regions.region_id = nations.region_id
  ),
  
  final as (
      select
          suppliers.supplier_id,
          suppliers.location_id,
          locations.region_id,
          locations.nation_id,
          suppliers.supplier_name,
          suppliers.supplier_address,
          suppliers.phone_number,
          locations.region,
          locations.region_comment,
          locations.nation,
          locations.nation_comment,
          suppliers.account_balance
      from suppliers
      inner join locations
          on suppliers.location_id = locations.location_sk
  )
  
  -- Simple select statement
  select * from final
  ```

## SQL style guide

- **DO NOT OPTIMIZE FOR FEWER LINES OF CODE.**  

  New lines are cheap, brain time is expensive; new lines should be used within reason to produce code that is easily read.

- Fields should be stated before aggregates / window functions

- Aggregations should be executed as early as possible before joining to another table.

- Ordering and grouping by a number (eg. group by 1, 2) is preferred over listing the column names (see [this rant](https://blog.getdbt.com/write-better-sql-a-defense-of-group-by-1/) for why). Note that if you are grouping by more than a few columns, it may be worth revisiting your model design. If you really need to, the [dbt_utils.group_by](https://github.com/dbt-labs/dbt-utils/tree/0.8.6/macros/sql/groupby.sql) function may come in handy.

- Prefer `union all` to `union` [*](http://docs.aws.amazon.com/redshift/latest/dg/c_example_unionall_query.html)

- Avoid table aliases in join conditions (especially initialisms) – it's harder to understand what the table called "c" is compared to "customers".

## Misc

- Don't misgender people!
