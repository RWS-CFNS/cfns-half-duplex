from aisutils import binary, nmea
from aisutils.BitVector import BitVector

msg = 'Alfred'
aisBits = BitVector(textstring=msg)
payloadStr, pad = binary.bitvectoais6(aisBits)  # [0]

print(payloadStr)

padding = binary.getPadding(payloadStr)
check = binary.ais6tobitvec(payloadStr,0)
if aisBits == check:
    print("True")
    buffer = nmea.bbmEncode(1, 1, 0, 1, 8, payloadStr, pad, appendEOL=False)
    print(buffer)
