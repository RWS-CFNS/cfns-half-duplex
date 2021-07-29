from smbus2 import SMBus, i2c_msg


class I2C:
    def __init__(self):
        self.address = 0
        self.bus = SMBus()

    def get_address(self):
        return self.address

    def set_address(self, new_address):
        self.address = new_address

    def init_i2c(self, address):
        self.address = address
        self.bus = SMBus(1)

    def list_i2c(self):
        for device in range(128):
            try:
                msg = i2c_msg.write(device, [64])
                self.bus.i2c_rdwr(msg)
                self.bus.read_byte(device)
                print(device)
            except:
                print("No device connected to bus")
                pass

    def write_i2c(self, dab_id, message_type, data):
        try:
            # Write a single byte to address 80
            buff = []
            buff.append(dab_id)
            buff.append(message_type)
            if data:
                buff.append(data[0])
            msg = i2c_msg.write(self.address, buff)
            self.bus.i2c_rdwr(msg)
            print("I2C data send for acknowledgement: ", buff)
        except:
            print("Could not send by I2C")
            pass

    def read_i2c(self):
        # Read 64 bytes from address 80
        msg = i2c_msg.read(self.address, 64)
        self.bus.i2c_rdwr(msg)
        return msg