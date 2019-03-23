---
title: Importing the SASUSER datasets in SAS Studio
date: 2019-03-23T11:14:06-07:00
tags:
- sas
- development
---

I have been playing around with SAS for the last two weeks. I started with a SAS University Edition running on a VirtualBox instance on my MacBook, but soon realized that it was way more convenient to use a SAS OnDemand account. Having made the switch, I realized that all learning materials made references to and used examples with datsets from a library named `SASUSER`.

It was not clear how to get these datasets and use them in SAS Studio. After a bunch of searches, I found [this page](https://communities.sas.com/t5/SAS-Certification/How-to-get-SASUSER-library-s-data-sets/m-p/306631/highlight/true#M124) that pointed at data set up scripts for these datasets. The URL it pointed to had of course been repurposed and now redirected to a marketing page. After going back through multiple versions of the page on Internet Archive, I finally managed to find a [snapshot](https://web.archive.org/web/20151005165134/http://support.sas.com:80/publishing/cert/basecertguide3.html) that linked to a set up file that worked.

Here are the steps to use the setup script:

* Download the [script](https://support.sas.com/content/dam/SAS/support/en/books/data/sampledata.txt). Depending on the version of the material you are using, you may want to grab an [older snapshot](https://web.archive.org/web/20150921023746/http://support.sas.com/publishing/cert/sampdata.txt) from the Internet Archive.
* Rename the file so that it's extension is changed to `.sas`.
* Create a directory under your home directory in SAS Studio, for example `sasuser`.
* Upload the sample data script from step 1 to this folder, using the web interface.
* Create a new SAS source file named `libname.sas` with the following content:

```sas
libname sasuser "~/sasuser";
```

* Execute this script.
* Now execute the sample data script.
* It should create all the datsets you need in the library named `sasuser`. You can verify this using the following script:

```sas
proc contents data=sasuser._all_ nods;
run;
```
