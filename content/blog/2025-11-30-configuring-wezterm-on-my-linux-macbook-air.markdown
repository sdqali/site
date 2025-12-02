---
title: Configuring WezTerm on my Linux MacBook Air
date: 2025-11-30T15:08:03-08:00
tags:
  - macbook
  - wezterm
  - xremap
ghissueid: 153
bbissueid: 146
---
After setting up Linux on the [MacBook Air](/blog/2025/11/27/keeping-a-mid-2011-macbook-air-running-with-linux/) as we discussed in the last blog post, the next item to sort out was making sure that the keyboard shortcuts that I have always used continue to work. Since the macOS key bindings I set up using `gnome-macos-remap-wayland` had special configurations in place to handle `Ctrl+` shortcuts in Gnome Terminal [^1], that is where I started. It became apparent that configuring Gnome Terminal to handle all the shortcuts is too painful and I decided to switch to WezTerm [^2] instead.

## Configuring xremap for WezTerm

The first configuration changes were needed to be made for `xremap`. Since `Ctrl` and `Super` had been switched, in order to send Terminal commands with `Ctrl` correctly, the configuration had to include the following.

```yaml
  - name: Terminal
    application:
      only: org.wezfurlong.wezterm
    remap:
      Super-W: Ctrl-W
      Super-E: Ctrl-E
      Super-E: Ctrl-R
      Super-T: Ctrl-T
      Super-Y: Ctrl-Y
      Super-U: Ctrl-U
      Super-O: Ctrl-O
      Super-P: Ctrl-P
      Super-A: Ctrl-A
      Super-S: Ctrl-S
      Super-F: Ctrl-F
      Super-G: Ctrl-G
      Super-H: Ctrl-H
      Super-J: Ctrl-J
      Super-K: Ctrl-K
      Super-L: Ctrl-L
      Super-Z: Ctrl-Z
      Super-X: Ctrl-X
      Super-V: Ctrl-V
      Super-B: Ctrl-B
      Super-N: Ctrl-N
      Super-KEY_SLASH: Ctrl-KEY_SLASH
```

The next part configures `Super` (now mapped to `Ctrl`) to be used for non Terminal commands.
```yaml
  - name: Console shortcuts
    application:
      only: org.wezfurlong.wezterm
    remap:
      Ctrl-C: Ctrl-Shift-C # Copy text
      Ctrl-V: Ctrl-Shift-V # Paste text
      Ctrl-N: Ctrl-Shift-N # New window
      Ctrl-Q: Ctrl-Shift-Q # Close window
      Ctrl-T: Ctrl-Shift-T # New tab
      Ctrl-W: Ctrl-Shift-W # Close tab
      Ctrl-F: Shift-Ctrl-F # Find
      Ctrl-KEY_RIGHTBRACE: Super-KEY_RIGHTBRACE #Previous Tab
      Ctrl-KEY_LEFTBRACE: Super-KEY_LEFTBRACE # Next Tab
```

## Numbered Tab Navigation

I use `Super+<number>` to switch to Console tab numbered `<number>`. This can be configured with WezTerm's `ActivateTab` action.

```lua
for i = 1, 9 do
	table.insert(config.keys, {
		key = tostring(i),
		mods = "CTRL",
		action = wezterm.action.ActivateTab(i - 1),
	})
end
```

Note the use of `CTRL` as the modifier to accommodate `xremap` sending `Super` as `Ctrl`.

## Undo Operation

For as long as I have used Terminal emulators, I have always used Emacs key bindings, and `Ctrl+_` has always been `Undo` for me. It turns out WezTerm uses `Ctrl+_` to decrease font size. The only way to overcome this seems to be to prevent WezTerm's default action for this key combination and force it to send it to the Shell.

```lua
config.keys = {
  -- 
	{
		key = "_",
		mods = "CTRL|SHIFT",
		action = wezterm.action.DisableDefaultAssignment,
	},
  --
}
```

## Delete Word Backwards

Following Emacs key bindings, `M-backspace` has been `Delete a Word backwards` for me [^4]. WezTerm has no documented Action to delete a word backwards, and the recommendation from the community is to send a different key combination to the target when this combination is invoked [^3]. It turns out that `Option+Delete` on the MacBook keypad is not really sending `Alt+Backspace`, so attempts with this configuration did not result in the behavior I wanted.

```lua
config.keys = {
  --
	{
		key = "Backspace",
		mods = "ALT",
		action = wezterm.action.SendKey({
			key = "w",
			mods = "CTRL",
		}),
	},
  --
}
```

However, this does the trick.

```lua
config.keys = {
  --
	{
		key = "Backspace",
		mods = "CTRL",
		action = wezterm.action.SendKey({
			key = "w",
			mods = "CTRL",
		}),
	},
  --
}

```
The full configuration is available [here](https://github.com/sdqali/dot-config/blob/main/wezterm/wezterm.lua).

[^1]: Gnome Terminal is the [default](https://apps.gnome.org/Console/) terminal emulator shipped with Gnome.
[^2]: [WezTerm](https://wezterm.org/) is a cross-platform Terminal emulator written in Rust, with a Lua configuration DSL.
[^3]: WezTerm GitHub Issues - [How do I get Ctrl-Backspace to delete a word? #3983](https://github.com/wezterm/wezterm/discussions/3983)
[^4]: Emacs Manual - [Words](https://www.gnu.org/software/emacs/manual/html_node/emacs/Words.html)
