import os
import sys
import struct
from datetime import datetime


class PackingUtils:
    @staticmethod
    def writeStr(pbo, string):
        try:
            pbo.write(str(string).encode('utf-8'))
            PackingUtils.writeNull(pbo)
        except Exception as e:
            print(f"Error writing string to PBO: {e}")
            sys.exit(1)
            
    @staticmethod
    def writeNull(pbo):
        try:
            pbo.write(struct.pack('x'))
        except Exception as e:
            print(f"Error writing null to PBO: {e}")
            sys.exit(1)
        
    @staticmethod
    def writeInt(pbo, num):
        try:
            pbo.write(num.to_bytes(4, byteorder='little'))
        except Exception as e:
            print(f"Error writing integer to PBO: {e}")
            sys.exit(1)
        
    @staticmethod
    def writeUInt(pbo, num):
        try:
            pbo.write(num.to_bytes(4, byteorder='little'))
        except Exception as e:
            print(f"Error writing unsigned integer to PBO: {e}")
            sys.exit(1)
        
    @staticmethod
    def writeByte(pbo, num):
        try:
            pbo.write(struct.pack('B', num))
        except Exception as e:
            print(f"Error writing byte to PBO: {e}")
            sys.exit(1)
        
    @staticmethod
    def writeBytes(pbo, num, amount):
        try:
            for _ in range(amount):
                pbo.write(struct.pack('B', num))
        except Exception as e:
            print(f"Error writing bytes to PBO: {e}")
            sys.exit(1)


class FileEntry:
    def __init__(self, name, winPath, entryData, packingType):
        self.fileName = name
        self.diskPath = winPath
        self.data = entryData
        self.packingType = packingType
        self.repopulate()
        
    def repopulate(self):
        self.originalSize = len(self.data)
        self.offset = 0
        self.timestamp = int(round(datetime.now().timestamp()))
        if self.packingType == 0:
            self.dataSize = self.originalSize
            self.dataCompressed = b''
        else:
            # Additional error handling could be placed here
            print("Unsupported packing type.")
            sys.exit(1)


def WritePbo(folder, files):
    print("Writing headers...")
    with open(folder + "-packed.pbo", "wb") as pbo:
        try:
            for _ in range(20):
                PackingUtils.writeNull(pbo)
            for info in ["sreV", "product", "dayz ugc", "prefix\0" + os.path.basename(os.path.normpath(folder))]:
                PackingUtils.writeStr(pbo, info)
            for f in files:
                PackingUtils.writeStr(pbo, f.fileName)
                PackingUtils.writeByte(pbo, f.packingType)
                PackingUtils.writeUInt(pbo, f.originalSize)
                PackingUtils.writeByte(pbo, f.offset)
                PackingUtils.writeUInt(pbo, f.timestamp)
                PackingUtils.writeUInt(pbo, f.dataSize)
            for _ in range(5):
                PackingUtils.writeNull(pbo)
            for f in files:
                pbo.write(f.data)
            print("Done...")
        except Exception as e:
            print(f"Error while writing PBO: {e}")
            sys.exit(1)


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
        
    folder = sys.argv[1]
    if not os.path.exists(folder):
        sys.exit("Source folder not found.")

    allowed_ext = ['.c', '.cpp']

    files = []
    for r, d, f in os.walk(folder):
        for file in f:
            if any(ext in file for ext in allowed_ext):
                try:
                    with open(os.path.join(r, file), 'rb') as fh:
                        ba = fh.read()
                    filename = os.path.join(r, file).replace(folder + "/", "")
                    files.append(FileEntry(filename, file, ba, 0))
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
                    sys.exit(1)
    
    WritePbo(folder, files)


if __name__ == "__main__":
    main()
