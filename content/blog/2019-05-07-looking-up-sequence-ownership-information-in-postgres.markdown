---
title: Looking up Sequence ownership information in Postgres
date: 2019-05-07T18:04:42-07:00
ghcommentid: 142
bbcommentid: 135
tags:
- postgres
- sql
---
This blog post is an exercise in identifying all the `sequences` in a PostgreSQL database that is associated with a table column via an `OWNED BY` relationship. Figuring out how to do this was harder than it should have been and this journals my understanding of it.

<!--more-->

When I first started looking at this, I ended up at this Stack Overflow [answer](https://stackoverflow.com/questions/9900346/how-do-you-view-new-sequence-ownership-information-in-postgres-after-using-alter) from 2012. While that seemed to work, it is fair to say that I had no idea what it did. So, I set out to understand it and hopefully improve it.

We will start by creating a `table` that we will later associate a `sequence` with.

```sql
create table users (
  id bigint not null,
  name varchar(40) not null
);
```

Next, we will create a sequence that is not going to be owned by any columns - a freehanging sequence.

```sql
create sequence freehanging;
```

Postgres stores `sequence`s across two different catalogs - [`pg_sequence`](https://www.postgresql.org/docs/current/catalog-pg-sequence.html) and [`pg_class`](https://www.postgresql.org/docs/current/catalog-pg-class.html). Catalog `pg_sequence` contains sequence parameters like `seqstart`, `seqincrement` etc. The rest of the information gets stored in `pg_class` catalog with the `seqlrelid` column in `pg_sequence` pointing to the corresponding `pg_class` entry.

```sql
=> \x
Expanded display is on.
=> select * from pg_sequence;
-[ RECORD 1 ]+--------------------
seqrelid     | 41000
seqtypid     | 20
seqstart     | 1
seqincrement | 1
seqmax       | 9223372036854775807
seqmin       | 1
seqcache     | 1
seqcycle     | f
```

That has the information that Postgres can use, but it does not look particularly useful to a human being. Luckily, Postgres provides a `view` named [`pg_sequences`](https://www.postgresql.org/docs/10/view-pg-sequences.html) that shows us more information.

```sql
=> select * from pg_sequences;
-[ RECORD 1 ]-+--------------------
schemaname    | public
sequencename  | freehanging
sequenceowner | todo
data_type     | bigint
start_value   | 1
min_value     | 1
max_value     | 9223372036854775807
increment_by  | 1
cycle         | f
cache_size    | 1
last_value    |
```

We can query `pg_class` with our `seqrelid`:

```sql
=> select * from pg_class where relfilenode = 41000;
-[ RECORD 1 ]-------+------------
relname             | freehanging
relnamespace        | 2200
reltype             | 41001
reloftype           | 0
relowner            | 24576
relam               | 0
relfilenode         | 41000
reltablespace       | 0
relpages            | 1
reltuples           | 1
relallvisible       | 0
reltoastrelid       | 0
relhasindex         | f
relisshared         | f
relpersistence      | p
relkind             | S
relnatts            | 3
relchecks           | 0
relhasoids          | f
relhasrules         | f
relhastriggers      | f
relhassubclass      | f
relrowsecurity      | f
relforcerowsecurity | f
relispopulated      | t
relreplident        | n
relispartition      | f
relrewrite          | 0
relfrozenxid        | 0
relminmxid          | 0
relacl              |
reloptions          |
relpartbound        |
```

We can create a second sequence we want to associate with the `users` table.

```sql
=> create sequence users_id_seq;
CREATE SEQUENCE
```

This will now show up in our queries.

```sql
=> select * from pg_sequence;
-[ RECORD 1 ]+--------------------
seqrelid     | 41000
seqtypid     | 20
seqstart     | 1
seqincrement | 1
seqmax       | 9223372036854775807
seqmin       | 1
seqcache     | 1
seqcycle     | f
-[ RECORD 2 ]+--------------------
seqrelid     | 41002
seqtypid     | 20
seqstart     | 1
seqincrement | 1
seqmax       | 9223372036854775807
seqmin       | 1
seqcache     | 1
seqcycle     | f

=> select * from pg_sequences;
-[ RECORD 1 ]-+--------------------
schemaname    | public
sequencename  | freehanging
sequenceowner | todo
data_type     | bigint
start_value   | 1
min_value     | 1
max_value     | 9223372036854775807
increment_by  | 1
cycle         | f
cache_size    | 1
last_value    |
-[ RECORD 2 ]-+--------------------
schemaname    | public
sequencename  | users_id_seq
sequenceowner | todo
data_type     | bigint
start_value   | 1
min_value     | 1
max_value     | 9223372036854775807
increment_by  | 1
cycle         | f
cache_size    | 1
last_value    |

```

We can perform a `join` on these catalogs.

```sql
=> select seqclass.relname, seqclass.relfilenode
from pg_class as seqclass
join pg_sequence as seq on (seq.seqrelid = seqclass.relfilenode);

-[ RECORD 1 ]-------------
relname     | freehanging
relfilenode | 41000
-[ RECORD 2 ]-------------
relname     | users_id_seq
relfilenode | 41002

```

We can go ahead and associate the new sequence with the `users` table by specifying `OWNED BY`. By setting `OWNED BY`, we are specifying that if the column is dropped, we want the sequence to be dropped as well.

```
=> alter sequence users_id_seq OWNED BY users.id;
ALTER SEQUENCE
```

This association is recorded by Postgres in the [`pg_depend`](https://www.postgresql.org/docs/current/catalog-pg-depend.html) catalog, using an `a` dependency type.

> DEPENDENCY_AUTO (a)
>
> The dependent object can be dropped separately from the referenced object, and should be automatically dropped (regardless of RESTRICT or CASCADE mode) if the referenced object is dropped. Example: a named constraint on a table is made autodependent on the table, so that it will go away if the table is dropped.


```sql
=> select * from pg_depend where objid = 41002 and deptype = 'a';
-[ RECORD 1 ]------
classid     | 1259
objid       | 41002
objsubid    | 0
refclassid  | 1259
refobjid    | 40997
refobjsubid | 1
deptype     | a

```

We can also verify that the `freehanging` sequence has no dependencies of type `a`.

```sql
=> select * from pg_depend where objid = 41000 and deptype = 'a';
(0 rows)

```

Now that we have a dependency identified for this relationship, we can verify that the dependency is indeed with the `users` table. For this, we will query using the dependency's `refobjid`.

```sql
=> select * from pg_class where relfilenode = 40997;
-[ RECORD 1 ]-------+------
relname             | users
relnamespace        | 2200
reltype             | 40999
reloftype           | 0
relowner            | 24576
relam               | 0
relfilenode         | 40997
reltablespace       | 0
relpages            | 0
reltuples           | 0
relallvisible       | 0
reltoastrelid       | 0
relhasindex         | f
relisshared         | f
relpersistence      | p
relkind             | r
relnatts            | 2
relchecks           | 0
relhasoids          | f
relhasrules         | f
relhastriggers      | f
relhassubclass      | f
relrowsecurity      | f
relforcerowsecurity | f
relispopulated      | t
relreplident        | d
relispartition      | f
relrewrite          | 0
relfrozenxid        | 5021
relminmxid          | 1
relacl              |
reloptions          |
relpartbound        |

```

We can indeed see that the dependency is on the `users` table.

What about the column associated with this dependency? Postgres stores information about table columns in [`pg_attribute`](https://www.postgresql.org/docs/current/catalog-pg-attribute.html) catalog. We can verify that the dependency is on the `id` column, by querying `pg_attribute`.

```sql
> select * from pg_attribute where attrelid=40997 and attnum = 1;
-[ RECORD 1 ]-+------
attrelid      | 40997
attname       | id
atttypid      | 20
attstattarget | -1
attlen        | 8
attnum        | 1
attndims      | 0
attcacheoff   | -1
atttypmod     | -1
attbyval      | t
attstorage    | p
attalign      | d
attnotnull    | t
atthasdef     | f
atthasmissing | f
attidentity   |
attisdropped  | f
attislocal    | t
attinhcount   | 0
attcollation  | 0
attacl        |
attoptions    |
attfdwoptions |
attmissingval |
```

We can see that the column corresponding to the dependency is indeed `id`.

Our `join` can now be improved to use this information. First, we will add the table name:

```sql
=> select seqclass.relname as sequencename, seqclass.relfilenode as sequenceref, dep.refobjid as depobjref, depclass.relname as tablename
from pg_class as seqclass
join pg_sequence as seq on (seq.seqrelid = seqclass.relfilenode)
join pg_depend as dep on (seq.seqrelid = dep.objid)
join pg_class as depclass on (dep.refobjid = depclass.relfilenode);
-[ RECORD 1 ]+-------------
sequencename | users_id_seq
sequenceref  | 41002
depobjref    | 40997
tablename    | users
```

We have to join twice on the `pg_class` catalog - once to get the `sequence`'s columns and once to get the `dependency`'s columns. This leaves us with the name of the table and the sequence name.

Finally, we can perform a join on `pg_attribute` to get column information.

```sql
=> select seqclass.relname as sequencename, seqclass.relfilenode as sequenceref, dep.refobjid as depobjref, depclass.relname as tablename, attrib.attname as column
from pg_class as seqclass
join pg_sequence as seq on (seq.seqrelid = seqclass.relfilenode)
join pg_depend as dep on (seq.seqrelid = dep.objid)
join pg_class as depclass on (dep.refobjid = depclass.relfilenode)
join pg_attribute as attrib on (attrib.attnum = dep.refobjsubid and attrib.attrelid = dep.refobjid);

-[ RECORD 1 ]+-------------
sequencename | users_id_seq
sequenceref  | 41002
depobjref    | 40997
tablename    | users
column       | id

```

We can drop `sequenceref` and `depobjref` from the result as it is not of particular interest to us when reporting this.

```sql
=> select seqclass.relname as sequencename, depclass.relname as tablename, attrib.attname as column
from pg_class as seqclass
join pg_sequence as seq on (seq.seqrelid = seqclass.relfilenode)
join pg_depend as dep on (seq.seqrelid = dep.objid)
join pg_class as depclass on (dep.refobjid = depclass.relfilenode)
join pg_attribute as attrib on (attrib.attnum = dep.refobjsubid and attrib.attrelid = dep.refobjid);

-[ RECORD 1 ]+-------------
sequencename | users_id_seq
tablename    | users
column       | id

```

This seems like information that should be surfaced by Postgres in an easier to access way. In fact there is a patch from [2008](https://web.archive.org/web/20190508035646/https://www.postgresql.org/message-id/1228622212.10877.59.camel%40godzilla.local.scalefeather.com) that would have introduced this capability. When Postgres 10 introduced the [`pg_sequences`](https://web.archive.org/web/20190508035646/https://www.postgresql.org/message-id/1228622212.10877.59.camel%40godzilla.local.scalefeather.com) catalog, it stopped at surfacing the id of the user who owns the sequence.

