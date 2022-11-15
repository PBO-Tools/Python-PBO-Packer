import os
import sys
import pprint
import struct
from datetime import datetime

#we need a default location set

class PackingUtils:
    
    @staticmethod
    def int_to_bytes(i: int, *, signed: bool = False) -> bytes:
        length = ((i + ((i * signed) < 0)).bit_length() + 7 + signed) // 8
        return i.to_bytes(length, byteorder='big', signed=signed)
    
    @staticmethod
    def writeStr(pbo, string):
        pbo.write(str(string).encode('utf-8'))
        PackingUtils.writeNull(pbo)

    @staticmethod
    def writeNull(pbo):
        pbo.write(struct.pack('x'))

    @staticmethod
    def writeInt(pbo, num):
        pbo.write(num.to_bytes(4, byteorder='little'))
    
    @staticmethod
    def writeUInt(pbo, num):
        pbo.write(num.to_bytes(4, byteorder='litte'))
    
    @staticmethod
    def writeByte(pbo, num):
        pbo.write(struct.pack('B', num))

    @staticmethod
    def writeBytes(pbo, num, amount):
        for x in range(amount):
            pbo.write(struct.pack('B', num))

class FileEntry:
    fileName = ""
    diskPath = ""
    packingType = 0
    data = []
    originalSize = 0;
    offset = 0;
    timestamp = 0;
    dataSize = 0;
    dataCompressed = [];
    
    def __init__(self, name, winPath, entryData, packingType):
        self.fileName = name
        self.diskPath = winPath;
        self.data = entryData;
        self.packingType = packingType;
        self.repopulate()
        #self.originalSize = size
        #print(self.data)
        
    #def __init__(self, name, winPath, packingType):
    #    self.fileName = name
    #    self.diskPath = winPath;
    #    self.data = b'';
    #    self.packingType = packingType;

            
    def repopulate(self):
        print(len(self.data))
        self.originalSize = len(self.data)
        self.offset = 0
        self.timestamp = int(round(datetime.now().timestamp()))
        if (self.packingType == 0):
            self.dataSize = self.originalSize
            self.dataCompressed = b''
        elif(self.packingType == 1131442803):
            # not coded atm
            return
        else:
            return

def WritePbo(folder, files):
    print("Writing headers...")
    with open(folder + "-packed.pbo", "wb") as pbo:
        PackingUtils.writeNull(pbo)
        PackingUtils.writeStr(pbo, 'sreV')
        for i in range(0,15):
            PackingUtils.writeNull(pbo)
        PackingUtils.writeStr(pbo, "product");
        PackingUtils.writeStr(pbo, "dayz ugc");
        PackingUtils.writeStr(pbo, "prefix\0"+ os.path.basename(os.path.normpath(folder)))
        print("Writing Metadata for File Entries...")
        PackingUtils.writeNull(pbo)
        for f in files:
            print("Debug: {}".format(f.fileName))
            print("Debug: {}".format(f.packingType))
            print("Debug: {}".format(f.originalSize))
            print("Debug: {}".format(f.offset))
            print("Debug: {}".format(f.timestamp))
            print("Debug: {}".format(f.dataSize))
            print()
            PackingUtils.writeStr(pbo, f.fileName)
            PackingUtils.writeByte(pbo, f.packingType)
            PackingUtils.writeUInt(pbo, f.originalSize)
            PackingUtils.writeByte(pbo, f.offset)
            PackingUtils.writeUInt(pbo, f.timestamp)
            PackingUtils.writeUInt(pbo, f.dataSize)
        PackingUtils.writeStr(pbo, "")
        PackingUtils.writeNull(pbo)
        PackingUtils.writeNull(pbo)
        PackingUtils.writeNull(pbo)
        PackingUtils.writeNull(pbo)
        PackingUtils.writeNull(pbo)
        for f in files:
            #PackingUtils.write(pbo, f.data)
            pbo.write(f.data)
        print("Done...")
        

folder = sys.argv[1]
if not os.path.exists(folder):
    exit("Source not found.")

allowed_ext = ['.c', '.cpp']

files = []
workingwith = []
# r=root, d=directories, f = files
for r, d, f in os.walk(folder):
    for file in f:
        if [ext for ext in allowed_ext if ext in file]:
            fh = open(os.path.join(r, file), 'rb')
            ba = fh.read()
            filename = os.path.join(r, file).replace(folder+ "/", "")
            files.append(
                FileEntry(
                    filename,
                    file,
                    ba,
                    0
                )
            )

pprint.pprint(files)
WritePbo(folder, files)