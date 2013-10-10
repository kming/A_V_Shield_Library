import Adafruit_BBIO.PWM as PWM
import threading

# Define reading input
def read_input():
	return raw_input("Press Enter to proceed")

# Starting from a 10KHz and scaling by 10KHz everycycle of the loop. 
frequency = 10000
freq_increment = 10000

PWM.start("P9_14", frequency)
t_read_input = Thread(target=read_input)
started = 0;
while True:
	if started == 0:
		t_read_input.start()
		started = 1
		print "Frequency: %d kHz: Press Enter to increase Frequency" % (frequency/1000)

	if (t_read_input.is_alive() == False) && (started == 1):
		started = 0
		frequency = frequency + freq_increment
		PWM.set_frequency("P9_14",frequency)


	
	
		
	
	
	

