---
title: "Docker + K8s Workshop - chroot example"
date: 2020-03-02T19:53:43-08:00
---

## Create a chroot jail

```
mkdir jail
```

## Create directories for system binaries

```
mkdir jail/bin
```

## Copy the bash binary from the host

```
cp -v /bin/bash jail/bin
```

## Create a list of libraries needed for the binary to work

```
list_of_libs="$(ldd /bin/bash | egrep -o '/lib.*\.[0-9]')"
echo $list_of_libs
```

## Copy the libraries recursively

```
for i in $list_of_libs; do cp  -v --parents "$i" `pwd`/jail; done
```

## Create a demo script

```
#!/bin/bash

let i=0;
while :
do
        let i++
        echo "Last value of i is ${i}"
        read -rep $'Pausing for 5 seconds\n' -t 5
done
```

## Copy the demo script to the jail

```
chmod +x demos.sh
cp demo.sh jail/
```

## Enter the chroot

```
sudo chroot `pwd`/jail /bin/bash
```

## In the chroot, execute the shell script

```
./demo.sh
```
