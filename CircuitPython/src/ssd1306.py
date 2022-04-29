import time
from micropython import const
import i2c_device
import os
import struct
import busio
import board

class BitmapFont:
    """class for reading font file"""
    def __init__(self, font_name="font5x8.bin"):

        self.font_name = font_name
        try:
            self._font = open(self.font_name, "rb")
            self.font_width, self.font_height = struct.unpack("BB", self._font.read(2))
            # simple font file validation check based on expected file size
            if 2 + 256 * self.font_width != os.stat(font_name)[6]:
                raise RuntimeError("Invalid font file: " + font_name)
        except OSError:
            print("Could not find font file", font_name)
            raise
        except OverflowError:
            pass

    def deinit(self):
        """Close the font file as cleanup."""
        self._font.close()

    def __enter__(self):
        """Initialize/open the font file"""
        self.__init__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """cleanup on exit"""
        self.deinit()
                    
    def get(self, string):  
        out = bytearray()
        for char in string:
            for char_x in range(self.font_width):
                # Grab the byte for the current column of font data.
                self._font.seek(2 + (ord(char) * self.font_width) + char_x)
                try:
                    out.append(struct.unpack("B", self._font.read(1))[0])
                except RuntimeError:
                    continue  # maybe character isnt there? go to next
            out.append(0)
        return out

    def width(self, text):
        """Return the pixel width of the specified text message."""
        return len(text) * (self.font_width + 1)

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)
SET_ZOOM = const(0xD6)

class _SSD1306:
    """Base class for SSD1306 display driver"""

    # pylint: disable-msg=too-many-arguments
    def __init__(self, width, height, *, external_vcc, reset, page_addressing, font_name="font5x8.bin"):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        # reset may be None if not needed
        self.reset_pin = reset
        self.page_addressing = page_addressing
        if self.reset_pin:
            self.reset_pin.switch_to_output(value=0)
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self._power = False
        # Parameters for efficient Page Addressing Mode (typical of U8Glib libraries)
        # Important as not all screens appear to support Horizontal Addressing Mode
        if self.page_addressing:
            raise NotImplementedError
        else:
            self.pagebuffer = None
            self.page_column_start = None
        # font
        self.font = BitmapFont(font_name=font_name)
        # Let's get moving!
        self.poweron()
        self.init_display()

    @property
    def power(self):
        """True if the display is currently powered on, otherwise False"""
        return self._power

    def init_display(self):
        """Base class to initialize display"""
        # The various screen sizes available with the ssd1306 OLED driver
        # chip require differing configuration values for the display clock
        # div and com pin, which are listed below for reference and future
        # compatibility:
        #    w,  h: DISP_CLK_DIV  COM_PIN_CFG
        #  128, 64:         0x80         0x12
        #  128, 32:         0x80         0x02
        #   96, 16:         0x60         0x02
        #   64, 48:         0x80         0x12
        #   64, 32:         0x80         0x12
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_MEM_ADDR,
            0x10  # Page Addressing Mode
            if self.page_addressing
            else 0x00,  # Horizontal Addressing Mode
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02
            if (self.height == 32 or self.height == 16) and (self.width != 64)
            else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc  # n.b. specs for ssd1306 64x32 oled screens imply this should be 0x40
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
            SET_ZOOM,
            0x01
        ):  # on
            self.write_cmd(cmd)
        if self.width == 72:
            self.write_cmd(0xAD)
            self.write_cmd(0x30)
        self.clear()

    def poweroff(self):
        """Turn off the display (nothing visible)"""
        self.write_cmd(SET_DISP | 0x00)
        self._power = False

    def invert(self, invert):
        """Invert all pixels on the display"""
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate: bool) -> None:
        """Rotate the display 0 or 180 degrees"""
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (rotate & 1))

    def contrast(self, contrast: int) -> None:
        """Adjust the contrast"""
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def write_cmd(self, cmd):
        """Derived class must implement this"""
        raise NotImplementedError

    def poweron(self):
        "Reset device and turn on the display."
        if self.reset_pin:
            self.reset_pin.value = 1
            time.sleep(0.001)
            self.reset_pin.value = 0
            time.sleep(0.010)
            self.reset_pin.value = 1
            time.sleep(0.010)
        self.write_cmd(SET_DISP | 0x01)
        self._power = True

    def set_cursor(self, x, y):
        """Update the display"""
        if not self.page_addressing:
            xpos0 = x
            xpos1 = self.width - 1
            if self.width == 64:
                # displays with width of 64 pixels are shifted by 32
                xpos0 += 32
                xpos1 += 32
            if self.width == 72:
                # displays with width of 72 pixels are shifted by 28
                xpos0 += 28
                xpos1 += 28
            self.write_cmd(SET_COL_ADDR)
            self.write_cmd(xpos0)
            self.write_cmd(xpos1)
            self.write_cmd(SET_PAGE_ADDR)
            self.write_cmd(y)
            self.write_cmd(self.pages - 1)

xiaoi2c = busio.I2C(board.SCL, board.SDA, frequency=int(1e6))

class SSD1306_I2C(_SSD1306):
    """ I2C class for SSD1306 """

    def __init__(
        self,
        width=128,
        height=64,
        i2c=xiaoi2c,
        addr=0x3C,
        external_vcc=False,
        reset=None,
        page_addressing=False,
        font_name="font5x8.bin",
    ):
        self.i2c_device = i2c_device.I2CDevice(i2c, addr)
        self.addr = addr
        self.page_addressing = page_addressing
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        super().__init__(
            width,
            height,
            external_vcc=external_vcc,
            reset=reset,
            page_addressing=self.page_addressing,
            font_name=font_name,
        )

    def write_cmd(self, cmd):
        """Send a command to the I2C device"""
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        with self.i2c_device:
            self.i2c_device.write(self.temp)
    
    def print(self, string, x=0, y=0, clrhead=False, clrtail=False):
        if self.page_addressing:
            raise NotImplementedError
        # message buffer
        message = bytearray([0x40])
        # set head
        if clrhead:
            message += bytearray([0x00] * x)
            self.set_cursor(0, y)
        else:
            self.set_cursor(x, y)
        # set body
        message += self.font.get(str(string))
        # set tail
        if clrtail:
            message += bytearray([0x00] * (129 - len(message)))
        # send
        with self.i2c_device:
            self.i2c_device.write(message)
    
    def clear(self):
        for i in range(4):
            self.print("", clrtail=True, y=i)