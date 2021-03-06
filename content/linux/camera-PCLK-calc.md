Title: 对于camera调试中PCLK的计算
Date: 2012-06-20 15:05
Update: 2016-05-30 15:34

[1]: /static/images/android/BT656-Lines.png

## 关于PCLK
PCLK即 pixclk,像素时钟信号

对于PAL信号和NTSC信号,两者PCLK分别为27M和27.2M

#### 计算公式

1728\*625\*25=27000000

1728\*525\*30=27216000

其中1728=720\*2+8+280

## BT656 每一行数据组成（Lines）
下面说明每一行的组成，一行是由4个部分组成：

行 = 结束码（EAV） + 水平消隐（Horizontal Vertical Blanking） + 起始码（SAV） + 有效数据（Active Video）

典型的一行数据组成如下图所示：

![BT656 LINES][1]

起始码（SAV）和结束码（EAV），它是标志着一行的开始结束的重要标记，也包含了其他的一些重要的信息。

为什么水平消隐 是280字节，这个我暂时还没搞清楚，不知道是不是标准定义的。

为什么一行中的有效数据是 1440 字节？ 因为PAL制式的SDTV或者D1的分辨率为 720*576，即一行有720个有效点，由于采集的是彩色图像，那么一行就是由亮度信息（Y）和色差信息（CbCr）组成的，由于是 YCbCr422格式，故一行中有720列Y，720列CbCr，这样，一行的有效字节数就自然为 720 x 2 = 1440 字节了。

从上面可以看出BT656格式的数据一行组成需要1728字节，然后PAL有625行，NTSC有525行，两种制式的数据刷新频率分别是25HZ和30HZ

这样更新一个像素点需要的时钟即为刚开始写的，

PAL：1728*625*25=27000000 HZ

NTSC：1728*525*30=27216000 HZ

