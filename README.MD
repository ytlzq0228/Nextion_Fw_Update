# 1、Hardware
This python script support Nextion and TJC USART display hardware to flash TFT file by serial.
One more thing is in order to retry flash when last time flash fail. There is a hardward reset function in this script and it can auto reset the display to let it reboot and then enter flash mode.
But this function need a hardware design support. For myself..i use a SC16IS752 chip to extend the GPIO PIN and let display REST pin connect to extend GPIO which i select to sent LOW GPIO singal to let display reboot.

哎~最近研究了好久关于如何通过串口来更新Nextion或者陶晶驰的串口屏。好在他俩是通用的，所以本程序一样可以支持这两个品牌的屏幕硬件。
注意，因为刷固件失败率还是蛮高的，所以为了刷机方便，特别设计了用GPIO来连接串口屏的REST引脚，在程序开始的时候，会先发送一个低电平来硬件复位串口屏。防止上一次失败之后卡在刷机界面，还要手动拔插屏幕重启。
至于连接到啥GPIO，我本身用的就是SC16IS752来扩展了一路USART接口，所以自然用的就是SC16IS752上的扩展GPIO。当然，也可以使用其他的GPIO接口。

# 2、Using

作者还比较懒，没有把整个刷机过程优化成脚本，我先大概说说。各位自己试试看，同时期待反馈
## 1、关闭目前占用屏幕串口的程序，释放串口资源。
	对于使用Pi-Star的HAM们而言
	如果安装了NextionDriver，需要更改NextionDriver的使用接口，然后重启树莓派。对于使用MMDVM Host直连串口屏，更改MMDVM的Nextion端口，然后保存就可以了。
## 2、尝试运行
```
cd ~
git clone https://github.com/ytlzq0228/Nextion_Fw_Update.git
python3 Nextion_Fw_Update/update_display
```
估计第一次运行肯定冒烟，重点关注python pip install包。具体装啥，你要不看看报错，然后缺啥就装啥呗。

## 3、参数
Please Input Update File Name[default:MMDVM_USART_HMI_T124_115200.tft]: //输入同文件夹下的tft文件名称
Please Input Download Baud[9600,19200,38400,57600,115200,230400][default:115200]:选择下载时候的波特率，默认使用115200下载
Please Input Serial Port[default:/dev/ttySC0]: 选择屏幕串口
Please Input Retry Times[default:10]: 选择自动重试次数

## 4、运行过程
Export: Pin0
Export: Pin1
Export: Pin2
Export: Pin3
Export: Pin4
Export: Pin5
Export: Pin6
Export: Pin7
Pin0:Output //拉低GPIO引脚电平，RESET屏幕，重启屏幕
Try Baud:  2400
Connect Fail with Baud:  2400
Try Baud:  4800
Connect Fail with Baud:  4800
Try Baud:  9600
Connect Fail with Baud:  9600
Try Baud:  19200
Connect Fail with Baud:  19200
Try Baud:  38400
Connect Fail with Baud:  38400
Try Baud:  57600
Connect Fail with Baud:  57600
Try Baud:  115200
//依次尝试屏幕当前所在的各种波特率
Connect Success.. Serial<id=0x766c6d70, open=True>(port='/dev/ttySC0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False) //建连成功，反馈串口对象参数
file_size:2599960 //TFT文件尺寸
Warning...Wait Echo timeout but it still OK to try to update tft file. //本来预期是在发送更新指令后250ms屏幕将会返回一个\x05的字节，确认屏幕进入刷机状态。但实际因为树莓派中断问题，导致以新的波特率重新建连串口对象的时间超过250ms，可能等不到这个信号。但是无所谓，不影响
Start DownLoad TFT File
size 2599960, blockNum 635 //Nextion下载会在每接受4096个字节后返回一个确认信号，基于此确认屏幕是否成功接收。但是，没有重传机制，丢包没救，直接重刷。程序在2s内等不到上一个4096字节的确认接收信号，会重新开始，复位硬件，重新刷机。
Download Process: 100%|██████████████████████████████████████| 635/635 [05:19<00:00,  1.99it/s]
