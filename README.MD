# 1、Hardware
This python script support Nextion and TJC USART display hardware to flash TFT file by serial.
One more thing is in order to retry flash when last time flash fail. There is a hardward reset function in this script and it can auto reset the display to let it reboot and then enter flash mode.
But this function need a hardware design support. For myself..i use a SC16IS752 chip to extend the GPIO PIN and let display REST pin connect to extend GPIO which i select to sent LOW GPIO singal to let display reboot.

哎~最近研究了好久关于如何通过串口来更新Nextion或者陶晶驰的串口屏。好在他俩是通用的，所以本程序一样可以支持这两个品牌的屏幕硬件。
注意，因为刷固件失败率还是蛮高的，所以为了刷机方便，特别设计了用GPIO来连接串口屏的REST引脚，在程序开始的时候，会先发送一个低电平来硬件复位串口屏。防止上一次失败之后卡在刷机界面，还要手动拔插屏幕重启。
至于连接到啥GPIO，我本身用的就是SC16IS752来扩展了一路USART接口，所以自然用的就是SC16IS752上的扩展GPIO。当然，也可以使用其他的GPIO接口。

# 2、Using
ennn~i am sorry that i have not writed a script yet to run this process automatically.Yeahhh but i will do that in the future. trust me....
Right now. I am looking forward that you can run it as below and tell me if you have any idea
作者还比较懒，没有把整个刷机过程优化成脚本，我先大概说说。各位自己试试看，同时期待反馈
## 1、关闭目前占用屏幕串口的程序，释放串口资源。Close the application which one use this serial resource
	For HAM who use pi-star system. please change NextionDriver config in the Expert page and reboot Raspberry by manual if you used NextionDriver. Or you can directly change MMDVM display method to None and then save it if you haven't use NesxtionDriver.
	对于使用Pi-Star的HAM们而言
	如果安装了NextionDriver，需要更改NextionDriver的使用接口，然后重启树莓派。对于使用MMDVM Host直连串口屏，更改MMDVM的Nextion端口，然后保存就可以了。
## 2、尝试运行 Try to run it in the first time
```
cd ~
git clone https://github.com/ytlzq0228/Nextion_Fw_Update.git
python3 Nextion_Fw_Update/update_display
```
估计第一次运行肯定冒烟，重点关注python pip install包。具体装啥，你要不看看报错，然后缺啥就装啥呗。
I think in the most possible. It will raise some err when you run it in the first time. please attention if there are some err releated with python pip packet. install it.....

## 3、参数 Parameter
```
Please Input Update File Name[default:MMDVM_USART_HMI_T124_115200.tft]: //输入同文件夹下的tft文件名称Input Update File Name
Please Input Download Baud[9600,19200,38400,57600,115200,230400][default:115200]:选择下载时候的波特率，默认使用115200下载/you can also input the baud by your self. default is 115200bps
Please Input Serial Port[default:/dev/ttySC0]: 选择屏幕串口/Select the Serial Port
Please Input Retry Times[default:10]: 选择自动重试次数/Retry times
```

## 4、运行过程 Flash Process
```
Export: Pin0
Export: Pin1
Export: Pin2
Export: Pin3
Export: Pin4
Export: Pin5
Export: Pin6
Export: Pin7
Pin0:Output //拉低GPIO引脚电平，RESET屏幕，重启屏幕 GPIO PIN will  output a low level to display modul reset PIN (if you connect it )to let it reset.
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
//依次尝试屏幕当前所在的各种波特率 It will try all support baud one by one to find the correct baud which can communication with display modul
Connect Success.. Serial<id=0x766c6d70, open=True>(port='/dev/ttySC0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False) //建连成功，反馈串口对象参数
file_size:2599960 //TFT文件尺寸
Warning...Wait Echo timeout but it still OK to try to update tft file. //本来预期是在发送更新指令后250ms屏幕将会返回一个\x05的字节，确认屏幕进入刷机状态。但实际因为树莓派中断问题，导致以新的波特率重新建连串口对象的时间超过250ms，可能等不到这个信号。但是无所谓，不影响
Start DownLoad TFT File
size 2599960, blockNum 635 //Nextion下载会在每接收4096个字节后返回一个确认信号，基于此确认屏幕是否成功接收。但是，没有重传机制，丢包没救，直接重刷。程序在2s内等不到上一个4096字节的确认接收信号，会重新开始，复位硬件，重新刷机。
Download Process: 100%|██████████████████████████████████████| 635/635 [05:19<00:00,  1.99it/s]
```

# 3、已知冲突
在刷新固件过程中，由于使用了I2C转USART，可能会因为I2C的总线上的其他设备导致I2C转USART的数据流异常。具体原因太复杂了，大家伙自己感兴趣的可以去看看。
## 1、与PiSugar3套件的I2C设备存在冲突，但是有解，需要更新PiSugar的固件
[https://github.com/PiSugar/PiSugar/wiki/PiSugar-3-Series](https://github.com/PiSugar/PiSugar/wiki/PiSugar-3-Series)
```
curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash
```
## 2、与GeekWork X729套件兼容性良好，没问题，大胆用

# 4、Remark
## 关于GPIO针脚的设置
实际测试发现在不同的树莓派上，SC16IS752上的扩展GPIO定义不一样。修改定义方式如下：
### 1、确认SC16IS752上的扩展GPIO其实资源
ls -l /sys/class/gpio/
./../devices/platform/soc/fe804000.i2c/i2c-1/1-004d/gpio/gpiochip496
找到对应i2c地址路径的gpio芯片，例如496
### 2、修改c/gpio下的SC16IS752GPIO.h
其中修改#define PIN0 496
### 3、编译生成SC16IS752GPIO.so
gcc SC16IS752GPIO.c -fPIC -shared -o SC16IS752GPIO.so
### 4、copy SO文件
cp SC16IS752GPIO.so ..
