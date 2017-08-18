---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Clojure Dojo - Levenshtein edit distance"
date: 2014-03-20
comments: true
categories:
- code
- clojure
- algorithms
- development
tags:
- code
- clojure
- algorithms
- development
---
I have been playing around with Clojure and after familiarising myself with the core, I decided to start writing little programs that forces me to choose the right idioms. I am starting off with Levenshtein edit distance of two strings.

### Levenshtein edit distance
Levenshtein edit distance between two string is a way of quantifying how similar or dissimilar they are, lower distance implying higher similarity. The algorithm to calculate Levenshtein distance is fairly simple - the algorithm cares about three operations that can be performed at a particular position in a string to move it towards the other - insertion, deletion and substitution.

This can be recursively solved for two strings `A0:AS` and `B0:BS` by comparing `AS`, `B0:BS`; `A0:AS`, `BS` and `AS`, `BS`.

### Code
```clojure
(ns clojure_dojo.core)

(defn edit-distance
  "Return the Levenshtein edit distance between two strings"
  [first second]
  (cond
   (empty? first) (count second)
   (empty? second) (count first)
   :else (min (+ 1 (edit-distance (drop 1 first) second))
              (+ 1 (edit-distance first (drop 1 second)))
              (+ (cond
                  (= (take 1 first) (take 1 second)) 0
                  :else 1)
                 (edit-distance (drop 1 first) (drop 1 second))))))
```

### Test
```clojure
(ns clojure_dojo.t-core
  (:use midje.sweet)
  (:use [clojure_dojo.core]))

(facts "about `edit-distance`"
       (fact "it returns length of other string if one string is empty"
             (edit-distance "foo" "") => 3
             (edit-distance "" "foo") => 3)
       (fact "detects deletions"
             (edit-distance "foo" "oo") => 1)
       (fact "detects substitutions"
             (edit-distance "ab", "cd") => 2)
       (fact "detects additions needed"
             (edit-distance "oo", "foo") => 1
             (edit-distance "kit", "sitting") => 5
             (edit-distance "intention", "execution") => 5
             (edit-distance "sittin", "sitting") => 1))
```

### The problem with this approach
This solution looks fine - it passes the tests. However, if we carefully observe the recursion tree, we notice that there are sub-problems that are solved multiple times and this makes this algorithm's order of complexity Θ(3^min(m, n)). This can be observed from the call tree of this recursion.

### Improvement
Recursive algorithms of this nature can be improved in two ways - memoization during recursion or applying [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) in a bottom up manner. The next blog post in this series will deal with how these two approaches can be done in Clojure.

The code for the above solution is on [GitHub](https://github.com/sdqali/clojure-dojo).
