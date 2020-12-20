packet = 'FFFFFFFFFF0686010700000843F00000'                                     # Incoming Packet
PL = "Packet length " + str(len(packet)) + " nibbles"                           # concatenate packet length
print (PL)                                                                      # Print packet length

xor = 0                                                                         # value initiated with 0
i = 0                                                                           # index initiated with 0
while i < len(packet):                                                          # initiate xor operation till length of the data
    xor = xor ^ ord(packet[i])                                                  # Bitwise xor
    i += 1                                                                      # move pointer to next value

checksum = hex (xor)                                                            # outputs 0xFF format
final = checksum[2:4]                                                           # formatting required data
print (final)                                                                   # print the formatted data




