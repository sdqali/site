---
aliases:
- /blog/2018/05/04/freebuilder-plugin-for-intellij/
bbcommentid: 104
date: 2018-05-05 05:27:35
ghcommentid: 137
tags:
- java
- freebuilder
- intellij
title: FreeBuilder plugin for IntelliJ
---

My work uses [FreeBuilder](http://freebuilder.inferred.org/) extensively to generate the [Builder](https://en.wikipedia.org/wiki/Builder_pattern) pattern for Java classes. In addition to this, we use the generated Builder classes to deserialize the data calsses using Jackson. After a while it became tiresome to type `@FreeBuilder` and `class Builder extends ...` everywhere. So I decided to write and IntelliJ IDEA plugin that does it for me.

<!--more-->

These are the things I wanted the plugin to do for me:

1. Annotate the public class from the current file with `@FreeBuilder` annotation.
1. Create an inner class for the annotated class - this should be a `static` class if the annotated class is an `abstract` class and a child class if the annotated class is an `interface`.
1. Ensure that the generated `Builder` class is annotated with `@JsonIgnoreProperties(ignoreUnknown=true)` because this is a convention we like to follow.
1. Ensure that the parent class gets annotated with `@JsonDeserialize(builder=...)` annotation.
1. Rebuild the project so that the annotation processing for FreeBuilder runs.

After poking around the IntelliJ Plugin development documentation, I was able to write a simple enough plugin that does it. For whatever reason, trying to find how to achieve simple things like how to create a new class that you can add as a child to an existing class was painful.

The plugin is available [here](https://plugins.jetbrains.com/plugin/10705-freebuilder-plugin) from the IntelliJ plugin repository and the source code is here on [GitHub](https://github.com/sdqali/freebuilder-intellij-plugin). In addition to the above mentioned features, I wanted to make sure that the annotations gets added only if the annoattion classes were in the classpath of the current module. The plugin also displayes messages when it decides to skip a step because an annotation class was not in the classpath or because nnotations already exist on the class.

A short demo of the plugin in action is shown below.

!["FreeBuilder Plugin Demo"](/images/freebuilder-plugin-demo.gif "FreeBuilder Plugin Demo")