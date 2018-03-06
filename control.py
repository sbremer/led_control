import time
from neopixel import Color, Adafruit_NeoPixel
import _rpi_ws281x as ws
from control_aux import wheel, convert_K_to_RGB

# LED strip configuration:
LED_COUNT = 118         # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
LED_DMA = 1             # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = True       # True to invert the signal (when using NPN transistor level shift)


class Control:
    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0,
                                  ws.WS2812_STRIP)
        self.strip.begin()
        self.running = True

    def color_temp(self, temp, brightness=1.0):
        r, g, b = convert_K_to_RGB(temp)
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)

        self.color(r, g, b)

    def color(self, r, g, b):
        color = Color(r, g, b)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        while True:
            self.strip.show()
            if self.running:
                time.sleep(20 / 1000.0)
            else:
                return

    def rainbow(self):
        while True:
            for j in range(256):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, wheel((i + j) & 255))

                self.strip.show()
                if self.running:
                    time.sleep(20 / 1000.0)
                else:
                    return

    def rainbow_onecolor(self):
        while True:
            for j in range(256):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, wheel(j & 255))

                self.strip.show()
                if self.running:
                    time.sleep(20 / 1000.0)
                else:
                    return
