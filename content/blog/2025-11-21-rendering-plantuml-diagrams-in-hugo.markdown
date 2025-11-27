---
title: "Rendering PlantUML Diagrams in Hugo"
date: 2025-11-20T19:45:44-08:00
tags:
- hugo
- plantuml
ghissueid: 148
bbissueid: 141
---

This blog is generated using Hugo [^1]. I have always wished that it had a way to render PlantUML diagrams [^2]. I am not alone in wishing for this - this is a feature that people have requested for over 5 years for now [^3]. But because of the peculiarities of Hugo's opinionated security posture [^4] and how PlantUML requires starting a Java process [^5], it has always been rejected [^6]. People have found various workarounds:

<!--more-->

1. Render the diagram in the browser using JavaScript that uses the public PlantUML server. [^7]
2. Adding a goldmark [^8] plugin that executes PlantUML commands [^9]. This is an approach that the Hugo team has explicitly rejected. [^10]
3. A pre-processing step that executes PlantUML before Hugo builds the pages. [^11]

After having to pre-generate the diagram images, I began wondering if this could be done at build time using a shortcode [^12] that called the PlantUML API. Hugo does expose a `resources.GetRemote` [^13] function to templates and shortcodes that can perform HTTP calls, as long as these calls are explicitly allowed in Hugo's security configuration. [^14]

This is what I came up with:

```go-html-template
// layouts/shortcodes/plantuml.html
{{ $baseUrl := site.Params.plantuml.baseUrl }}
{{ $content := .Inner }}

{{ $opts := dict
  "method" "POST"
  "body" $content
  "headers" (dict "Content-Type" "text/plain; charset=utf-8")
}}

{{ with resources.GetRemote $baseUrl $opts }}
  {{ $contentType := .MediaType.Type }}
  {{ if or (eq $contentType "image/svg+xml") (strings.Contains $contentType "svg") }}
    <div class="plantuml-svg">
      {{ .Content | safeHTML }}
    </div>
  {{ else if or (eq $contentType "image/png") (strings.Contains $contentType "png") }}
    <div class="plantuml-png">
      <img src="data:image/png;base64,{{ .Content | base64Encode }}" alt="PlantUML Diagram" />
    </div>
  {{ else }}
    <div class="error">Unexpected content type: {{ $contentType }}</div>
  {{ end }}
{{ else }}
  <div class="error">Failed to fetch PlantUML diagram</div>
{{ end }}
```

This allows the PlantUML API end point to be configurable via site params. The shortcode, when rendered uses `resources.GetRemote` to POST the contents of the shortcode invocation to the PlantUML API. It then renders the returned SVG directly, or adds an `img` tag to render PNG images. 

For example, the following declarion:

```
{{</* plantuml */>}}
@startuml
skinparam svgDimensionStyle false
skinparam BackgroundColor transparent
skinparam SequenceBoxBackgroundColor transparent
pparticipant Participant as Foo
actor       Actor       as Foo1
boundary    Boundary    as Foo2
control     Control     as Foo3
entity      Entity      as Foo4
database    Database    as Foo5
collections Collections as Foo6
queue       Queue       as Foo7
Foo -> Foo1 : To actor 
Foo -> Foo2 : To boundary
Foo -> Foo3 : To control
Foo -> Foo4 : To entity
Foo -> Foo5 : To database
Foo -> Foo6 : To collections
Foo -> Foo7: To queue
@enduml
{{</* /plantuml */>}}
```

will render:
{{< plantuml>}}
@startuml
skinparam svgDimensionStyle false
skinparam BackgroundColor transparent
skinparam SequenceBoxBackgroundColor transparent
participant Participant as Foo
actor       Actor       as Foo1
boundary    Boundary    as Foo2
control     Control     as Foo3
entity      Entity      as Foo4
database    Database    as Foo5
collections Collections as Foo6
queue       Queue       as Foo7
Foo -> Foo1 : To actor 
Foo -> Foo2 : To boundary
Foo -> Foo3 : To control
Foo -> Foo4 : To entity
Foo -> Foo5 : To database
Foo -> Foo6 : To collections
Foo -> Foo7: To queue
@enduml
{{< /plantuml >}}

(This is an SVG rendered at build time, using the shortcode above.)

This is how the configuration looks like:
```yaml
params:
  ...
  plantuml:
    baseUrl: http://localhost:9999/svg/
security:
  enableInlineShortcodes: true
  http:
    methods:
    - POST
    urls:
      - ^http://localhost:9999/svg/*
```

It is important to note that the `skinparam svgDimensionStyle false` is here to ensure that the SVG produced doesn't include `width` and `height` attributes [^16]. This allows finer control on how the SVG is displayed, especially on narrower screens, with CSS that would look like this:

```css
svg {
  margin-top: 20px;
  width: 100%;
  height: auto;
  display: block;
}
```

My configuration points to a local PlantUML server.

```shell
docker run -d -p 9999:8080 plantuml/plantuml-server:jetty
```

In theory, you can point to the public PlantUML server. [^15]

My preference is to use the SVG end point. The shortcode can be easily modified to always produce PNGs. Compared to the other approaches, this removes the need for any pre-processing, doesn't need to host a PlantUML server that the page can call from a browser, and the need to maintain a fork of Hugo.

[^1]: [Hugo - The world’s fastest framework for building websites](https://gohugo.io/)
[^2]: [PlantUML is a highly versatile tool that facilitates the rapid and straightforward creation of a wide array of diagrams.](https://plantuml.com/)
[^3]: [Add support for generating figures and diagrams #7765](https://github.com/gohugoio/hugo/issues/7765) 
[^4]: [Hugo Security model](https://gohugo.io/about/security/)
[^5]: [Quick Start Guide to PlantUML](https://plantuml.com/starting)
[^6]: [Discourse -  Executing a shell command in a shortcode](https://discourse.gohugo.io/t/executing-a-shell-command-in-a-shortcode/25109/6)
[^7]: [Paul Dugas - Hugo Shortcode for PlantUML](https://paul.dugas.cc/post/plantuml-shortcode/)
[^8]: [Hugo uses goldmark, a Markdown parser written in Go](https://github.com/yuin/goldmark)
[^9]: [PR - Add PlantUML rendering support -- post-hugo processing #8398](https://github.com/gohugoio/hugo/issues/8398)
[^10]: [Comment on PR #8398](https://github.com/gohugoio/hugo/issues/8398#issuecomment-1003144518)
[^11]: [The Edge of Random - Adding PlantUML support to Hugo](https://eyjhb.dk/blog/adding-plantuml-support-to-hugo/)
[^12]: [Shorcodes are shorthands that can render content](https://gohugo.io/content-management/shortcodes/)
[^13]: [Functions - resources.GetRemote](https://gohugo.io/functions/resources/getremote/)
[^14]: [Configuration - Security](https://gohugo.io/configuration/security/)
[^15]: [PlantUML Online Server](https://www.plantuml.com/plantuml)
[^16]: [PlantUML SVG](https://plantuml.com/svg)
