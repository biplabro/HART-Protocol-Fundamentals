# Using the script:
# While using the data.txt file method, both files must be in same directory
# 'python data_upstream.py' for normal operation
# 'python data_upstream.py --debug' for debug mode
# Tested & fully compatible with python2.x, python3.x
# serial device can be interfaced as and when required, provisions given in code
# ==============================================================================

import time									# required for delay function
import sys									# required for fetching cmdline argument
# import serial_library module	
# import serial, time, io, datetime
# from serial import Serial							# required for serial device interface

dummy_data = open('HART_Data.txt', 'r')                                        	# open datafile read-only, py script & datafile in same directory
lines = dummy_data.readlines()							# read all the lines, enumerate line numbers

# serial device configuration (optional)
# serial setup
'''
addr0 = "/dev/ttyS0"								# serial port for the interface
baud = 9600									# baud rate of the instrument

ser = serial.Serial(                    					# serial port hardware configuration, serial object
    port = addr0,\
    baudrate = baud,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)
'''

def upstream_data (in_bytes, script_arg):					# function for data interpretation & error checking module

	############### segregation of information #######################
	packet_len = (len(in_bytes)-1)//2					# length in bytes (2 nibbles each). `//` int division operator python 3.x
	incoming_checksum = in_bytes[-3:-1]					# Last byte (HH) is incoming checksum, [reverse index:remaining]
	slave_id = in_bytes[12:14]						# refer HART_data.txt for index
	command_code = in_bytes[14:16]                                                  
	incoming_byte_count = in_bytes[16:18]
	data_bytes = in_bytes[22:-3]						# separate only the device data (variables)
	data_bytes_count = len(in_bytes[22:-3])//2                                       
	for_check = in_bytes [0:(len(in_bytes)-3)]				# Separated string, excluding the checksum byte, for cs calculation
			                                   
	############# error check module0 (checksum based) ###############
	xor = 0									# value initiated with 0
	i = 0									# index initiated with 0
	while i < len(for_check):						# initiate xor operation till length of the data
		xor = xor ^ ord(for_check[i])					# Bitwise xor, incremental value
		i += 1								# move pointer to next value

	checksum = hex (xor)							# outputs 0xFF format
	calculated_checksum = checksum[2:].zfill(2)				# remove `0x`, add leading 0 with zfill(), if required
	calculated_checksum = calculated_checksum.upper()			# convert string to uppercase for comparison

	if (incoming_checksum == calculated_checksum):				# Compare checksums
		cs = "00"							# checksum pass flag for upstream
	else:
		cs = "01"

	############# error check module1 (byte_count based) #############
	packet_byte_count = hex (len (for_check[18:])//2)			# `//` int division operator python3.x, calculate byte count & convert to hex
	calculated_byte_count =  packet_byte_count[2:].zfill(2)			# remove `0x`, add leading 0 with zfill(), if required
	calculated_byte_count = calculated_byte_count.upper()			# convert string to uppercase for comparison

	if (incoming_byte_count == calculated_byte_count):			# Compare bytecount
		bc = "00"							# byte count pass flag
	else:
		bc = "01"

	############### error check module2 (value based) ##############
	'''
	algo:
	=====
	1. user_input or predefined threshold for measuring parameters
		or
		import files containing ML algorithm in this file header
		call ML func, obtain values suggested by the ML script

	2. read the data bytes from HART/FDT command
	3. interpret & compare the data 
	4. add flag (0xHH) with upstream data for NorthBound application
	'''
	################# error check module3 (? based) ################

	#################### debugging information #####################
	if (script_arg == "--debug"):						# debug information output
			print ("Incoming packet: " + (in_bytes))		# Print packet length
			print ("Debug information")
			print ("Packet length: " + str(packet_len) + " Bytes")	# int to string conversion & concatenation
			print ("Slave address: " + (slave_id))                                       
			print ("Command code: " + (command_code))
			print ("Data Bytes: " + (data_bytes))
			print ("Total number of Data Bytes: " + str(data_bytes_count) + " Bytes")    
			print ("Checksum input: " + (for_check))		# print bytestream for checksum calculation
			print ("Incoming checksum: " + (incoming_checksum))
			print ("calculated checksum: " + (calculated_checksum))                       
			print ("Incoming byte count: " + (incoming_byte_count))
			print ("calculated byte count: " + (calculated_byte_count)) 

	################# formatted upstream data ####################
	upstream_data = str(slave_id + command_code + data_bytes + cs + bc)	# formatted string with checksum & byte count flag for upstream

	if (cs == "01"):							# error acknowledgement
		print ("Error: Checksum Mismatch")
					                       
	if (bc == "01"):							# warning acknowledgement
		print ("Warning: Byte count Mismatch")

	if (cs == "00") and (bc == "00"):
		print ("Valid Datastream")					# validation acknowledgement

	print ("Upstream data: " + upstream_data)
	print ("----------------------------------------------")

##################################_Main Loop_###################################
##################_Infinite loop for embedded applications_#####################
while True:
# Read from serial device & store the data into data_fed variable (optional)
# data_fed = str(ser.readline())						# reading serial dtastream from instrument, timeout = specify

	try:									# try: except: condition, enabling interrupt
		for i in range(8):						# 8 refers to the first 8 lines of the input.txt file, variable
			if (len(sys.argv) == 1):				# running script in minimal info mode
				data_fed = str(lines[i])			# line from the input.txt file
				print ("Processing information: instance " + str(i+1))
				upstream_data (data_fed, 0)			# feeding the bytestream into upstream_data(), no --debug flag
				time.sleep(1)					# delay between reading two instances

			if (len(sys.argv) == 2):				# checking for second[1] cmdline_arg
				cmdline_arg = sys.argv[1]
				if (cmdline_arg == "--debug"):			# enabling --debug mode
					data_fed = str(lines[i])		# line from the input.txt file
					print ("Processing information: instance " + str(i+1) + " with --Debug mode")
					upstream_data (data_fed, cmdline_arg)	# feeding the bytestream into upstream_data(), with --debug flag
					time.sleep(3)
				else:
					print ("Invalid argument")		# patch for invalid arguments
					time.sleep(2)

			if ((len(sys.argv) >= 3)):				# patch for invalid arguments
				print ("Invalid argument")
				time.sleep(2)

	except KeyboardInterrupt:						# enable interrupt using "ctrl+c" 
	        print ("Interrupted")
	        break


# References
# ==========
# https://www.guru99.com/reading-and-writing-files-in-python.html
# https://www.knowledgehut.com/blog/programming/sys-argv-python-examples
# https://stackoverflow.com/a/19824763
# https://gist.github.com/projectweekend/1fae5a8cf2a5b9282f3d
# https://pyserial.readthedocs.io/en/latest/shortintro.html
# https://stackoverflow.com/q/845058
# https://www.w3schools.com/python/python_for_loops.asp
# https://www.programiz.com/python-programming/for-loop
# https://docs.python.org/2/library/stdtypes.html#str.zfill
# https://stackoverflow.com/a/15884750/12747885
# https://realpython.com/python-sleep/





