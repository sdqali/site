---
bbissueid: 40
categories:
- code
- development
- java
- jmeter
- performance-test
- tools
comments: true
date: 2014-02-17
ghissueid: 93
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- java
- jmeter
- performance-test
- tools
title: A simple JMeter test with login
---

<meta content="jmeter, login" name="keywords">
I had to set up a JMeter test last week - the test included logging in to a site, and then hitting a bunch of URLs, all of them being GET requests. I found it hard to find a simple documentation that described how to do this - the ones I found were either incomplete or were trying to teach me a large number of things at the same time. So when I figured it out, I decided to write this down, for anyone else finding themselves in the same place as me.

For this example, the application under test is a simple Rails application, with the login form at `/login` and a `POST` request to `/login` does the authentication.

### Add a Thread Group
A Thread Group defines a pool of users that will execute a particular test case against the server. JMeter makes the number of users, and the ramp-rate configurable. For the purpose of this example, Number of Threads is 2 and the ramp up time period is 1 second. This thread group is also configured to run forever.
!["Screenshot of Thread Group window"](/images/jmeter/thread_group.png "Thread Groups")

### HTTP Request Defaults
The net step is to add an HTTP Request Defaults configuration element to the Thread Group. This configuration element sets up the domain or I.P. address of the server, the port and the protocol (HTTP / HTTPS). In this example, Server Name is `127.0.0.1` and Port is `3000`.
!["Screenshot of HTTP Request Defaults"](/images/jmeter/request_defaults.png "HTTP Request Defaults")

### HTTP Cookie Manager
A cookie manager stores and sends cookies, as a web browser would do if an actual user was hitting the server. For the purposes of this example, the default configurations are enough.
!["Screenshot of Cookie Manager"](/images/jmeter/cookie_manager.png "Cookie Manager")

### Implement normal page actions
From this point, all that remains is to implement HTTP Requests to the end points that are relevant to this test. In this example, we navigate to the Login page at `/login`, fire a `POST` request to `/login` with the appropriate form input values and proceed to the Admin page.