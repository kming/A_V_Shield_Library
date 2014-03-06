###############################################################
#
#	audio.py -- common audio functionality --> Setup in setup.py
#
#	By: Kei-Ming Kwong 2013
#
###############################################################

#import Adafruit_BBIO.ADC as ADC
import generic as generic
import Adafruit_BBIO.SPI as SPI
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

# Constant Definition
verbose = False
class bbb_SPI:
	_adc = ""
	_data_file = ""
	_file_lock = False
	_pin_setup = {}
	def __init__ (self):
		self._adc = SPI(0,0)		# Use SPI0 as the main protocol to communicate with the ADC
		self._data_file = "" 		# Write to a temporary data file
		self._file_lock = True
		
	def setup_spi_protocol (self, max_freq, bpw=8, cs_high=False, threewire=False, loopback=False, mode=0):
		self._adc.msh = max_freq
		self._adc.bpw = bpw
		self._adc.cshigh = cs_high
		self._adc.threewire = threewire
		self._adc.loop = loopback
		self._adc.mode = mode
		if verbose:
			print "bpw\t{0}".format(self._adc.bpw)
			print "msh\t{0}".format(self._adc.msh)
			print "cshigh\t{0}".format(self._adc.cshigh)
			print "threewire\t{0}".format(self._adc.threewire)
			print "loop\t{0}".format(self._adc.loop)
			print "mode\t{0}".format(self._adc.mode)
	
	def read_till_stop(self, pin = "P8_14"):
		# Setup input control pin if it wasn't setup before
		if (not (pin in self._pin_setup) or (self._pin_setup[pin] is False)):
			GPIO.setup(pin, GPIO.IN)
			self._pin_setup[pin] = True
		
		# Setup output file
		self._data_file = open("data.sample", "w") 
		GPIO.add_event_detect(pin, GPIO.RISING)
		i = 0
		addr = {}
		
		# Write to output file until user input
		while (not GPIO.event_detected(pin)):
		    addr["{0}".format(i)] = [0]
			self._data_file.write(str(self._adc.xfer(addr[str(i)])[0]))	
			i = i+1
			
		
		# Cleanup GPIO and file handling
		self._data_file.close()
		GPIO.cleanup()
		
		
		
		
	
	
	
def raw_adc_input(pin_name):
	## PINS FOR ADC/AUDIO
	#"AIN4", "P9_33"
	#"AIN6", "P9_35"
	#"AIN5", "P9_36"
	#"AIN2", "P9_37"
	#"AIN3", "P9_38"
	#"AIN0", "P9_39"
	#"AIN1", "P9_40"
	#return ADC.read(pin_name)
	pass
	
# Need to do: write WAV Header, write WAV Data
def read_wav_file (full_file_path):

	return

