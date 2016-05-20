Title: sudoers文件属性为777后无法使用root
Date: 2014-06-23 18:26:01
Update: 2016-05-20 14:39:02
Tags: root, ubuntu, sudoers

## 问题形成原因

在使用ubuntu时有时为了添加root权限，需要将用户信息添加进`/etc/sudoers`，有些人为了方便，将这个文件的权限修改为777了，接着发现sudo的时候想使用root权限不可以了..


## 解决方法

重启机器，在开机的过程中长按`shift`键，使ubuntu进入grub mode，进入root shell，在root shell中输入下面两条命令即可:

    mount -o rw,remount /
    chmod 440 /etc/sudoers
