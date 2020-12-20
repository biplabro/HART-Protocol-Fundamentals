packet = 'FFFFFFFFFF0686010700000843F0000076'                                   # Incoming Packet from HART transmitter
print ("Packet length " + str(len(packet)) + " nibbles")                        # Print packet length
for_check = packet [0:(len(packet)-2)]                                          # Separated data, excluding the checksum byte
incoming_checksum = packet [-2:]                                                # Last byte (FF) is incoming checksum
print ("incoming packet is: " + (packet))
print ("incoming checksum is: " + (incoming_checksum))
print ("checksum input is: " + (for_check))                                     # print bytestream for checksum calculation

xor = 0                                                                         # value initiated with 0
i = 0                                                                           # index initiated with 0
while i < len(for_check):                                                       # initiate xor operation till length of the data
    xor = xor ^ ord(for_check[i])                                               # Bitwise xor
    i += 1                                                                      # move pointer to next value

checksum = hex (xor)                                                            # outputs 0xFF format
calculated_checksum = checksum[2:]                                              # formatting checksum data
print ("calculated checksum is " + (calculated_checksum))                       

if (incoming_checksum == calculated_checksum):                                  # Compare checksums
    print ("Checksum Match")                                                    # print result
else:
    print ("Checksum Mismatch")                                           



# calculated checksum value is 0x77
# incoming checksum is 0x76 (for debug purpuse)
# edit the incoming packet to get "Checksum Match" confirmation
