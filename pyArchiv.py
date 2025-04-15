#  v0.08  approx. january 2024  rtob  github upload

fnIn = "EEPROM_28C256.BIN"

posStart1 = 0x114e
posStart2 = 0x12a0

posStop  = 0x6840
strSize =      30
recSize  =     40

genreDict = {
    0x0 : "DIVERS",
    0x1 : "TIERE ",
    0x2 : "LEER  ",
    0x3 : "FILM  ",
    0x4 : "ACTION",
    0x5 : "KRIMI ",
    0x6 : "HUMOR ",
    0x7 : "KRIEG ",
    0x8 : "HORROR",
    0x9 : "VIDEO ",
    0xA : "NEU   ",
    0xB : "HiFi  ",
    0xC : "LIVE  ",
    0xD : "SciFi ",
    0xE : "ADVENT",
    0xF : "      ",
}

sonder = {
0x7e : 'ß',
0x7b : 'ä',  # doppeltes ä ?
0x92 : 'ä',  # doppeltes ä ?
0x98 : 'ö',  # auch Ö?
0x7d : 'ü',  # doppeltes ü ?
0x9a : 'ü',  # doppeltes ü ?
0xcb : '#',  # 1/2
0x8c : '²',  #?
}






fIn = open(fnIn, "rb").read()

#print( fIn )


#for p in range(20):


tapeList = {}

print("\neinträge in reihenfolge wie im EEPROM")
print()

analysisUniqueExt2 = {}
p = 0
while 1:
   pos = posStart2 + p * recSize
   if pos >= posStop:
      break
   x = fIn[pos:][:recSize]
   titel1 = x[7:][:strSize]
#   titel2 = titel1
   titel2 = ""
   for c in titel1:
#      print (c)
      r = chr(c)
      if c in sonder:
         r = sonder[c]
      titel2 += r
      TapeNo    = "{:x}{:02x}"          .format(x[0]&0x0f, x[1])
      timeStart = "{:x}:{:02x}"         .format(x[3]     , x[4])
      timeStartMinutes = int(x[3]*60 + x[4])
      timeEnd   = "{:x}:{:02x}"         .format(x[5]     , x[6])
      datum     = "{:02x}.{:02x}.{:02x}".format(x[-3],x[-2],x[-1])
#      ext1      = "{:x}"                .format(x[0]>>4)
      ext1      =  x[0]>>4
#      ext2      = "{:02x}"              .format(x[2])
      ext2      = x[2]
      invalid  = ['-','X'][ (x[0]&0x0f)==0xf ]
      genre = genreDict[ext1]
#   titel2 = titel1.decode("cp1252")

   ext2Comment = ''
   if   ext2 == 249: ext2Comment = "E-265"
   elif ext2 == 250: ext2Comment = "E-305"
   elif ext2 >  245: ext2Comment = "over"

   entryString = "{:4}  {}  {:3} {}-{}  {}  {:x}->'{}'  {:02x} / {:3} / {:5}  {}  '{}'".format(p, TapeNo, timeStartMinutes, timeStart, timeEnd, datum, ext1, genre, ext2,ext2, ext2Comment, invalid, titel2)
   print( entryString )

   if TapeNo=="fee":
      virtualTapeNo = 1000
   else:
      virtualTapeNo = int(TapeNo)

   if virtualTapeNo not in tapeList:
      tapeList[virtualTapeNo] =     [ [timeStartMinutes, entryString] ]
   else:
      tapeList[virtualTapeNo].append( [timeStartMinutes, entryString] )


   if ext2 in analysisUniqueExt2:
      analysisUniqueExt2[ext2] += 1
   else:
      analysisUniqueExt2[ext2]  = 1

   p+=1


print("\nbandlaengen histogramm")
print()
for ext2 in sorted(analysisUniqueExt2.keys()):
   v = analysisUniqueExt2[ext2]
   print("{:02x} / {:3} / {:08b} : {:3}".format(ext2,ext2,ext2,  v))


print("\ncassette numbers")
cassNoList = sorted(tapeList.keys())
print()
print(cassNoList)

print("\neintraege nach kassetten-nummer")
print()
for c in cassNoList:
    print("{:4}:".format(c))
#    print(tapeList[c])
    for content in sorted(tapeList[c]):
        print("      {}".format(content[1]))
#print(tapeList)
