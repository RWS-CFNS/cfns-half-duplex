import serial
rx_carbon_port = "COM4"
carbon_pro_port = "COM12"
carbon_pro = serial.Serial(
    port=carbon_pro_port, baudrate=38400, bytesize=8, stopbits=serial.STOPBITS_ONE
)
carbon_pro.flushInput()

rx_carbon = serial.Serial(
    port=rx_carbon_port, baudrate=38400, bytesize=8, stopbits=serial.STOPBITS_ONE
)
rx_carbon.flushInput()

print("Serial is open: " + str(carbon_pro.isOpen()))
print("Now Writing")
carbon_pro.write(b'!AIABM,1,1,0,244123459,1,12,D89CP9CP1PD5CDP=5CC175,4*4A')
# print("Did write, now read")
# x = ser_six.readline()
# print(x)

# print("Serial is open: " + str(ser_four.isOpen()))
# print("Now Writing")
# ser_four.write("!AIVDM,1,1,,A,10`lQ3hP000EfQ@N7REv4?wF25B4,0*23".encode())
# print("Did write, now read")
# x = ser_four.readline()
# print(x)

while True:
    try:
        print("Writing to transponder")
        carbon_pro.write(b'!AIABM,1,1,0,244123459,1,12,D89CP9CP1PD5CDP=5CC175,4*4A')

        print("Reading from receiver")
        ser_bytes = carbon_pro.readline()
        print(ser_bytes)
    except:
        print("Keyboard Interrupt")
        break