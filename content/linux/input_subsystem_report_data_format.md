Title: input子系统 KeyPad-Touch上报数据格式与机制
Date: 2012-04-17 14:48:23
Tags: input, linux, touch, keypad

### 上报格式
linux drive中input子系统上报信息，调用函数

    void input_event(struct input_dev *dev, unsigned int type, unsigned int code, int value);

input子系统最终调用`copy_to_user(buffer, event, sizeof(struct input_event))`将信息上报给上层，event为`struct input_event`类型结构体， 中间会有一些处理将 type，code，value值打包成input_event类型的数据。底层上报该结构体给上层。
    
    struct input_event {
        struct timeval time;
        __u16 type;
        __u16 code;
        __s32 value;
    };
    
    struct timeval {
        __kernel_time_t tv_sec; /* seconds */
        __kernel_suseconds_t tv_usec; /* microseconds */
    };
    
    typedef long        __kernel_time_t;
    typedef int __kernel_suseconds_t;

#### 对于keypad

type为事件类型，按键为EV_KEY,在include/linux/input.h中,

    #define EV_KEY    0x01

code为按键的值，value用于标记按键是按下还是弹起，1是按下，0是弹起。
按下和弹起事件只需上报一次。

#### 对于touch
`static inline void input_report_abs(struct input_dev *dev, unsigned int code, int value)`  为input_event的封装，函数如下

    input_event(dev, EV_ABS, code, value);

type为EV_ABS,  #define EV_ABS   0X03,

code的值，根据上报属性的不同，分别如下：

<font color=red>多点触摸</font>

    #define ABS_MT_TOUCH_MAJOR 0x30 /* Major axis of touching ellipse */
    #define ABS_MT_TOUCH_MINOR 0x31 /* Minor axis (omit if circular) */
    #define ABS_MT_WIDTH_MAJOR 0x32 /* Major axis of approaching ellipse */
    #define ABS_MT_WIDTH_MINOR 0x33 /* Minor axis (omit if circular) */
    #define ABS_MT_ORIENTATION 0x34 /* Ellipse orientation */
    #define ABS_MT_POSITION_X 0x35 /* Center X ellipse position */
    #define ABS_MT_POSITION_Y 0x36 /* Center Y ellipse position */
    #define ABS_MT_TOOL_TYPE 0x37 /* Type of touching device */
    #define ABS_MT_BLOB_ID 0x38 /* Group a set of packets as a blob */
    #define ABS_MT_TRACKING_ID 0x39 /* Unique ID of initiated contact */
    #define ABS_MT_PRESSURE 0x3a /* Pressure on contact area */

ABS_MT_TOUCH_MAJOR和ABS_MT_PRESSURE实现一个应该就可以了。

<font color=red>多点触摸</font>

input.h中列举了很多属性，但只需实现以下几种即可。

    #define ABS_X 0x00
    #define ABS_Y 0x01
    #define ABS_Z 0x02  //一般不必实现
    #define ABS_PRESSURE 0x18

下面一个BTN_TOUCH为点击事件，单点触摸中需要上报点击事件

    #define BTN_TOUCH 0x14a

### touch点上报机制
<font color=red>多点触摸</font>

value为对应属性的值，如code为ABS_MT_POSITION_X，则value的值为就为x轴坐标。

当把一个点的信息发送完毕以后，还需加上input_mt_sync（注意：即使只有一个点也需要加上），这个函数转换成input_event事件为

    input_event(dev, EV_SYN, SYN_MT_REPORT, 0);
    #define EV_SYN  0x00
    #define SYN_MT_REPORT    2

则type为0x00，code为2，value为0。

接着再上报第二个点，第二个点上报结束，依旧要上报input_mt_sync，直至最后一次报点结束，加上input_sync，转换成input_event事件为

    input_event(dev, EV_SYN, SYN_REPORT, 0)；
    #define EV_SYN  0x00
    #define SYN_REPORT 0

则type为0x00，code为0，value为0。至此报点结束。

点需要一直上报。

Linux 驱动中的例子

    input_report_abs(ssd2531_data.input, ABS_MT_TRACKING_ID, 1);
    input_report_abs(ssd2531_data.input, ABS_MT_TOUCH_MAJOR, PRESS_STATUS);
    input_report_abs(ssd2531_data.input, ABS_MT_POSITION_X, X_COOR);
    input_report_abs(ssd2531_data.input, ABS_MT_POSITION_Y, Y_COOR);
    input_mt_sync(ssd2531_data.input);

<font color=red>单点触摸</font>

单点上报同多点上报差不多，只是不需要input_mt_sync了，上报过程中需要

    input_event(dev, EV_KEY, BTN_TOUCH,  0/1 );

value为1，代表按下，value为0代表抬起。code值为BTN_TOUCH，  #define BTN_TOUCH 0x14a；

同样最后结束需要input_sync。

linux驱动的例子:

    input_report_abs(ts.input, ABS_X, ts.xp);
    input_report_abs(ts.input, ABS_Y, ts.yp);
    input_report_key(ts.input, BTN_TOUCH, 1);
    input_sync(ts.input);

input_event结构体中，有一个成员为struct timeval time;用来记录此刻的墙上时间。
