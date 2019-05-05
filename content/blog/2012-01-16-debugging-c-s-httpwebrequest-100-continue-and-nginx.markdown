---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Debugging: C Sharp's HttpWebRequest, 100-Continue and nginx"
date: 2012-01-16
comments: true
categories:
- c#
- code
- debug
- nginx
- rails
- development
tags:
- c#
- code
- debug
- nginx
- rails
- development
aliases:
- "/2012/01/debugging-c-httpwebrequest-100-continue.html"
---

Recently I spent some time debugging an issue our team was facing around some C# code making a request on one of our servers. The request was throwing a `The server committed a protocol violation. Section=ResponseStatusLine` error.

Initial investigation suggested that this could happen if we are making HTTP/1.1 requests to a server configured for HTTP/1.0. Our Rails application runs on Mongrel fronted with nginx 0.6.5. We modified the C# code to use HTTP/1.0 and the error went away. The following line does the trick.

```c#
request.ProtocolVersion = HttpVersion.Version10;
```

But wait! This means that somewhere in the chain, a server is configured to use HTTP/1.0. It looked unlikely and further debugging revealed that it was indeed not the case. Further staring at the Rails logs showed that one of the headers that the app expects was not being set, when the request was done using HTTP/1.1 from the code.

After some time, we figured <a href="http://stackoverflow.com/questions/2482715/the-server-committed-a-protocol-violation-section-responsestatusline-error">out</a> that the .Net library throws the `server committed ...` error if it is expecting the HTTP 100 (Continue) response in the wrong way. We set the code to not expect the HTTP 100 response from the server using

```c#
request.ServicePoint.Expect100Continue = false;
```

and voila, it worked. The Rails app received all the headers it expected and things worked fine. The code looked like this:

```c#
var request = (HttpWebRequest) HttpWebRequest.Create("https://example.com/foo");
request.ServicePoint.Expect100Continue = false;
request.Credentials = new NetworkCredential("user", "password");
request.Method = "PUT";
request.ContentType = "application/x-www-form-urlencoded";
byte[] objByteArray = Encoding.UTF8.GetBytes("foo=bar");
request.ContentLength = objByteArray.Length;
var dataStream = request.GetRequestStream();
dataStream.Write(objByteArray, 0, objByteArray.Length);
dataStream.Close();

var response = request.GetResponse();
```


So what is happening?

The HTTP 100 status is supposed to work like this. When a client has to send some data, instead of sending it upfront, it can send some headers along with the "Expect:100-Continue" header. The server responds with a 100 if it is willing to accept the request or send a final status. The spec is <a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3">here</a>.

We are using nginx as a proxy. The specification says that the proxy should forward the request if it knows that the next-hop server is HTTP/1.1 compliant. The proxy is supposed to ignore the "Expect:100-Continue" header, if the request came from a client using HTTP/1.0.

In our case, the default behavior of the .Net HTTP client library is to set "Expect:100-Continue" header on every request for HTTP/1.1. So the client sends only some headers and waits for the 100 response from nginx. Nginx sees the request, knows that Mongrel supports HTTP/1.1 and just forwards the request. The app sends a 401 because it could not authenticate. The client is expecting a 100 and gets a 401. It thinks the server committed a protocol violation.

When we ask the client to use HTTP/1.0, the .Net library does not use the Expect header, sends all the headers and nginx forwards the request to Mongrel. The authentication goes through.

When we explicitly set the Expect 100 property of the library to false, it sends all the headers at once and the authentication goes through fine.

Looks like there is a way to tell .Net not to expect 100 from the server through configuration, by putting this in <app>.exe.conf</app>

```xml
<system.net>
  <settings>
    <servicePointManager expect100Continue="false"/>
  </settings>
</system.net>
```


1. http://stackoverflow.com/questions/2482715/the-server-committed-a-protocol-violation-section-responsestatusline-error
2. http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3
