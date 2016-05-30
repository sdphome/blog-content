Title: 一句话介绍openstack的每个组件
Date: 2016-05-30 16:28
Tags: openstack

openstack使用模块化设计，正是由于这样的设计使得openstack可以有许多动态的模块。下面用一句话来简单概括openstack的每个模块的功能。

> Dashboard

Openstack的Dashboard是基于OpenStack各个组件开发的web管理后台，它是一个网络接口组件。

> Keystone

Keystone是openstack的身份认证/管理组件，它管理着tenants, users, roles, endpoints和一个services的列表。tenant是一个object的群组，users, instances, network都是一个object。users管理着一个role。

> Glance

Glance是openstack的镜像管理组件，提供虚拟机镜像的发现，注册，取得服务。

> Neutron

Neutron是openstack的网络管理组件，为openstack提供虚拟网络支持。

> Nova

Nova是openstack的实例管理组件，它需要image, network, key pair, security group的支持才可以启动。

> Cinder

Cinder是openstack的块存储组件，能够为instance创建卷并与instance绑定，它还提供了硬盘的snapshot的功能。

> Swift

Swift是openstack的对象存储组件，为运行上下文提供服务。

> Ceilometer

Ceilometer是openstack的统计组件，他能够收集openstack中的资源使用情况，可以用来警示资源额度。

> Heat

Heat是openstack的协作组件，它能够自动的创建多个计算实例，并让他们一起协同工作。Head还可以与AWS CloundFormation兼容。


参考资料：
1. [openstack Essentials][1]


[1]: https://www.packtpub.com/virtualization-and-cloud/openstack-essentials
