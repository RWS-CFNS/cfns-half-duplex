import spidev


class SPI:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi_bus = 0
        self.spi_device = 0

    def get_spi_bus(self):
        return self.spi_bus

    def set_spi_bus(self, new_spi_bus):
        self.spi_bus = new_spi_bus

    def get_spi_device(self):
        return self.spi_device

    def set_spi_device(self, new_spi_device):
        self.spi_device = new_spi_device

    def init_spi(self, spi_bus, spi_device):
        self.spi_bus = spi_bus
        self.spi_device = spi_device
        self.spi.max_speed_hz = 1000000

    def open_spi(self):
        self.spi.open(self.spi_bus, self.spi_device)

    def close_spi(self):
        self.spi.close()

    def write_spi(self, data, type):
        # Write a single byte to address 80
        buff = []
        buff.append(data)
        buff.append(type)
        self.spi.writebytes([buff])
        print("data send")

    def read_spi(self):
        # Read 64 bytes from address 80
        msg = self.spi.readbytes(64)
        return msg
