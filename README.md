Python converter script that takes a binary image file of the 32 KiB ROM of a Grundig VHS VCR machine 
of the mid 1990ies with the proprietary "Archiv-System" and outputs some hopefully useful text on the console.

INPUT:
1. : File "EEPROM_28C256.BIN"

OUTPUT:
1. : Clip titles, hh:mm positions etc. in order as found in ROM
2. : Histogram over found tape lengths
3. : Found cassette numbers
4. : Re-ordered by (A) cassette number and (B) order within each tape by start position

Condition: "Worked for my input file"
