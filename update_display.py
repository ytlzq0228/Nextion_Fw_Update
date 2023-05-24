#!/usr/bin/python
# coding=UTF-8
import serial #导入模块
import time
import os
import sys
import RPi.GPIO as GPIO
from tqdm import tqdm
from tqdm import trange
file_dir = os.path.dirname(os.path.realpath(__file__))
from reset_display_hardware import REST_Hardware

#GPIO.setwarnings(False)
#GPIO.setup(26, GPIO.OUT)

def recv(serial):
	i=0
	while i<10:
		i+=1
		time.sleep(0.3)
		data = serial.read_all()
		if data == b'':
			continue
		else:
			break
	return data

	

def open_file(file_name):
	f=open(os.path.join(file_dir,file_name),"rb")
	print(f.len())



def send_data_to_serial(ser, data, expectedAck, TryTime,download_baud):
	ser.write(data)
	#time.sleep(len(data)*8/download_baud+0.01)
	time.sleep(0.05)
	for i in range(TryTime):
		ack = ser.read_all()
		if len(ack)>0:
			break
		else:
			#print("Waiting Ack Singal.....")
			time.sleep(0.01)
			continue
	if len(ack)==0:
		print("DownLoad Fail~~")
		raise




def sent_file(file_name,ser,download_baud):
	readLen=4096
	dataList = []
	fileSize = os.path.getsize(os.path.join(file_dir,file_name))
	blockNum = fileSize/readLen
	if fileSize%readLen != 0:
		blockNum += 1
	print ("size %d, blockNum %d" % (fileSize, blockNum))
	
	with open(os.path.join(file_dir,file_name),'rb+') as f:
		for i in range(int(blockNum)):
			block = f.read(readLen)
			#dataList.append(block.strip())
			dataList.append(block)
	f.close()	
	n=0
	step=4096/readLen
	for i in tqdm(dataList,desc="Download Process: "):
		if (n+1)%step==0:
			send_data_to_serial(ser, i, b'\x05', 500,download_baud)
		else:
			ser.write(i)
		#print("sent block %s OK"%str(n))
		n+=1



def flash_tft_file(sent_update_file_name,download_baud,portx):
	try:
		
		#if (input("Find Port Baud?Y/N[default:Y]: ") or "Y")!="N":
		REST_Hardware()
		#sent_update_file_name="MMDVM_USART_HMI.tft"
		available_baud_list=[2400,4800,9600,19200,38400,57600,115200,230400,256000,512000,921600]
		#portx="/dev/ttySC1"
		for baud in available_baud_list:
			ser=serial.Serial(portx,baud,timeout=5)
			print("Try Baud: ", baud)
			ser.write(bytes.fromhex('00 ff ff ff'))
			ser.write("connect".encode("UTF-8"))
			ser.write(bytes.fromhex('ff ff ff'))
			time.sleep(0.5)
			msg = recv(ser)
			if len(msg.split())>0:
				if msg.split()[0].decode("UTF-8")=="comok":
					print("Connect Success..", ser)
					break
			else:
				print("Connect Fail with Baud: ", baud)
			ser.close()
		
		file_size=os.path.getsize(os.path.join(file_dir,sent_update_file_name))
		print("file_size:%s"%str(file_size))
		ser.write(("whmi-wri %s,%s,0"%(str(file_size),str(download_baud))).encode("UTF-8"))
		ser.write(bytes.fromhex('ff ff ff'))
		ser.close()
		#reconnect serial with new baud parament
		ser=serial.Serial(portx,download_baud,timeout=None)
		msg=recv(ser)
		#print(msg)
		if msg==b'\x05':
			print("Echo OK and it will start update file now.")
		else:
			print("Warning...Wait Echo timeout but it still OK to try to update tft file.")
		time.sleep(1)
		print("Start DownLoad TFT File")
		sent_file(sent_update_file_name,ser,download_baud)
		ser.close()
		return True
	
	except Exception as e:
		print("Exception as",e)
		return False



if __name__ == '__main__':
	if len(sys.argv)>1:
			if sys.argv[1]=='-d':
				sent_update_file_name="MMDVM_USART_HMI_T124_115200.tft"
				download_baud=115200
				portx="/dev/ttySC0"
				retry_times=10
			else:
				print("invalid argv")
				raise
	else:
		sent_update_file_name=input("Please Input Update File Name[default:MMDVM_USART_HMI_T124_115200.tft]: ") or "MMDVM_USART_HMI_T124_115200.tft"
		download_baud=int(input("Please Input Download Baud[9600,19200,38400,57600,115200,230400][default:115200]: ") or 115200)
		portx=input("Please Input Serial Port[default:/dev/ttySC0]: ") or "/dev/ttySC0"
		retry_times=input("Please Input Retry Times[default:10]: ") or 10
	for retry_time in range(retry_times):
		run_result=flash_tft_file(sent_update_file_name,download_baud,portx)
		if run_result:
			break
