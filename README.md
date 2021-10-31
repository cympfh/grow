# grow.md - Markdown Viewer

![](https://user-images.githubusercontent.com/2749629/126341872-17401668-481e-47e7-ace0-652c118968b5.png)

```bash
$ grow ~/Dropbox/scrap-markdown/ --port 8080
$ open localhost:8080
```

## Setup

Clone this, then

```bash
$ make build
```

## Markdown Compile

Compile script is written as `./bin/grow-compile`.
Default uses just `pandoc`.
Modify this if you need.

<!--

### Tagging

Write `[#tag]` in Markdown.
This will be compiled to a link `[#tag](/#tag)` (see `./bin/grow-compile`).
And `/#tag` is a tag-filtered page.

-->

### mdc

[mdc](https://github.com/cympfh/mdc) is a extended markdown.
`grow-compile` uses this if available.

