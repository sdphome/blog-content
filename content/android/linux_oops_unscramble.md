Title: oops的解读方法-----怎么通过oops查找源码行
Date: 2012-05-18 15:50:12
Tags: 汇编, oops, crash, linux

今天很郁闷的遇到了一个oops，以前碰到这类事情我就会退缩的，今天刚好没有任务，就想要不就分析一下，这个还是很重要的，我不能总是逃避这类问题啊，果断开始分析了。

先把oops亮出来给大伙看看。

>[ 230.893864] Unable to handle kernel paging request at virtual address 
9c0d5030
>[ 230.959592] pgd = 9aaf8000  
>[ 230.962313] [9c0d5030] *pgd=aa003011, *pte=00000000, *ppte=00000000  
>[ 231.001197] Internal error: Oops: 7 [#1] PREEMPT  
>[ 231.005821] last sysfs file: 
/sys/devices/platform/wakeup_event-driver/wakeup_source  
>[ 231.013571] Modules linked in: dhd(-)  
>[ 231.017270] CPU: 0 Not tainted (2.6.35.3 #1)  
>[ 231.022037] PC is at dhdsdio_htclk+0x28/0x438 [dhd]  
>[ 231.026977] LR is at dhdsdio_clkctl+0x5c/0x108 [dhd]  
>[ 231.031950] pc : [<7f012d84>] lr : [<7f013490>] psr: 20000013  
>[ 231.031956] sp : 9ae41e30 ip : 00000000 fp : 2b3408f0   
>[ 231.043450] r10: 35c61ef0 r9 : 9ae40000 r8 : 00000001  
>[ 231.048681] r7 : 00000000 r6 : 00000000 r5 : 9c096000 r4 : 9c09f000  
>[ 231.055217] r3 : 00000000 r2 : 9c0d5000 r1 : 00004329 r0 : 9c09f000  
>[ 231.061754] Flags: nzCv IRQs on FIQs on Mode SVC_32 ISA ARM Segment user  
>[ 231.068898] Control: 10c5387d Table: aaaf8019 DAC: 00000015  
>[ 231.074652] Process WifiService (pid: 2580, stack limit = 0x9ae402e8)  
>[ 231.081100] Stack: (0x9ae41e30 to 0x9ae42000)  
>[ 231.085468] 1e20: 9ae41eb4 803f17d0 20000093 80814e28  
>[ 231.093659] 1e40: 94073900 80814e28 00000001 20000013 9c1dc714 
9c09f000 00000003 00000000  
>[ 231.101850] 1e60: 9c1dc03c 00000001 9ae40000 35c61ef0 2b3408f0 
7f013490 9c09f000 00000000  
>[ 231.110042] 1e80: 9ae636c0 7f0155b0 9c09f000 00000001 9ae41e68 
00000000 9c1dc000 9c1dc0a8  
>[ 231.118234] 1ea0: 9c1df000 9c1dc03c 8004c0c4 7f00142c 9c1dc000 
7f00159c 9c09f000 9ae636c0  
>[ 231.126426] 1ec0: 7f025240 67e04660 8004c0c4 7f014638 7f025228 
9c093000 7f025240 7f01b24c  
>[ 231.134617] 1ee0: 922df400 7f02337c 922df43c 802ebcd0 922df408 
7f02337c 922df43c 802178b0  
>[ 231.142809] 1f00: 922df408 7f02337c 922df43c 80217980 7f02337c 
00000000 80846374 80216c24  
>[ 231.151000] 1f20: 7f0233b0 00000000 9ae41f44 7f01b3d0 7f0233b0 
7f01b5b0 7f0233b0 8009b1d4  
>[ 231.159191] 1f40: 00000000 00646864 00000000 9ad9f8dc 00000001 
39c2a6d3 00015e23 00000000  
>[ 231.167382] 1f60: ffffffff 00000000 00000000 39dd6b48 00000003 
00000003 39dd6c10 00000107  
>[ 231.175573] 1f80: 7f0233b0 00000880 9ae41f8c 00000000 39dd6b48 
ffffffff 67e04544 00000009  
>[ 231.183764] 1fa0: 00000081 8004bf40 ffffffff 67e04544 67e04660 
00000880 35c61f34 33d63f1c  
>[ 231.191955] 1fc0: ffffffff 67e04544 00000009 00000081 39dd6b68 
35c61f04 35c61ef0 2b3408f0  
>[ 231.200147] 1fe0: 67e06288 39dd6b30 67e03f01 6fd0c44c 20000010 
67e04660 7fff6d67 fdf7f39f  
>[ 231.208458] [<7f012d84>] (dhdsdio_htclk+0x28/0x438 [dhd]) from [<7f013490>] (dhdsdio_clkctl+0x5c/0x108 [dhd])  
>[ 231.218497] [<7f013490>] (dhdsdio_clkctl+0x5c/0x108 [dhd]) from [<7f0155b0>] (dhd_bus_stop+0x48/0x2ac [dhd])  
>[ 231.228426] [<7f0155b0>] (dhd_bus_stop+0x48/0x2ac [dhd]) from [<7f00142c>] (dhd_bus_detach+0x2c/0x44 [dhd])  
>[ 231.238242] [<7f00142c>] (dhd_bus_detach+0x2c/0x44 [dhd]) from [<7f00159c>] (dhd_detach+0x158/0x1c0 [dhd])  
>[ 231.247993] [<7f00159c>] (dhd_detach+0x158/0x1c0 [dhd]) from [<7f014638>] (dhdsdio_release+0x40/0xcc [dhd])  
>[ 231.257861] [<7f014638>] (dhdsdio_release+0x40/0xcc [dhd]) from [<7f01b24c>] (bcmsdh_remove+0x1c/0x8c [dhd])  
>[ 231.267779] [<7f01b24c>] (bcmsdh_remove+0x1c/0x8c [dhd]) from [<802ebcd0>] (sdio_bus_remove+0x18/0x54)  
>[ 231.277116] [<802ebcd0>] (sdio_bus_remove+0x18/0x54) from [<802178b0>] 
(__device_release_driver+0x84/0xd0)  
>[ 231.286790] [<802178b0>] (__device_release_driver+0x84/0xd0) from [<80217980>] (driver_detach+0x84/0xac)  
>[ 231.296287] [<80217980>] (driver_detach+0x84/0xac) from [<80216c24>] 
(bus_remove_driver+0x90/0xb8)  
>[ 231.305324] [<80216c24>] (bus_remove_driver+0x90/0xb8) from [<7f01b3d0>] (sdio_function_cleanup+0xc/0x2c [dhd])  
>[ 231.315522] [<7f01b3d0>] (sdio_function_cleanup+0xc/0x2c [dhd]) from [<7f01b5b0>] (dhd_module_cleanup+0x8/0x14 [dhd])  
>[ 231.326140] unwind: Index not found 7f01b5b0  
>[ 231.330421] Code: 0a0000d5 e5902008 e3041329 e5d031d8 (e5920030)  
>[ 232.176926] ---[ end trace 23c706acef457857 ]---  

## 分析
从上面很明显的可以看出是一个dhd模块出错了，在我的这个板子上是一个wifi的驱动，
这么一大串，吓到了。。。。

乍看是在dhdsdio_htclk这个函数中出错了，因为有这么一个片段的log啊

    PC is at dhdsdio_htclk+0x28/0x438 [dhd]

此是pc的值是在dhdsdio_htclk这个函数的范围内(啥，，你不知道pc是啥玩意，，那这个就靠你自己去google一下啦)

下面我要做的事情就是要将这个函数所对应的c文件产生的.o文件反汇编一下，如下：

>./prebuilt/linux-x86/toolchain/arm-eabi-4.4.3/bin/arm-eabi-objdump -D external/linux-bcm4329-wifi/src/dhd/linux/dhd-cdc-sdmmc-gpl-2.6.35/dhd_sdio.o > dhd_dump.text

这样dhd_sdio.c的反汇编代码就保存在dhd_dump.txt里面(注：这个是android环境下的代码路径)啦，我们找到dhdsdio_htclk这个函数的所在位置(我只贴相关部分,还附带了我的注释,汇编的注释就是c啦，哈哈哈)

    00000124 <dhdsdio_htclk>:
         124:   e3510000    cmp r1, #0  ; 0x0   ;r1=on
         128:   e92d4ff0    push    {r4, r5, r6, r7, r8, r9, sl, fp, lr}
         12c:   e1a04000    mov r4, r0  ;r4=r0=bus
         130:   e24dd024    sub sp, sp, #36 ; 0x24
         134:   e1a07002    mov r7, r2
         138:   e5905004    ldr r5, [r0, #4]    ; sdh = bus->sdh; r5=sdh    ;ok
         13c:   0a0000d5    beq 498 <dhdsdio_htclk+0x374>
         140:   e5902008    ldr r2, [r0, #8]    ; r0+8=bus->sih ; r2=bus->sih   ;ok sih's real address
         144:   e3041329    movw    r1, #17193  ; 0x4329        ;ok
         148:   e5d031d8    ldrb    r3, [r0, #472]  ;r3=r0+472=bus->alp_only ; r3 = clkreq = bus->alp_only = 0;
         14c:   e5920030    ldr r0, [r2, #48]   ;r0=r2+48=bus->sih->chip    ;XXXXXXX  NO
         150:   e3530000    cmp r3, #0  ; 0x0   ;clkreq = bus->alp_only ? SBSDIO_ALP_AVAIL_REQ : SBSDIO_HT_AVAIL_REQ;
         154:   13a03008    movne   r3, #8  ; 0x8
         158:   03a03010    moveq   r3, #16 ; 0x10
         15c:   e1500001    cmp r0, r1
         160:   1a000002    bne 170 <dhdsdio_htclk+0x4c>
         164:   e5922034    ldr r2, [r2, #52]   ;;r2+52=bus->sih->chiprev
         168:   e3520000    cmp r2, #0  ; 0x0
         16c:   03833001    orreq   r3, r3, #1  ; 0x1   ;clkreq |= SBSDIO_FORCE_ALP; r3=clkreq
         170:   e1a00005    mov r0, r5
         174:   e3a01001    mov r1, #1  ; 0x1
         178:   e59f23a8    ldr r2, [pc, #936]  ; 528 <dhdsdio_htclk+0x404>
         17c:   e28dc01c    add ip, sp, #28 ; 0x1c
         180:   e58dc000    str ip, [sp]
         184:   ebfffffe    bl  0 <bcmsdh_cfg_write>
           ......(后面省略一大段)

下面再贴出c的代码啦，别急喔，

    static int
    dhdsdio_htclk(dhd_bus_t *bus, bool on, bool pendok)
    {
        int err;
        uint8 clkctl, clkreq, devctl;
        bcmsdh_info_t *sdh;
    
        DHD_TRACE(("%s: Enter\n", __FUNCTION__));
    
    #if defined(OOB_INTR_ONLY)
        pendok = FALSE;
    #endif
        clkctl = 0;
        sdh = bus->sdh;
    
    
        if (on) {
            /* Request HT Avail */
            clkreq = bus->alp_only ? SBSDIO_ALP_AVAIL_REQ : SBSDIO_HT_AVAIL_REQ;
    
            if ((bus->sih->chip == BCM4329_CHIP_ID) && (bus->sih->chiprev == 0))
                clkreq |= SBSDIO_FORCE_ALP;
    
    
    
    
            bcmsdh_cfg_write(sdh, SDIO_FUNC_1, SBSDIO_FUNC1_CHIPCLKCSR, clkreq, &err);
            if (err) {
                DHD_ERROR(("%s: HT Avail request error: %d\n", __FUNCTION__, err));
                return BCME_ERROR;
            }
        ........(下面省略一大段)
		}
	}

由

    PC is at dhdsdio_htclk+0x28/0x438 [dhd]  

可知问题出在 从dhdsdio_htclk+0x28的代码处，由反汇编代码知dhdsdio_htclk在124位置处，加上0x28的话，就是0x14c处，我们找到0x14c对应的汇编代码

>14c:   e5920030    ldr r0, [r2, #48]   ;r0=r2+48=bus->sih->chip    ;XXXXXXX  NO  

对于这段汇编代码，我在上面已经大概做出注释了，

>140:   e5902008    ldr r2, [r0, #8]    ; r0+8=bus->sih ; r2=bus->sih   ;ok sih's real address  

由上一行汇编得知r2保存的是bus->sih的地址，r2偏移48那就是sih中的chip成员啦，可以给出sih的结构定义，如下

    typedef struct dhd_bus {
        dhd_pub_t   *dhd;
    
        bcmsdh_info_t   *sdh;           /* Handle for BCMSDH calls */
        si_t        *sih;           /* Handle for SI calls */
        char        *vars;          /* Variables (from CIS and/or other) */
        ...... dhd_bus的定义，下面省略，只需关注sih这个成员变量

接着来看看sih的定义(即si_t)

    struct si_pub {
        uint    socitype;       
        
        uint    bustype;     
        uint    buscoretype;
        uint    buscorerev; 
        uint    buscoreidx;
        int ccrev;       
        uint32  cccaps;
        int pmurev;       
        uint32  pmucaps;
        uint    boardtype;      
        uint    boardvendor;
        uint    boardflags;
        uint    chip;
    &nbsp;   uint    chiprev;     
        uint    chippkg; 
        uint32  chipst;   
        bool    issim;    
        uint    socirev;   
        bool    pci_pr32414;
    };
        
    #if defined(WLC_HIGH) && !defined(WLC_LOW)
    typedef struct si_pub si_t;
    #else
    typedef const struct si_pub si_t;
    #endif

这样就方便看汇编啦，
从上面的分析可知，我们的代码是在读取r2+48(即r2+0x30)这个地址所对应的值，然后保存到r0中的时候出错的，

下面来验证我上面的分析。

## 验证

>[ 231.043450] r10: 35c61ef0 r9 : 9ae40000 r8 : 00000001  
>[ 231.048681] r7 : 00000000 r6 : 00000000 r5 : 9c096000 r4 : 9c09f000  
>[ 231.055217] r3 : 00000000 r2 : 9c0d5000 r1 : 00004329 r0 : 9c09f000  

oops提供的信息中包含了各个寄存器的值，让我们来看看r2，r2=0x9c0d5000,
那么r2+0x30=0x9c0d5030

好了，我们知道是在读取0x9c0d5030这个地址处的值,然后保存到r0的时候出现oops的，那么到底是读取的时候出错了，还是保存的时候出错了呢，

下面我们再来看一句可以验证我们想法的log信息，那就是oops的第一句，如下

> Unable to handle kernel paging request at virtual address 9c0d5030  

 注意看这个地址，，注意看最后的这个地址啊,,,,,,9c0d5030，哇，，好熟悉啊，不就是我们上面算出来的值么,,是在读取这个地址的值的时候出错的。。。瓦咔咔,,,分析出来了
 
## 疑问
上面好像一片和谐的景象啊，，结果有了，哈哈哈，可是不要高兴的太早喔，，结果是有了，可是该怎么解决呢，，毕竟我们分析问题的目的就是为了解决问题啊。。

单从该问题来说，我觉得可能是因为sih这个变量已经被deatch了，但是还没有验证，问题比较偶现，，唉，，最烦偶现的bug了，，

其实写这篇文章的目的也主要是为了讲述怎么从oops信息中去查找对应c代码中的错误行的，在linux内核调试中还是很有用的。

>Unable to handle kernel paging request at virtual address &lt;pre name="code" class="cpp">9c0d5030  

其实对于这句话我还是没有能够理解到底是怎么了，怎么会出现这种错误，

如果哪位朋友对这个比较了解的话，希望能不吝赐教，多多回帖帮我解惑，再此先感谢了。

---
ps: 解答上面的问题

## 解答
不能访问的内核虚地址为45685516，内核中一般可访问的地址都是以0xCXXXXXXX开头的地址。

	Oops: 0002 [#1]

这里面，0002表示Oops的错误代码（写错误，发生在内核空间），#1表示这个错误发生一次。

Oops的错误代码根据错误的原因会有不同的定义，本文中的例子可以参考下面的定义（如果发现自己遇到的Oops和下面无法对应的话，最好去内核代码里查找）：

error_code:

* bit 0 == 0 means no page found, 1 means protection fault
* bit 1 == 0 means read, 1 means write
* bit 2 == 0 means kernel, 1 means user-mode
* bit 3 == 0 means data, 1 means instruction
