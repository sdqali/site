---
bbcommentid: 11
categories:
- code
- groovy
- gradle
- android
comments: true
date: 2013-10-01
ghcommentid: 83
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- groovy
- gradle
- android
title: Reading user input in Gradle scripts
---

Continuing from the last [blog post](/blog/2013/10/01/accessing-environment-variables-in-gradle/), I have been looking at reading user input from a Gradle script. This was a result of Stack Overflow user *user672009*'s [question](http://stackoverflow.com/questions/18328730/how-to-create-a-release-signed-apk-file-using-gradle/19130098#19130098) about prompting for input from a Gradle script so the one does not have to include passwords in the script while checking in.

Just like the last example, the fact that Gradle scripts are written in a Groovy DSL comes to our help. Groovy's `System. console(). readLine` can be called from inside Gradle tasks. The same recipe from the last post can be rewritten to prompt for various parameters.

```
signingConfigs {
	release {
		storeFile file(System.console().readLine("\n\$ Enter keystore path: "))
		storePassword System.console().readLine("\n\$ Enter keystore password: ")
		keyAlias System.console().readLine("\n\$ Enter key alias: ")
		keyPassword System.console().readLine("\n\$ Enter key password: ")
	}
}

buildTypes {
	release {
		signingConfig signingConfigs.release
	}
}
```


### This is a bad idea
While Gradle allows this kind of prompts, this is a bad pattern for a build script, especially when the script is run remotely, for example on a Continuous Integration [^1] environment. The correct way to prevent hard coding of parameters like this is to access them from environment variables.

[^1]: Continuous Integration (CI) is a software development practice where code from different developers, on different components are integrated frequently with the aid of an automated build. Martin Fowler has a [great article](http://www.martinfowler.com/articles/continuousIntegration.html) about it.