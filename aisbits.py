#
#    CFNS - Rijkswaterstaat CIV, Delft © 2020 - 2021 <cfns@rws.nl>
#
#    Copyright 2020 - 2021 Alfred Espinosa Encarnación <alfred.espinosaencarnacion@rws.nl>
#
#    This file is part of cfns-half-duplex
#
#    cfns-half-duplex is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    cfns-half-duplex is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with cfns-half-duplex. If not, see <https://www.gnu.org/licenses/>.
#

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
