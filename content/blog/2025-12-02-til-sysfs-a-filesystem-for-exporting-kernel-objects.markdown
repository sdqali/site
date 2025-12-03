---
title: "TIL: sysfs - a filesystem for exporting kernel objects"
date: 2025-12-02T21:24:46-08:00
tags:
  - linux
---
While tweaking kernel parameters on the [MacBook running Linux](/blog/2025/11/27/keeping-a-mid-2011-macbook-air-running-with-linux/), I learned about `sysfs` [^1]- a filesystem that provides access to the kernel data. That blog post described how startup chimes can be modified by setting UEFI parameters by using the `efivarfs` filesystem [^2], which was created as a improvement over `sysfs` for storing UEFI parameters.

Looking at the `hid_apple` module [^3], it's state is available at `/sys/module/hid_apple/`

```shell
> tree /sys/module/hid_apple/

/sys/module/hid_apple/
├── coresize
├── drivers
│   └── hid:apple -> ../../../bus/hid/drivers/apple
├── holders
├── initsize
├── initstate
├── notes
├── parameters
│   ├── fnmode
│   ├── iso_layout
│   ├── swap_ctrl_cmd
│   ├── swap_fn_leftctrl
│   └── swap_opt_cmd
├── refcnt
├── sections
│   ├── __dyndbg
│   ├── __jump_table
│   ├── __mcount_loc
│   ├── __param
│   └── __patchable_function_entries
├── srcversion
├── taint
└── uevent
```

Parameters set for this module are available under `parameters`:

```shell
> for f in /sys/module/hid_apple/parameters/*; do  echo $f; cat $f; done

/sys/module/hid_apple/parameters/fnmode
2
/sys/module/hid_apple/parameters/iso_layout
-1
/sys/module/hid_apple/parameters/swap_ctrl_cmd
0
/sys/module/hid_apple/parameters/swap_fn_leftctrl
0
/sys/module/hid_apple/parameters/swap_opt_cmd
0
```

Specifically, the [parameter](https://github.com/torvalds/linux/blob/master/drivers/hid/hid-apple.c#L58) that was set to use Function keys as pure Function keys is at `/sys/module/hid_apple/parameters/fnmode`.

```shell
> cat /sys/module/hid_apple/parameters/fnmode

2
```

We can modify `fnmode` by writing to this file as if it were a regular file:

```shell
> echo 1 | sudo tee /sys/module/hid_apple/parameters/fnmode

> cat /sys/module/hid_apple/parameters/fnmode
1
```

This immediately changes the behavior of the `Function` keys. However, this is temporary, as a reboot will cause the kernel to use values from `/etc/modprobe.d/hid_apple.conf`.

```shell
> cat /etc/modprobe.d/hid_apple.conf

options hid_apple fnmode=2
```

[^1]: [sysfs](https://docs.kernel.org/filesystems/sysfs.html) - _The_ filesystem for exporting kernel objects.
[^2]: [efivarfs](https://docs.kernel.org/filesystems/efivarfs.html) - a (U)EFI variable filesystem.
[^3]: [hid_apple](https://github.com/torvalds/linux/blob/master/drivers/hid/hid-apple.c) is the module that provides support for Apple input devices like the keyboard and trackpad.
