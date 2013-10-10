import Adafruit_BBIO.PWM as PWM
import threading as thread

input_list = []

# Define reading input
def read_input(pList):
	pList.append (raw_input("   - Input Value: "))
	return 0
#convert string to int, and invalid values, increment by 0
def convert_string(s):
	try:
		ret = int(s)
	except ValueError:
		print " - ERROR: Invalid frequency"
		ret = 0
	return ret

# Starting from a 10KHz and scaling by default 10KHz everycycle of the loop. 
frequency = 10000
freq_increment = 10000

PWM.start("P9_14", 50,frequency)
started = 0;
while True:
	if started == 0:
		t_read_input = thread.Thread(target=read_input, args=[input_list])
		started = 1
		print "Frequency: %d kHz" % (frequency/1000)
		print " - Enter a Frequency (kHz) to increment by the amount"
		print " - Enter 'q' or 'quit' to exit"
		t_read_input.start()

	if (not t_read_input.is_alive()) and  (started == 1):
		input_value = input_list.pop()
		input_value.rstrip()
		if (input_value == "q") or (input_value == "quit"):
			break
		else:
			freq_increment = convert_string(input_value)*1000
		started = 0
		frequency = frequency + freq_increment
		PWM.set_frequency("P9_14",frequency)
		
		
print "Cleaning Up PWM"
PWM.stop ("P9_14")
PWM.cleanup()



	
	
		
	
	
	

