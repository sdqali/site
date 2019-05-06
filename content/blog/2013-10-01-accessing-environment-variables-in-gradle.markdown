---
bbcommentid: 10
categories:
- code
- groovy
- gradle
- android
comments: true
date: 2013-10-01
ghcommentid: 82
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- groovy
- gradle
- android
title: Accessing Environment Variables in Gradle
---

I have been writing a fun Android App. [Share With Title](https://play.google.com/store/apps/details?id=in.sdqali.sharewithtitle) is a small application that allows you to share web pages you are reading to other applications without having to jump through the messy copy-paste hoop. (You should try it. If you share stuff from the web like I do, it will save you a lot of time and frustration). I have been coding on [Android Studio](https://developer.android.com/sdk/installing/studio.html), Google's IntelliJ based IDE for Android development. It uses Gradle for build scripts. Gradle is a Groovy based DSL [^1] for declaratively specifying build tasks. From what I have seen so far, it looks like an improvement over Ant.

While attempting to build a signed version of my app, I found a [Gradle recipe](http://stackoverflow.com/questions/18328730/how-to-create-a-release-signed-apk-file-using-gradle) for signing Android applications. However, it used hard coded parameters including passwords. This lead me to figuring out how to use environment variables in Gradle scripts.

Since Gradle scripts are Groovy files, Groovy's `System.getEnv` method will do the trick. The recipe modified to use this and thereby eliminate hard coded parameters will look like this:

```
signingConfigs {
	release {
		storeFile file(System.getenv("KEYSTORE"))
		storePassword System.getenv("KEYSTORE_PASSWORD")
		keyAlias System.getenv("KEY_ALIAS")
		keyPassword System.getenv("KEY_PASSWORD")
	}
}

buildTypes {
	release {
		signingConfig signingConfigs.release
	}
}
```

[^1]: A Domain Specific Languages (DSL) is a languages targeted to a particular kind of problem. Martin Fowler has a very good description of them [here](http://martinfowler.com/bliki/DomainSpecificLanguage.html). Build scripts like Make, Ant and Rake are all DSLs.