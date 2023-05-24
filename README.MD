# 1、Hardware
This python script support Nextion and TJC USART display hardware to flash TFT file by serial.
One more thing is in order to retry flash when last time flash fail. There is a hardward reset function in this script and it can auto reset the display to let it reboot and then enter flash mode.
But this function need a hardware design support. For myself..i use a SC16IS752 chip to extend the GPIO PIN and let display REST pin connect to extend GPIO which i select to sent LOW GPIO singal to let display reboot.

哎~最近研究了好久关于如何通过串口来更新Nextion或者陶晶驰的串口屏。好在他俩是通用的，所以本程序一样可以支持这两个品牌的屏幕硬件。
注意，因为刷固件失败率还是蛮高的，所以为了刷机方便，特别设计了用GPIO来连接串口屏的REST引脚，在程序开始的时候，会先发送一个低电平来硬件复位串口屏。防止上一次失败之后卡在刷机界面，还要手动拔插屏幕重启。
至于连接到啥GPIO，我本身用的就是SC16IS752来扩展了一路USART接口，所以自然用的就是SC16IS752上的扩展GPIO。当然，也可以使用其他的GPIO接口。

