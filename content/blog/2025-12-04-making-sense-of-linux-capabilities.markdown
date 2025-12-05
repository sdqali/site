---
title: Making sense of Linux capabilities
date: 2025-12-04T18:57:03-08:00
draft: true
---
In this blog post, we will explore Linux capabilities, which is a way to ensure that processes and executables have just enough rights to perform the actions they are deemed safe to perform, without giving them _carte blanche_ to anything and everything by running as the `root` user.

{{< toc >}}


## Basic Privilege model
To state the basics - the classic Unix model of privilege is built around the concept of granting a `super user` (via their UID) the right to do pretty much anything - read and modify any data, open connections etc. This root user typically has the `UID` set to `0`. 

Non-root users execute commands as `root` when required using the utilities `sudo` or `sudo su`. And in special cases, like changing a user's password, they leverage the `setuid` bit on programs like `passwd`. The `setuid` bit permits the program to run as the effective owner of the program, regardless of who invokes it. Since the owner of `passwd` is `root`, any user executing `passwd` is effectively running it as `root`.

```shell
>ls -la `which passwd`

-rwsr-xr-x 1 root root 64152 May 30  2024 /usr/bin/passwd
```

Notice how the file is owned by `root`, but the `setuid` bit is set.

Alternatively, some programs have the `setgid` bit set, which permits the program to run with the privileges of the group that owns the file. For example:

```shell
> ls -la `which ssh-agent`

-rwxr-sr-x 1 root _ssh 309688 Aug 26 06:49 /usr/bin/ssh-agent
```

What happens when a user wants to execute a binary that they trust to do certain things, but not other things - like a binary they downloaded from the Internet? If they run as `root`, the binary in question can execute every privileged action it wants to - including performing `rm -rf /`.

## Evolution of Capabilities

`Capabilities` is a system designed to overcome these shortcomings by decomposing the privileged actions to separate buckets, such that programs could be permitted to execute certain privileged actions, but not others.

### POSIX Standards 1003.1e and 1003.2c
The nucleus of what ended up becoming Linux Capabilities appear to have first appeared in the two proposed IEEE POSIX Standards `1003.1e` and `1003.2c` [^2].

{{< details summary="Capabilities proposed in the POSIX 1e Standards" >}}
- CAP_ADMIN
- CAP_AUDIT_CONTROL
- CAP_AUDIT_WRITE
- CAP_CHOWN
- CAP_CLEAR
- CAP_DAC_EXECUTE
- CAP_DAC_OVERRIDE
- CAP_DAC_READ
- CAP_DAC_READ_SEARCH
- CAP_DAC_SEARCH
- CAP_DAC_WRITE
- CAP_EFFECTIVE
- CAP_FOWNER
- CAP_FSETID
- CAP_INF_NOFLOAT_OBJ
- CAP_INF_NOFLOAT_SUBJ
- CAP_INF_RELABEL_OBJ
- CAP_INF_RELABEL_SUBJ
- CAP_INHERITABLE
- CAP_KILL
- CAP_LINK_DIR
- CAP_MAC_DOWNGRADE
- CAP_MAC_LOCK
- CAP_MAC_READ
- CAP_MAC_RELABEL_SUBJ
- CAP_MAC_UPGRADE
- CAP_MAC_WRITE
- CAP_PERMITTED
- CAP_SET
- CAP_SETFCAP
- CAP_SETGID
- CAP_SETUID
{{< /details >}}

#### Capability Sets

The POSIX proposal included the concept of Capability sets, for both Files and Processes. These define how Files and Processes get assigned Capabilities and.

##### Process Capability Sets
- The `effective` set contains Capabilities that is currently active for the process. The process can drop a Capability any time it wants.
- The `permitted` set contains Capabilities that a process could activate, thereby making it `effective`. At any point, the process can acquire any Capability in the `permitted` list.
- The `inheritable` flag on a process determines if a Process may grant it's successor process the Capabilities the former has.

##### File Capability Sets
- The `effective` set contains Capabilities that the process launched by executing the application will have in it's `effective` set.
- The `permitted` set contains Capabilities that the process launched by executing the program may use, thereby making it `effective`.
- The `inheritable` set contains Capabilities that the process launched by executing the program may choose to use from the Capabilities it's parent process passed to it and the process may pass to child processes.


### Linux-Privs

Even though these POSIX Standards were proposed and then withdrawn, this effort inspired the `Linux-Privs` proposal [^5]. This specification lists Capabilities that are specific to Linux that are not part of the POSIX proposal.

{{< details summary="Linux-specific Capabilities proposed in Linux-Privs" >}}
- CAP_LINUX_IMMUTABLE - _Allow modification of S_IMMUTABLE and S_APPEND file attributes._
- CAP_LINUX_KERNELD - _Permission to act as kerneld._
- CAP_LINUX_INSMOD - _Allow installation of kernel modules._
- CAP_LINUX_RMMOD - _Allow removal of kernel modules._
- CAP_LINUX_RAWIO - _Allow ioperm/iopl access._
- CAP_LINUX_ATTENTION - _Allow configuration of the secure attention key._
- CAP_LINUX_RANDOM - _Allow administration of the random device._
{{< /details >}}

The proposal also lists Capabilities present in other systems that are not part of the POSIX proposal or the Linux-Privs proposal.

{{< details summary="Capabilities found in other systems" >}}
CAP_NET_BIND_SERVICE - _Allows binding to TCP/UDP sockets below 1024._
CAP_NET_BROADCAST - _Allow broadcasting._
CAP_NET_DEBUG - _Allow setting debug option on sockets._
CAP_NET_FIREWALL - _Allow configuring of firewall stuff._
CAP_NET_IFCONFIG - _Allow interface configuration._
CAP_NET_PACKET - _Allow use of PACKET sockets._
CAP_NET_RAW - _Allow use of RAW sockets._
CAP_NET_ROUTE - _Allow modification of routing tables._
CAP_NET_SETID - _CAP.FIXME: what is this about?._
CAP_IPC_LOCK - _Allow locking of segments in memory._
CAP_IPC_OWNER - _Override IPC ownership checks._
CAP_SYS_CHROOT - _Allow use of chroot()._
CAP_SYS_PTRACE - _Allow ptrace() of any process._
CAP_SYS_ACCOUNT - _Allow configuration of process accounting._
CAP_SYS_ADMIN - _System Admin functions: mount et al._
CAP_SYS_BOOT - _Allow use of reboot()._
CAP_SYS_DEVICES - _Allow device administration._
CAP_SYS_NICE - _Allow use of renice() on others, and raising of priority._
CAP_SYS_RESOURCE - _Override resource limits._
CAP_SYS_TIME - _Allow manipulation of system clock._
CAP_SYS_TTY_CONFIG - _Allow configuration of tty devices._
CAP_SYS_QUOTA - _Allow examination and configuration of disk quotas._
{{< /details >}}

There are some interesting things to note here:
- This entry was never corrected `CAP_NET_SETID - CAP.FIXME: what is this about?`. This appears to be a typo.
- Some of the capabilities noted in other systems eventually made it in to Linux, for example `CAP_NET_BIND_SERVICE` and `CAP_NET_RAW`.

#### Capability Sets

Linux-Privs took the Capability Sets idea from the POSIX proposals and defined how Process Capabilities would be computed from the parent's Process Capabilities and the File's Capabilities.

- `effective` - pE' = pP' & fE _i.e._ the new effective set is the new permitted set masked with the executed file's effective set.
- `inheritable` - pI' = pI _i.e._ inheritable set is passed unchanged.
- `permitted` - pP' = fP | ( fI & pI ) _i.e._ the permitted set becomes the combination of the permitted set of the executed file and those inheritable capabilities of the executing file that are also inheritable by the file.

It was first proposed in the Linux mailing lists in 1998 [^6], with the first implementation releasing in Kernel version `2.2.11` [^3] [^4]. At this point, Capabilities were configurable only on Processes and not Files, using `libcap`'s `capsh` utility or using the syscalls `capset()` and `capget()`.


systemd - https://0pointer.de/blog/projects/security.html

[^2]: https://web.archive.org/web/20011215142012/http://wt.xpilot.org/publications/posix.1e/download.html
[^3]: https://lwn.net/1999/0408/a/caps.html
[^4]: https://static.lwn.net/1999/0408/kernel.php3
[^5]: https://www.kernel.org/pub/linux/libs/security/linux-privs/old/doc/linux-privs.html/linux-privs.html#toc1
[^6]: https://lkml.org/lkml/1998/4/19/31
[^7]: 
