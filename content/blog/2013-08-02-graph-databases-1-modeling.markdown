---
categories:
- code
- graphdb
- neo4j
- cypher
comments: true
date: 2013-08-02
ghcommentid: 66
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- graphdb
- neo4j
- cypher
title: Graph databases 1 - Modeling
---

I am making my way through the book _Graph Databases_ [^1] which is an introductory book to the subject from Neo Technology [^2], creators of Neo4j [^3]. At work, we are using Neo4j for a cool new thing we are building, and I see it as a great chance to learn some thing new and interesting. In the past, I have gone through a spiral [^4] when it comes to learning stuff and the constant feedback I get is to pick something that one gets to work with everyday and dig deep into it, in order to avoid the frustration and the inevitable spiral.

<!--more-->

This is obviously a completely new subject to me and I am enjoying it so far. I am going to write a series of blog posts about my effort to learn Graph Databases and my observations and learnings.

I am presently reading chapter 3, which deals with _Data Modeling with Graphs_. The key idea here is that the graph representation mirrors entities and relationships.

* Entities are represented by _nodes_ and their characteristics are represented as _properties_ of the node. Eg. : Cristiano Ronaldo is a _node_, while his height is a _property_.
* Relationships are modeled by _relationships_. Eg. : _OF_NATIONAL_TEAM_ is a _relationship_.
* Relationships always connect two _nodes_
* Relationships sometimes have properties. Eg. : _debut_ is a property of the _OF_NATIONAL_TEAM_ relationship.


# Example - European football players
If we were to model football players to have played for European clubs, a section of the graph will look like this:

!["Graph: Zidane and teams"](/images/graph_zidane.png "Graph: Zidane and teams")


# Building the graph with Cypher

Cypher [^5] is Neo4j's query language. It is essentially structured ASCII art that tries to be as close to how relationships are mapped on a graph. The above graph can be created in Neo4j using the following Cypher snippet:

```sql
CREATE (zidane {name: "Zinadine Zidane", position: "Midfielder" }),
(cannes {name: "A.S. Cannes", founded: 1902}),
(bordeaux {name: "F.C.G. de Bordeaux", founded: 1881}),
(juventus {name: "Juventus F.C.", founded: 1897}),
(realmadrid {name: "Real Madrid C.F.", founded: 1902}),
(spain {name: "Spain"}),
(france {name: "France"}),
(italy {name: "Italy"}),
(zidane)-[:OF_NATIONAL_TEAM{debut: "19940817"}]->(france),
(zidane)-[:PLAYED_FOR_CLUB]->(cannes),
(zidane)-[:PLAYED_FOR_CLUB]->(bordeaux),
(zidane)-[:PLAYED_FOR_CLUB]->(juventus),
(zidane)-[:PLAYED_FOR_CLUB]->(realmadrid),
(cannes)-[:OF_FA]->(france),
(bordeaux)-[:OF_FA]->(france),
(juventus)-[:OF_FA]->(italy),
(realmadrid)-[:OF_FA]->(spain);
```

That is pretty straight forward and easy to grok. We define 8 nodes representing Zidane, the 4 clubs he played for and the 3 countries these clubs play in. Then we define the Relationships between them. Cypher uses the -> to represent a relationship between nodes.

# Querying the graph

Querying the graph we created for interesting things is where the fun really is.

* To figure out what clubs Zidane played for, we will write the following Cypher snippet:

```sql
MATCH (zidane)-[:PLAYED_FOR_CLUB]->(club)
RETURN club;
```

When executed:

```bash
neo4j-sh (?)$ MATCH (zidane)-[:PLAYED_FOR_CLUB]->(club)
>             RETURN club;
+--------------------------------------------------+
| club                                             |
+--------------------------------------------------+
| Node[53]{founded:1902,name:"A.S. Cannes"}        |
| Node[54]{founded:1881,name:"F.C.G. de Bordeaux"} |
| Node[55]{founded:1897,name:"Juventus F.C."}      |
| Node[56]{founded:1902,name:"Real Madrid C.F."}   |
+--------------------------------------------------+
```

What if the question is _When were all the clubs Zidane played for founded?_ We will answer it with the following query:

```sql
MATCH (zidane)-[:PLAYED_FOR_CLUB]->(club)
RETURN club.founded;
```

* Let's try to answer _When did Zidane make his international debut?_. Let's try the following query:

```sql
MATCH (zidane)-[player:OF_NATIONAL_TEAM]->(team)
RETURN player.debut;
```
This when executed will result in:

```console
+--------------+
| player.debut |
+--------------+
| "19940817"   |
+--------------+
```

Here, _[player:OF_NATIONAL_TEAM]_ specifies a relationship of type _OF_NATIONAL_TEAM_ and labels it as _player_ so that we can later extract out the _debut_ property from _player_.

It can be seen from this example that, sometimes we are not really interested in extracting out certain information, although we want that information to be part of the query. Here, we don't really care what national team Zidane played for, we are just intested in an attribute of the relationship. Cypher allows you to represent this intend to ignore.

```sql
MATCH (zidane)-[player:OF_NATIONAL_TEAM]->()
RETURN player.debut;
```

The above query will produce the same result as the previous query. The _()_ specifies that there is some node there, but we are not interested in what it represents.

* The ability to ignore can be leveraged to answer our next question. _What all countries have Zidane played league football in?_

```sql
MATCH (zidane)-[:PLAYED_FOR_CLUB]->()-[:OF_FA]->(fa)
RETURN DISTINCT fa.name;
```

The result:

```bash
+----------+
| fa.name  |
+----------+
| "France" |
| "Italy"  |
| "Spain"  |
+----------+
```

We use _DISTINCT_ to get uniques because Zidane played for Cannes and Bordeaux, both of the French Ligue 1.

# Summary

I am still making my way through the book. So far it has looked promising and I have been able to grasp things. I am looking forward to learning more complex querying and will write about it in the subsequent blog posts.

[^1]: [Graph Databases by Ian Robinson, Jim Webber, and Emil Eifrem (O’Reilly). Copyright 2013 Neo Technology, Inc., 978-1-449-35626-2.](http://graphdatabases.com/)
[^2]: [Neo Technology](http://www.neotechnology.com/)
[^3]: [Neo4j](http://www.neo4j.org/)
[^4]: [The Spiral of Learning](http://blog.sdqali.in/blog/2012/05/30/the-spiral-of-learning/)
[^5]: [What is Cypher?](http://docs.neo4j.org/chunked/stable/cypher-introduction.html)