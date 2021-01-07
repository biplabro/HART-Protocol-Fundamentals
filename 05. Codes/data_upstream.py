import time
import sys
'''
debug_flag = ""
debug_flag = sys.argv[1:]
print sys.argv[1:]
print debug_flag
'''

dummy_data = open('HART_Data.txt', 'r')                                            # open datafile readonly, py script & datafile in same directory
lines = dummy_data.readlines()


def upstream_data (in_bytes, script_arg):

	########## segregation of information #################
	packet_len = len(in_bytes)/2                                                    # length in bytes (2 nibbles each)
	incoming_checksum = in_bytes[-3:-1]                                              # Last byte (HH) is incoming checksum, [reverse index:remaining]
	slave_id = in_bytes[12:14]                                                      # refer HART_data.txt for index
	command_code = in_bytes[14:16]                                                  
	incoming_byte_count = in_bytes[16:18]
	data_bytes = in_bytes[22:-3]
	data_bytes_count = len(in_bytes[22:-3])/2                                       
	for_check = in_bytes [0:(len(in_bytes)-3)]                                      # Separated string, excluding the checksum byte
		                                       
	############# error check module0 (checksum based) ###############
	xor = 0                                                                         # value initiated with 0
	i = 0                                                                           # index initiated with 0
	while i < len(for_check):                                                       # initiate xor operation till length of the data
	    xor = xor ^ ord(for_check[i])                                               # Bitwise xor
	    i += 1                                                                      # move pointer to next value

	checksum = hex (xor)                                                            # outputs 0xFF format
	calculated_checksum = checksum[2:].zfill(2)                                     # remove `0x`, add leading 0 with zfill(), if required
	calculated_checksum = calculated_checksum.upper()                               # convert string to uppercase for comparison

	if (incoming_checksum == calculated_checksum):                                  # Compare checksums
	    cs = "00"                                                                   # checksum pass flag for upstream
	else:
	    cs = "01"
	    ##return cs
	############# error check module1 (byte_count based) ###############
	packet_byte_count = hex (len(for_check[18:])/2)                                 # calculate byte count & convert to hex
	calculated_byte_count =  packet_byte_count[2:].zfill(2)                         # remove `0x`, add leading 0 with zfill(), if required
	calculated_byte_count = calculated_byte_count.upper()                           # convert string to uppercase for comparison

	if (incoming_byte_count == calculated_byte_count):                              # Compare bytecount
	    bc = "00"                                                                   # byte count pass flag
	else:
	    bc = "01"
	    ##return bc
	############# error check module2 (value based) ###############

	################# error check module3 (? based) ################

	############## debugging information #################
	if (script_arg == "--debug"):
			print ("Incoming packet: " + (in_bytes))                                     # Print packet length
			print ("Debug information")
			print ("Packet length: " + str(packet_len) + " Bytes")                       # int to string conversion & concatenation
			print ("Slave address: " + (slave_id))                                       
			print ("Command code: " + (command_code))
			print ("Data Bytes: " + (data_bytes))
			print ("Total number of Data Bytes: " + str(data_bytes_count) + " Bytes")    
			print ("Checksum input: " + (for_check))                                     # print bytestream for checksum calculation
			print ("Incoming checksum: " + (incoming_checksum))
			print ("calculated checksum: " + (calculated_checksum))                       
			print ("Incoming byte count: " + (incoming_byte_count))
			print ("calculated byte count: " + (calculated_byte_count)) 

	################# formatted upstream data ####################
	upstream_data = str(slave_id + command_code + data_bytes + cs + bc)     	# formatted string with checksum & byte count flag for upstream

	print ("\r \n")
	if (cs == "01"):
		print ("Error: Checksum Mismatch")
				                           
	if (bc == "01"):
		print ("Warning: Byte count Mismatch")

	if (cs == "00") and (bc == "00"):
		print ("Valid Datastream")
	print ("Upstream data: " + upstream_data)
	print ("----------------------------------------------")

while True:
    try:
		for i in range(8):
			if (len(sys.argv) == 1):
				data_fed = str(lines[i])
				print ("Reading information instance: " + str(i+1))
				upstream_data (data_fed, 0)
				time.sleep(2)				

			if (len(sys.argv) == 2):	
				cmdline_arg = sys.argv[1]
				if (cmdline_arg == "--debug"):
					data_fed = str(lines[i])
					print ("Reading information instance: " + str(i+1) + " with --Debug mode")
					upstream_data (data_fed, cmdline_arg)
					time.sleep(2)
				else:
					print ("Invalid argument")
					time.sleep(2)

			if ((len(sys.argv) >= 3)):
				print ("Invalid argument")
				time.sleep(2)

    except KeyboardInterrupt:
            print 'Interrupted'
            break



# https://www.guru99.com/reading-and-writing-files-in-python.html
# https://stackoverflow.com/q/845058
# https://www.w3schools.com/python/python_for_loops.asp
# https://www.programiz.com/python-programming/for-loop
# https://docs.python.org/2/library/stdtypes.html#str.zfill
# https://stackoverflow.com/a/15884750/12747885
# https://realpython.com/python-sleep/





