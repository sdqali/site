---
title: Looking up Enum types and values in Postgres
date: 2019-05-09T17:10:23-07:00
ghissueid: 143
bbissueid: 136
tags:
- postgres
- sql
---

In this blog post, we will explore how Postgres stores Enum types and how to query for Enum types and their values. Postgres' Enum, like their counterparts in many programming languags are data types that allow only a predefined set of values to be assigned to them. An interesting difference is that compared to programming languages, Postgres does allow blanks within the values of Enums.

<!--more-->

Postgres Enums are created using the `CREATE TYPE` statement. The values are ordered in the order in which they are specified in the `CREATE` statement.

```sql
=> CREATE TYPE weather AS ENUM (
  'sunny', 'rainy', 'cloudy', 'snow'
  );

CREATE TYPE

```

Postgres stores Enums in the `pg_type` catalog. This catalog assigns a `typcategory` to every type and Enums [have category](https://www.postgresql.org/docs/current/catalog-pg-type.html#CATALOG-TYPCATEGORY-TABLE) `E`.

```sql
=> SELECT
  *
  FROM pg_type
  WHERE typcategory = 'E';

-[ RECORD 1 ]--+----------
typname        | weather
typnamespace   | 2200
typowner       | 24576
typlen         | 4
typbyval       | t
typtype        | e
typcategory    | E
typispreferred | f
typisdefined   | t
typdelim       | ,
typrelid       | 0
typelem        | 0
typarray       | 41019
typinput       | enum_in
typoutput      | enum_out
typreceive     | enum_recv
typsend        | enum_send
typmodin       | -
typmodout      | -
typanalyze     | -
typalign       | i
typstorage     | p
typnotnull     | f
typbasetype    | 0
typtypmod      | -1
typndims       | 0
typcollation   | 0
typdefaultbin  |
typdefault     |
typacl         |

```

This shows us that the name of the enum is `weather`. How do we find the possible values of this Enum? Values are stored in the catalog `pg_enum`.

```sql
=> SELECT
  *
  FROM pg_enum;

 enumtypid | enumsortorder | enumlabel
-----------+---------------+-----------
     41020 |             1 | sunny
     41020 |             2 | rainy
     41020 |             3 | cloudy
     41020 |             4 | snow
(4 rows)
```

It is worth noting that each of the enum values are in separate rows of the catalog, with each row using the same `enumtypid`. The `enumtypid` is referring to the `oid` of the enum entry in `pg_type` catalog. We can verify that we are indeed looking at the same type. [^1]

```sql
=> SELECT
  *
FROM pg_type
WHERE oid = 41020;

-[ RECORD 1 ]--+----------
typname        | weather
typnamespace   | 2200
typowner       | 24576
typlen         | 4
typbyval       | t
typtype        | e
typcategory    | E
typispreferred | f
typisdefined   | t
typdelim       | ,
typrelid       | 0
typelem        | 0
typarray       | 41019
typinput       | enum_in
typoutput      | enum_out
typreceive     | enum_recv
typsend        | enum_send
typmodin       | -
typmodout      | -
typanalyze     | -
typalign       | i
typstorage     | p
typnotnull     | f
typbasetype    | 0
typtypmod      | -1
typndims       | 0
typcollation   | 0
typdefaultbin  |
typdefault     |
typacl         |
```

We can use the information we have so far to perform a `JOIN` on these catalogs to get all Enum types. To test that values and types are fetched correctly, lets create another enum.

```sql
=> CREATE TYPE transport AS ENUM (
  'bus', 'tram', 'rail', 'ferry'
);

CREATE TYPE
```

This enum will create more entries in `pg_enum`.

```sql
=> SELECT
  *
FROM pg_enum;

 enumtypid | enumsortorder | enumlabel
-----------+---------------+-----------
     41020 |             1 | sunny
     41020 |             2 | rainy
     41020 |             3 | cloudy
     41020 |             4 | snow
     41030 |             1 | bus
     41030 |             2 | tram
     41030 |             3 | rail
     41030 |             4 | ferry
(8 rows)
```

We can now perform the `JOIN`

```sql
=> SELECT
  type.typname,
  enum.enumlabel AS value
FROM pg_enum AS enum
JOIN pg_type AS type
  ON (type.oid = enum.enumtypid)
GROUP BY enum.enumlabel,
         type.typname;

  typname  | value
-----------+--------
 weather   | cloudy
 transport | ferry
 transport | bus
 transport | tram
 transport | rail
 weather   | rainy
 weather   | sunny
 weather   | snow
(8 rows)

```

This query needs a `GROUP BY` due to the fact that there are multiple rows representing a single Enum's values.

This result gives us everything we want in most cases. But sometimes we want to get a single row with an Enum and all it's values. This can be accomplished by the use of Postgres' [`string_agg`](https://www.postgresql.org/docs/9.0/functions-aggregate.html) function.

```sql
=> SELECT
  type.typname AS name,
  string_agg(enum.enumlabel, '|') AS value
FROM pg_enum AS enum
JOIN pg_type AS type
  ON (type.oid = enum.enumtypid)
GROUP BY type.typname;

   name    |          value
-----------+-------------------------
 transport | bus|tram|rail|ferry
 weather   | sunny|rainy|cloudy|snow
(2 rows)
```

Our choice of `|` as the separator is arbitrary, but it is important to remember that Postgres does allow blanks in Enum values and using blank as the separator will lead to unexpected and wrong results. [^2]

[^1]: Postgres does not display values of `oid` columns of catalogs by default. It has to be explicitly queried for.
[^2]: Being bit hard by this issue is how I learned about this.
