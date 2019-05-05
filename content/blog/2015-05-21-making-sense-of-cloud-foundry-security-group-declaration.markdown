---
Categories:
- development
- cloudfoundry
- devops
Description: ''
Tags:
- development
- cloudfoundry
- paas
- json
- devops
date: 2015-05-22 05:58:41
ghcommentid: 99
title: Making sense of Cloud Foundry security group declarations
---

Cloud Foundry allows fine grained declaration of security groups, down to IP address ranges and Ports. While this provides great flexibility, making sense of why each rule in a security group exists and what each does is really difficult because of the limitations of the security group declaration mechanism.

<!--more-->

The Cloud Foundry command line tool allows the creation of security groups from JSON declarations. The `create-security-group` command works like so:

```bash
> cf create-security-group SECURITY_GROUP PATH_TO_JSON_RULES_FILE
```
 The JSON file needs to declare an array of rules where each rule has the following structure:

```json
{
   "protocol": "tcp",
   "destination": "10.244.1.18",
   "ports": "3306",
   "log": true
}
```

In my Cloud Foundry environment, I have a security group assigned to a `Space` with the following declaration:

```json
[
  {"protocol":"tcp","destination":"<ip-foo>","ports":"3306"},
  {"protocol":"tcp","destination":"<some-ip>-<another-ip>","ports":"55882"},
  {"protocol":"tcp","destination":"<ip-bar>","ports":"443"}
]
```
With only 3 rules in place, it is already confusing what service each rule is for and why they are there.

I believe this can be easily improved by allowing an extra field `comment` that provides context about each rule. With this in place, the rules will look like this:

```json
[
  {"protocol":"tcp","destination":"<ip-foo>","ports":"3306", "comment": "Allow database connection to PostgreSQL at hosted-postgres-service.com"},
  {"protocol":"tcp","destination":"<some-ip>-<another-ip>","ports":"55882", "comment": "Allow logging to hosted-logging-service.com"},
  {"protocol":"tcp","destination":"<ip-bar>","ports":"443", "comment": "Allow monitoring service at hosted-monitoring-service.com"}
]
```

As things stand, Cloud Foundry Cloud Controller does not allow any extra fields to exist in a rule. For example, the above declaration will cause an error while trying to create a security group.

```bash
> cf create-security-group sample-space-security-group spec.json

Server error, status code: 400, error code: 300001, message: The security group is invalid: rules rule number 1 contains the invalid field 'comment', rules rule number 2 contains the invalid field 'comment', rules rule number 3 contains the invalid field 'comment'

```

If JSON allowed comments, commenting would result in a slightly more readable declaration file, although it won't be stored in the Cloud Controller database and hence won't be available upon querying with `cf security-group <security-group-name>`. This is a moot point anyway, as JSON [explicitly](https://plus.google.com/+DouglasCrockfordEsq/posts/RK8qyGVaGSr) doesn't allow comments. There are workarounds that involve minifying the JSON input before parsing the configurations, but I don't think that is the right direction to head to.

I have filed a [ticket](https://github.com/cloudfoundry/cloud_controller_ng/issues/382) against Cloud Controller to address this issue. It [doesn't look like a difficult](https://github.com/cloudfoundry/cloud_controller_ng/blob/cacb5563264208e920f4b7fecc7060f89b929fbb/lib/cloud_controller/rule_validator.rb#L6) feature to implement. Hopefully this is available in Cloud Controller soon.