---
bbcommentid: 98
date: 2019-03-23 19:46:08
ghcommentid: 141
tags:
- SAS
- development
title: Understanding trailing @ processing in SAS input
---

One of the first things I noticed when I started poking around in SAS code is that the `input` statement is very powerful, flexible and hence sometimes hard to understand. It can read pretty much anything in to a dataset as long as you tell it what to do.

The use of trailing `@`s to take control of how SAS advances the input pointer is a powerful technique to read from input files where the data is laid out in non-standard formats. In this blog post, we will try to understand how trailing `@` processing works with the help of some `infile` statement options and the `putlog` statement to write to the SAS log.

Let's take this example from the excellent paper _The Input Statement: Where It's @_ [^1] - given an put file where the first variable has to be read beginning from a particular column in the input line based on the value of the second variable.

```sas
Age  Type
23   1
  44 2
```

A first pass at trying to do this will result in code like this:

```sas
data ages;
  input @6 type $1.;

  if type='1' then
    input @1 age 2.;
  else if type='2' then
    input @3 age 2.;
  drop type;
  datalines;
23   1
  44 2
;
run;

proc print data=ages;
  title "Age read without trailing @";
run;
```

The result we get is not what we expect.

```sas
| Obs | Age |
|-----|-----|
| 1   | .   |
```

We can understand how SAS read this input using the `line=` and `column=` options of the `infile` statement. While the code in the above listing does not explicitly use `infile` to point at the `datalines`, this can be done when we want to use `infile`'s options with `datalines`.

This is a good time to remind us what the `line=` and `column=` options of `infile` does. From the [documentation](https://documentation.sas.com/?docsetId=lestmtsref&docsetTarget=n1rill4udj0tfun1fvce3j401plo.htm&docsetVersion=9.4&locale=en):

> LINE=variable

> specifies a variable that SAS sets to the line location of the input pointer in the input buffer. As with automatic variables, the LINE= variable is not written to the data set.

> COLUMN=variable

> names a variable that SAS uses to assign the current column location of the input pointer. As with automatic variables, the COLUMN= variable is not written to the data set.

We can modify our code to set these options and then print the value of all variables including these options using the `_all_` variable that prints the _Program Data Vector (PDV)_.

```sas
data ages;
  infile datalines line=line column=col;

  input @6 type $1.;
  putlog "After reading type, before reading age: " _all_ ;

  if type='1' then
    input @1 age 2.;
  else if type='2' then
    input @3 age 2.;
  putlog "After reading age: " _all_ ;
  putlog "";

  drop type;
  datalines;
23   1
  44 2
;
run;
```

When the code runs, the following can be seen in the SAS logs:

```sas
 After reading type, before reading age: line=1 col=7 type=1 age=. _ERROR_=0 _N_=1
 After reading age: line=2 col=3 type=1 age=. _ERROR_=0 _N_=1
 "
```

After `type` is read, we can see that the pointer is at line `1` and column `7`, which makes sense considering that the code instructs SAS to go to column `6` and read `1` character. But then we notice that when `age` is read, the pointer has moved to `2` and column `3` as instructed in the first branch of the `if else` condition. Since there is nothing at column `1-2` of line `2` in the input, a missing value is stored in `age`.

What we want is some way to tell `input` to ot move the pointer after the first input statement. This is where the single trailing `@` comes in. It intructs `input` to stay on the same line for the next `input` statement in the `data` step. The above listing modified to use trailing `@` is as follows:

```sas
data trailing;
  infile datalines line=line column=col;

  input @6 type $1. @;
  putlog "After reading type, before reading age: " _all_ ;

  if type='1' then
    input @1 age 2.;
  else if type='2' then
    input @3 age 2.;
  putlog "After reading age: " _all_ ;
  putlog "";

  drop type;
  datalines;
23   1
  44 2
;
run;
```

The following log lines are written:

```sas
 After reading type, before reading age: line=1 col=7 type=1 age=. _ERROR_=0 _N_=1
 After reading age: line=1 col=3 type=1 age=23 _ERROR_=0 _N_=1
 "
 After reading type, before reading age: line=1 col=7 type=2 age=. _ERROR_=0 _N_=2
 After reading age: line=1 col=5 type=2 age=44 _ERROR_=0 _N_=2
 "
```

The log shows that `input` stayed on line `1` even after reading the `type` variable.

The new dataset has the expected values:

```sas
| Obs | Age |
|-----|-----|
| 1   | 23  |
| 2   | 44  |
```

Here is another example that you often run in to on the internet when discussing trailing `@`:

```sas
data  colors;
  infile datalines line=linenum column=col;
  input @1 Var1 $ @8 Var2 $ @;
  putlog "After reading Var1 and Var2: " _all_;

  input @1 Var3 $ @8 Var4 $ ;
  putlog "After reading Var3 and Var4: " _all_;
  putlog "";

  datalines;
RED    ORANGE  YELLOW  GREEN
BLUE   INDIGO  PURPLE  VIOLET
CYAN   WHITE   FUCSIA  BLACK
GRAY   BROWN   PINK    MAGENTA
;
run;
```

This results in the following dataset:

```sas
|Obs  | Var1 | Var2   | Var3 | Var4   |
|-----|------|--------|------|--------|
| 1   | RED  | ORANGE | RED  | ORANGE |
| 2   | BLUE | INDIGO | BLUE | INDIGO |
| 3   | CYAN | WHITE  | CYAN | WHITE  |
| 4   | GRAY | BROWN  | GRAY | BROWN  |
```

Because of the trailing `@` in the first `input` statement, the values of `Var1` and `Var3` for all the observations are the same, as both are read from column `1`. Similarly `Var2` and `Var4` are the same as they are read from column `8`.

[^1]: The Input Statement: Where It's @. Paper 253-29, SUGI 29 Proceedings.