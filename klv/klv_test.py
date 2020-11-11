
import sys
import klvdata





with open("day_flight_mpg_klv_data.out", 'rb') as f: 
    for packet in klvdata.StreamParser(f):
        print()
        print("----------------- packet.structure(): ---------------------")
        print(packet.structure())
        print("---------------- packet.MetdataList(): --------------------")
        print(packet.MetadataList())




# for packet in klvdata.StreamParser(sys.stdin.buffer.read()): 
#     print()
#     print("----------------- PACKET: ---------------------")
#     print(packet.structure())

