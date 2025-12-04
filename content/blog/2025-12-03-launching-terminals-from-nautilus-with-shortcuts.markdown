---
title: Launching Terminals from Nautilus with Shortcuts
date: 2025-12-03T22:00:23-08:00
tags:
  - gnome
  - nautilus
---
This is a blog post about how to set up Nautilus [^1] to launch any chosen Terminal emulator for the currently open directory. It was inspired by [this comment](https://news.ycombinator.com/item?id=46139007) about missing features in Ghostty [^2].

By default Nautilus has a context menu entry that launches the default GNOME Terminal at the open directory. There are two missing pieces here - one is that the action needs to be invoked from the context menu with a mouse click, and the second is that it will only launch the default GNOME Terminal.

Nautilus for a long time has supported an extension framework [^3] that makes it possible to add context menus with rich functionality. And a lot of popular terminal applications do provide extensions that use `python-nautilus` - here is [WezTerm's](https://github.com/wezterm/wezterm/blob/4634946d23082e38f9abf0f10c6e1fa08303d9ed/assets/wezterm-nautilus.py) [^6] and Ghostty's [is here](https://github.com/ghostty-org/ghostty/blob/c97205161155c227cd4102e050e16933ec7e806f/dist/linux/ghostty_nautilus.py). They solve the problem of being able to launch the desired Terminal emulator. However, they do not provide key bindings due to inherent limitations of the `python-nautilus` framework [^4].

In order to use shortcuts, Nautilus `scripts` [^5] can be used. Scripts generally go in `~/.local/share/nautilus/scripts/` and can be any executable. For example, in order to launch `WezTerm`, I have this script:

```shell
> cat ~/.local/share/nautilus/scripts/WezTerm

#!/usr/bin/env bash

exec wezterm start --cwd $(pwd)
```


Similarly, a script that can launch Ghostty would look like this:

```shell
>cat ~/.local/share/nautilus/scripts/Ghostty

#!/usr/bin/env bash

ghostty --working-directory=$(pwd)
```

These scripts will show up in Nautilus when it is restarted, after `nautilus -q`.

{{< figure src="/nautilus-scripts.gif" alt="Nautilus scripts show up in context menu" caption="Nautilus scripts launches WezTerm in the right directory" >}}

Keybindings are defined in `~/.config/nautilus/scripts-accels`.

```shell
> cat ~/.config/nautilus/scripts-accels

<Ctrl><Shift>w WezTerm
<Ctrl><Shift>F4 Ghostty
```

{{< figure src="/nautilus-scripts-shortcut.gif" alt="Shortcuts are displayed and works" caption="Script can be launched from Context menu _and_ Shortcut" >}}

This was a fun feature to figure out, even though launching terminals from Nautilus is not part of my workflow.

[^1]: [Nautilus](https://apps.gnome.org/Nautilus/) is GNOME's default File manager.
[^2]: [Ghostty](https://ghostty.org/) is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.
[^3]: [Nautilus-python](https://gitlab.gnome.org/GNOME/nautilus-python) allows extending Nautilus with Python scripts with the help of Nautilus’s GObject API.
[^4]: The Nautilus extensions framework provides hooks for four capabilities - [Context Menu](https://gnome.pages.gitlab.gnome.org/nautilus-python/class-nautilus-python-menu-provider.html), [File Info](https://gnome.pages.gitlab.gnome.org/nautilus-python/class-nautilus-python-info-provider.html), [Columns in List view](https://gnome.pages.gitlab.gnome.org/nautilus-python/class-nautilus-python-column-provider.html) and [Custom properties](https://gnome.pages.gitlab.gnome.org/nautilus-python/class-nautilus-python-properties-model-provider.html).
[^5]: Ubuntu official documentation - [NautilusScriptsHowto](https://help.ubuntu.com/community/NautilusScriptsHowto)
[^6]: [WezTerm](https://wezterm.org/index.html) is a powerful cross-platform terminal emulator and multiplexer.
