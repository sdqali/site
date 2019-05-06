---
Categories:
- development
- java
Description: ''
Tags:
- development
- tomcat
- java
bbcommentid: 48
date: 2015-06-09 05:11:05
ghcommentid: 100
image: images/1280px-Tomcat-logo.svg.png
title: Running multiple applications in the same Tomcat installation
---

This blog post describes how to set up Tomcat to run multiple applications running as separate JVM processes, using the same Tomcat installation. This method utilizes the `CATALINA_HOME` and `CATALINA_BASE` environment variables used by Tomcat. I have verified this method against Tomcat versions `8.0.x`; other versions should work the same way.

<!--more-->

## A typical Tomcat installation

If we explode the Tomcat 8.0.23 [tarball](http://mirrors.sonic.net/apache/tomcat/tomcat-8/v8.0.23/bin/apache-tomcat-8.0.23.tar.gz), we get the following directory structure:

```bash
$ tar apache-tomcat-8.0.23.tar.gz

$ ls apache-tomcat-8.0.23/
LICENSE		RELEASE-NOTES	bin		lib		temp		work
NOTICE		RUNNING.txt	conf		logs		webapps
```
This distribution, by default runs applications in a single JVM. How does it do this?

Tomcat control scripts - `startup.sh`, `shutdown.sh`, `catalina.sh` uses the environment variables `CATALINA_HOME` and `CATALINA_BASE` to locate binaries and configuration files.

From the documentaion inside `catalina.sh` under `apache-tomcat-8.0.23/bin/` we can see that:
```bash
#   CATALINA_HOME   May point at your Catalina "build" directory.
#
#   CATALINA_BASE   (Optional) Base directory for resolving dynamic portions
#                   of a Catalina installation.  If not present, resolves to
#                   the same directory that CATALINA_HOME points to.

```
This allows us to separate the `CATALINA_HOME` and `CATALINA_BASE` directories. The Tomcat binaries and scripts need to be inside `CATALINA_HOME` and our first application can deploy itself to `CATALINA_BASE`.

## Separating CATALINA_HOME and CATALINA_BASE

The `app1` directory will have the following directories:
```bash
$ ls -a app1/
.	..	bin	conf	logs	temp	webapps	work
```
The `bin` directory will have the `setenv.sh` script used to set additional environment variables for the application.

The `tomcat` directory will have the following directories:
```bash

$ ls tomcat/
LICENSE		NOTICE		RELEASE-NOTES	RUNNING.txt	bin		lib
```
The `bin` directory will have the Tomcat management scripts like `startup.sh`, `shutdown.sh`, `catalina.sh` etc.

Now we can start `app1` by pointing `CATALINA_BASE` to `app1` and `CATALINA_HOME` to `tomcat`.
```bash

$ export CATALINA_HOME=/Users/sdqali/src/sandbox/tomcat

$ export CATALINA_BASE=/Users/sdqali/src/sandbox/app1

$ $CATALINA_HOME/bin/startup.sh

$ $CATALINA_HOME/bin/startup.sh
Using CATALINA_BASE:   /Users/sdqali/src/sandbox/app1
Using CATALINA_HOME:   /Users/sdqali/src/sandbox/tomcat
Using CATALINA_TMPDIR: /Users/sdqali/src/sandbox/app1/temp
Using JRE_HOME:        /Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home
Using CLASSPATH:       /Users/sdqali/src/sandbox/tomcat/bin/bootstrap.jar:/Users/sdqali/src/sandbox/tomcat/bin/tomcat-juli.jar
Tomcat started.

$ curl -s -D - -o /dev/null http://127.0.0.1:8080
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Date: Tue, 09 Jun 2015 07:37:43 GMT
```
Let's try and deploy a second application `app2` running on port `9090`.
```bash

$ export CATALINA_HOME=/Users/sdqali/src/sandbox/tomcat

$ export CATALINA_BASE=/Users/sdqali/src/sandbox/app2

$ $CATALINA_HOME/bin/startup.sh
Using CATALINA_BASE:   /Users/sdqali/src/sandbox/app2
Using CATALINA_HOME:   /Users/sdqali/src/sandbox/tomcat
Using CATALINA_TMPDIR: /Users/sdqali/src/sandbox/app2/temp
Using JRE_HOME:        /Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home
Using CLASSPATH:       /Users/sdqali/src/sandbox/tomcat/bin/bootstrap.jar:/Users/sdqali/src/sandbox/tomcat/bin/tomcat-juli.jar
Tomcat started.

$ curl -s -D - -o /dev/null http://127.0.0.1:9090
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Date: Tue, 09 Jun 2015 07:41:02 GMT
```

## Tying it all together

At this point, it is useful to create management scripts that abstract away the environment variables and allows for starting up and shutting down applications individually. The `start.sh` script will be as follows.

```bash
#!/usr/bin/env sh

# start.sh
# Script to start a Tomcat application

show_usage() {
    echo "Usage: ./start.sh <app-name>";
    exit 1;
}

declare app_name=$1;
[[ -z $app_name ]] && show_usage;


declare INSTALL_BASE=/Users/sdqali/src/sandbox

export CATALINA_HOME=$INSTALL_BASE/tomcat
export CATALINA_BASE=$INSTALL_BASE/$app_name

$CATALINA_HOME/bin/startup.sh
```
Similarly, the `stop.sh` script will be:
```bash
#!/usr/bin/env sh

# stop.sh
# Script to stop a Tomcat application

show_usage() {
    echo "Usage: ./stop.sh <app-name>";
    exit 1;
}

declare app_name=$1;
[[ -z $app_name ]] && show_usage;


declare INSTALL_BASE=/Users/sdqali/src/sandbox

export CATALINA_HOME=$INSTALL_BASE/tomcat
export CATALINA_BASE=$INSTALL_BASE/$app_name

$CATALINA_HOME/bin/shutdown.sh
```

We can manage individual applications using these scripts:

```bash
$ ./management/start.sh app2
Using CATALINA_BASE:   /Users/sdqali/src/sandbox/app2
Using CATALINA_HOME:   /Users/sdqali/src/sandbox/tomcat
Using CATALINA_TMPDIR: /Users/sdqali/src/sandbox/app2/temp
Using JRE_HOME:        /Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home
Using CLASSPATH:       /Users/sdqali/src/sandbox/tomcat/bin/bootstrap.jar:/Users/sdqali/src/sandbox/tomcat/bin/tomcat-juli.jar
Tomcat started.

$ nc -z  127.0.0.1 9090
Connection to 127.0.0.1 port 9090 [tcp/websm] succeeded!

$ curl -s -D - -o /dev/null http://127.0.0.1:9090
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Date: Tue, 09 Jun 2015 08:16:05 GMT


$ ./management/stop.sh app2
Using CATALINA_BASE:   /Users/sdqali/src/sandbox/app2
Using CATALINA_HOME:   /Users/sdqali/src/sandbox/tomcat
Using CATALINA_TMPDIR: /Users/sdqali/src/sandbox/app2/temp
Using JRE_HOME:        /Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home
Using CLASSPATH:       /Users/sdqali/src/sandbox/tomcat/bin/bootstrap.jar:/Users/sdqali/src/sandbox/tomcat/bin/tomcat-juli.jar

$ nc -z  127.0.0.1 9090

$ curl -v http://127.0.0.1:9090
* Rebuilt URL to: http://127.0.0.1:9090/
* Hostname was NOT found in DNS cache
*   Trying 127.0.0.1...
* connect to 127.0.0.1 port 9090 failed: Connection refused
```