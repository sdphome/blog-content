Title: Android HAL层实现与调用
Date: 2012-05-21 11:29:23
Tags: android, hal

## HAL层实现
在这篇文章中我们讨论下HAL层代码的简单组成，以及jni是如何调用HAL层代码。文章尽量避免了一些无用信息，直接写有实际的东西。

在这里我用一个简单的HAL层代码(电子防眩目的hal代码)来开始我们的讲解。

在一个hal代码中主要的工作是实现一个名为`HAL_MODULE_INFO_SYM`的module实例，其结构定义为:

        struct lcd_reflect_module_t {
            struct hw_module_t common;
        };

可以看到这个结构的名字是随意的，一般用(模块名_module_t)来表示，可以看到它只有一个成员变量hw_module_t，也就是说主要的工作就是填充这个hw_module_t这个结构了。

    const struct lcd_reflect_module_t HAL_MODULE_INFO_SYM = {
        .common = {
            .tag = HARDWARE_MODULE_TAG,
            .version_major = 1,
            .version_minor = 0,
            .id = LCD_REFLECT_HARDWARE_MODULE_ID,
            .name = "LCD Reflect",
            .author = "Archermind Tech.",
            .methods = &lcd_reflect_module_methods,
        }
    };

可以看到其中只有一个open函数指针，作为module的callback。

前面我们已经接触了两个重要的结构体，hw_module_t和hw_module_methods_t，下面我们还需要来看一下hal层中第三个重要的结构体hw_device_t。

下面我们来看一下`hw_module_methods_t`中的open函数`lcd_reflect_module_methods`。

    static int
    lcd_reflect_open(const struct hw_module_t *module,
    
                  const char *name, struct hw_device_t **device)
    {
        int status = -EINVAL;
    
        LOGV("lcd_reflect_open\n");
        if (!strcmp(name, LCD_REFLECT_HARDWARE)) {
            struct lcd_reflect_device_t *dev;
    
            dev = malloc(sizeof (*dev));
            memset(dev, 0, sizeof (*dev));
    
            dev->common.tag = HARDWARE_DEVICE_TAG;
            dev->common.version = 0;
            dev->common.module = (struct hw_module_t *)module;
            dev->common.close = lcd_reflect_close;
    
            *device = &dev->common;
    
            dev->get_level = &lcd_reflect_get_level;
            dev->set_level = &lcd_reflect_set_level;
            dev->get_state = &lcd_reflect_get_state;
            dev->set_state = &lcd_reflect_set_state;
    
            status = 0;
        }
        
        return status;
    }

可以看到hw_device_t作为open的形参传入open函数中，并且我们还发现了另外一个结构体`struct lcd_reflect_device_t *dev;`这个结构是我们模块自己定义的，用于存放一些我们模块需要的操作，jni层中就是通过这个结构体来调用hal层中提供的接口的。看一下它的定义。

    struct lcd_reflect_device_t {
        struct hw_device_t common;
    
        /**
         * Get the mxc_reflect state
         *
         * Returns: 0 on success, error code on failure
         */
        int (*get_state)(struct lcd_reflect_device_t *dev,
                         int *stat);
    
        /**
         * Set the mxc_reflect state
         *
         * Returns: 0 on success, error code on failure
         */
        int (*set_state)(struct lcd_reflect_device_t *dev,
                         int stat);
    
        /**
         * Get the mxc_reflect level
         *
         * Returns: 0 on success, error code on failure
         */
        int (*get_level)(struct lcd_reflect_device_t *dev,
                        int *level);
    
        /**
         * Set the mxc_reflect state
         *
         * Returns: 0 on success, error code on failure
         */
        int (*set_level)(struct lcd_reflect_device_t *dev,
                        int level);
    };

里面有hw_device_t这个成员，并且它是在最前面的一个成员，这个是非常重要的，我们将在下面说明为什么它需要放在最前面，除了hw_device_t就是一些hal层需要提供给jni调用的函数指针。

再回到open函数中，现在我们就能看懂这个open函数所做的工作了，它首先注册了一个`struct lcd_reflect_device_t *dev; lcd_reflect_device_t`变量，然后填充common，也就是hw_device_t这个结构，这里需要注意有几个成员：

tag：必须指定为`HARDWARE_DEVICE_TAG`

还需要实现一个close函数，接着*device= &dev->common;，即让jni的hw_device_t与hal中的`lcd_reflect_device_t`联系在一起了，由于common这个成员在`lcd_reflect_device_t`的最前面定义的，那么也就是`lcd_reflect_device_t`的地址和common的地址是相同的。只要知道common的地址就可以知道`lcd_reflect_device_t`的地址，这样`lcd_reflect_device_t`结构就可以传送到jni层使用了，只需要将common的地址强制转换一下即可。最后把hal层需要提供给jni的API实现就可以了。这样一个简单的hal层代码框架就有啦。

## 调用HAL

在jni层，我们通过hw_get_module函数得到hw_module_t结构，如下：

	hw_get_module(LCD_REFLECT_HARDWARE_MODULE_ID,(hw_module_t const**)&module);

通过指定`LCD_REFLECT_HARDWARE_MODULE_ID`来区别module,接着还需要得到`lcd_reflect_device_t*device;`这个结构，我们可以通过下面这个函数实现：

    static lcd_reflect_device_t *
    get_device(hw_module_t *module, char const *name)
    {
        int err;
        hw_device_t *device;
    
        err = module->methods->open(module, name, &device);
        if (err == 0) {
            return (lcd_reflect_device_t *)device;
        } else {
            return NULL;
        }
    }

函数返回的是`lcd_reflect_device_t`结构的地址，在函数中首先定义`hw_device_t*device;`接着将其通过`module->methods->open(module,name, &device);`得到`hw_device_t`这个结构的地址，接着将这个地址返回，返回前需要将地址类型强制转换一下，`(lcd_reflect_device_t*)device`，这样就得到`lcd_reflect_device_t`这个结构的地址啦。原因我们在上面讲过，是因为`hw_device_t`和`lcd_reflect_device_t`两个结构的首地址是相同的。

 有了`lcd_reflect_device_t`我们就可以调用hal层中实现的API啦，通过这些API操作硬件。
