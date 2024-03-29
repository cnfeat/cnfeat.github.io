---
title: 老白小黑固态硬盘升级记
layout: default
tags: [固态硬盘,知识管理]
pinned: false
blog_post: true
---

笔记本用了一年多，开机越来越慢，开个markdownpad写东西都要等十几秒，一来打算重装，二来早就听说是固态硬盘是可以相见恨晚增加幸福感的东西，所以干脆在国庆时候入手了两块固态硬盘。

一块是Intel的复刻版520，淘宝价398，120G，来自深圳华强北。
![](http://cnfeat.qiniudn.com/DSC00449_100914_093116_PM.jpg)

这一块是给Claire的老白用的，Claire的老白是联想F41珠穆朗玛峰奥运纪念版，2008年买的，当时据说用了七八千，以前用这部机看视频居然会突然死机，上网一查，发现这货用的硬盘是5400转的，初以为是硬盘转的厉害，所以想着换个硬盘。

![](http://cnfeat.qiniudn.com/DSC00444.JPG)

你看看，一代小白变老白。

此前在网上看过无数这样的帖子，笔记本换块硬盘应该很容易，但是上论坛一查，这部已经退市近六年的机子却没有我想象中简单。

首先，这部机子没有开启AHCI的开关，需要软解；其次，老白F41出过无数系列，而老白的CPU是最低端的2230，论坛上的高手说，如果老白要升级，一定要升CPU，而升CPU之前又一定要升BIOS。

>P.S.IT168真是神论坛，老白居然还有子版块，重要的是，版主还十分活跃，十分难得，多年前注册的账号还能用。

搞清楚短板就好办了，马上找攻略，升BIOS，软解AHCI（说起来两句话，却折腾了大半天），随后上淘宝找CPU，五六年前七八百块钱的CPU如今八十六块钱就搞到了，摩尔定律可真不是盖的。

![](http://cnfeat.qiniudn.com/1868066136.jpg)

以前的CPU是2230，淘宝回来的CPU是8330，性能飞跃三倍多。

第一次拆笔记本电脑，当时心情还是有点小激动和紧张，不过一想老白都是六年的机子了，坏了也不可惜，顶多出事拿去修修，最坏的预算就是修不了买一部新的，不过幸好，装上去之后，大家喜闻乐见的情况没有出现，一次点亮，系统运作速度与之前相比简直是天壤之别。

接着就是重头戏：拆换硬盘，有了之前的经验之后，拆换硬盘就淡定多了，首先拆开后盖，拿出机械硬盘。

![](http://cnfeat.qiniudn.com/DSC00457.JPG)

再装上固态硬盘。

![](http://cnfeat.qiniudn.com/DSC00458.JPG)

最后装上后盖，搞掂。

有人问，那之前的机械硬盘怎么办？

原来的机械硬盘只有160G，现在的固态有120G，对老白来讲已经够用，干脆在京东买了一个硬盘盒子，将笔记本的机械硬盘放进去，刚好可以当作一个移动硬盘。

从经济成本考虑，光驱托架需要四十多块钱，而一个硬盘盒子只需要29块，装进笔记本里面实在划不来。

![](http://cnfeat.qiniudn.com/348360792.jpg)

还有人问，固态硬盘是空的，你怎么启动？

同学，先用U盘制作一个老毛桃的启动盘，然后分区，接着安装系统，难道你这样都不懂？这样都不懂妹子怎么找你修电脑。

P.S.我家妹子就是修电脑找回来的。

第二块固态硬盘是闪迪极速128G（实际上是120G），天猫459块搞掂。

![](http://cnfeat.qiniudn.com/DSC00463.JPG)

有了老白开路之后，小黑的安装就顺畅很多了。

>小黑的设计还真是人性化。

打开盖子，拉出硬盘。

![](http://cnfeat.qiniudn.com/DSC00469.JPG)

装上硬盘，合上盖子。

![](http://cnfeat.qiniudn.com/DSC00471.JPG)

塞个系统进去。

![](http://cnfeat.qiniudn.com/DSC00474.JPG)

P.S.这个系统有4.63G，是传说中的纯净完整版。

然后就搞掂了吗？当然没有，我还在淘宝买了一个光驱盒子和光驱硬盘托架，花了65块。这两个东西有什么用？是这样的，我小黑的硬盘有500G，这个硬盘当然不能拿当移动硬盘，这是是要继续放在电脑中当作第二硬盘使用的，可是电脑中的位置已经满了，怎么办？只能将光驱拆出来，将硬盘塞进去，可是硬盘不能硬塞进去，只能用个光驱硬盘托架将硬盘放进去，而拆出来的光驱再用光驱盒子装起来，当作移动光驱。

这部分我没有没有拍照，因为我忘记了，为什么呢？

因为我将机械硬盘放进去的时候，电脑老是启动机械硬盘的系统，慢得要死，于是我尝试改BIOS，取消机械硬盘的活动区和临时改启动盘，都失败了，搞得我心烦意乱，最后实在没有法子，出大招，进PE系统将机械硬盘的系统盘给格式化了，连系统都没有了我看你还怎么进去，删了系统之后，机子终于顺利地从固态硬盘启动了。

装完系统，搞个360，打完补丁，启动时间15秒。

来个总结：固态硬盘启动Office几乎秒开，天天对着电脑的同学们，对自己好一点，现在固态3块钱1G，价格还算可以，真心可以入。


----

如果你从此文得到收获，请订阅微信公众号「cnfeat」，你一定会获得更多。

（题图：October 2014 Blood Moon by Mike Mezeul II）

点击「阅读原文」到我的博客查看[历史文章存档](http://cnfeat.com)。

![](http://cnfeat.qiniudn.com/signitrue-2014-09-28.jpg)

**【一期一会】**

在后台收到了不少读者的建议，智慧的力量还是无穷的，感谢大家。








