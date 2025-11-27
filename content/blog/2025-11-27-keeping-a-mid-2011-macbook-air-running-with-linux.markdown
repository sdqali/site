---
title: "Keeping a Mid-2011 MacBook Air Running With Linux"
date: 2025-11-27T08:05:17-08:00
tags:
  - macbook
  - linux
---
I have a 2011 vintage MacBook Air that has not seen much usage. I purchased it from a previous employer's auction of used computers. It did just enough things - browsing, watching videos, working on documents, and writing some code in a pinch. Somewhere along the way, the battery stopped holding a charge and the MacBook became tethered to a power cable. This led me to replacing the battery, following tools, replacement battery and excellent instructions from iFixit[^1].

<!--more-->

While that repair breathed new life in to it, running High Sierra on it was still a slow experience. So, it ended up being left to collect dust, and I began using my Linux Desktop a lot more. We planned to buy a new MacBook this year, and while waiting to figure that out, I decided to see if running a more lightweight OS on the old MacBook Air would render it more useful.

## Specifications

```
- **Hardware Model:**                              Apple Inc. MacBookAir4,2
- **Memory:**                                      4.0 GiB
- **Processor:**                                   Intel® Core™ i7-2677M × 4
- **Graphics:**                                    Intel® HD Graphics 3000 (SNB GT2)
- **Disk Capacity:**                               251.0 GB
```

Searches about installing Linux on old MacBook Airs always seems to turn up with Linux Mint as the winner. People rate it highly for being more lightweight than Ubuntu, while retaining support for most drivers. There were plenty of warnings about Wi-Fi not working out of the box and the need to install drivers for the Wi-Fi device through Internet over Bluetooth pairing to a Phone.

## Installation

I decided to install Linux Mint Mate, which came with a reputation for being more lightweight than the Cinnamon version. The installation was pretty smooth and I was able to connect to Wi-Fi, even on the Live installer, without needing to install drivers.

## Out of the box experience

- Wi-Fi worked out of the box, to my pleasant surprise.
- Bluetooth works, although playing Audio through Bluetooth is still a nightmare, as it is on my other Linux desktops. [^2]
- Audio, brightness, keyboard backlight controls worked out of the box, although I had to modify Function key behavior, as described later in this post.

## Things that needed tweaking

### Key bindings
I have, over the years become so used to Mac keybindings that I set all my Linux desktops to use the same keybindings. I typically use `kinto.sh` [^3] for this, even though it is not perfect [^4]. It turned out that I simply couldn't get it working on Linux Mint Mate, no matter how much Python venv wrangling I did. I have used `gnome-macos-remap-wayland` [^5] before when running Wayland, so I decided to switch to Gnome desktop instead of Mate. The default installation of `gnome-macos-remap-wayland` didn't start on login, and I ended up with this Systemd entry that worked:

```systemd
; /etc/systemd/system/default.target.wants/gnome-macos-remap.service
[Unit]
Description=GNOME -> macOS Remap

[Service]
Type=simple
Restart=on-failure
RestartSec=10
ExecStart=xremap /etc/gnome-macos-remap/config.yml

[Install]
WantedBy=default.target
```

### Start-up Chime
I needed a way to turn off the loud Startup Chime at boot time. After trying various approaches, I found something that just works[^6].

```shell
sudo su

sudo chattr -i /sys/firmware/efi/efivars/SystemAudioVolume-7c436110-ab2a-4bbb-a880-fe41995c9f82

sudo printf "\x07\x00\x00\x00\x00" > /sys/firmware/efi/efivars/SystemAudioVolume-7c436110-ab2a-4bbb-a880-fe41995c9f82

sudo chattr +i /sys/firmware/efi/efivars/SystemAudioVolume-7c436110-ab2a-4bbb-a880-fe41995c9f82
```

### Function Key
I want to be able to use the Function keys as plain Function keys by default. I was able to get that working by modifying the `hid_apple` module parameters[^7]:

```shell
echo options hid_apple fnmode=2 | sudo tee -a /etc/modprobe.d/hid_apple.conf

sudo update-initramfs -u -k all
```

## Overall Impressions

Linux Mint feels snappier than High Sierra, and I am able to run Firefox and Neovim simultaneously - without the fans beginning to sound like jet engines. I rate the overall experience 4.5 out of 5. The MacBook not ending up as e-waste is a pretty good win.


[^1]: iFixit - [MacBook Air 13" Mid 2011 Repair](https://www.ifixit.com/Device/MacBook_Air_13%22_Mid_2011)
[^2]: I have spent countess hours trying to get this fixed, to no avail. The choppy audio issue is seen with PulseAudio as well as [Pipewire](https://bugs.launchpad.net/ubuntu/+source/pipewire/+bug/2063150).
[^3]: [kinto.sh](https://kinto.sh/) is nifty and it has worked well in the past for me.
[^4]: Terminal emulators on Linux need extra configuration for keybindings, and they almost always end up creating conflicts - `kinto.sh` works by mapping `Command` to `Ctrl` and `Ctrl` is far too pivotal in Terminals.
[^5]: [gnome-macos-remap-wayland](https://github.com/petrstepanov/gnome-macos-remap-wayland) is like `kinto.sh`, but works in Wayland.
[^6]: For some time, it looked like the only way to do this was to enter macOS's Internet Recovery option, enter the macOS Terminal and make changes, since I was not dual booting and had wiped the macOS volume. Eventually, I found this [approach that works from Linux](https://gist.github.com/0xbb/ae298e2798e1c06d0753?permalink_comment_id=4296049#gistcomment-4296049).
[^7]: Linux Mint Forums - [[SOLVED] MacBook fn keys](https://forums.linuxmint.com/viewtopic.php?t=417982)
