###############################################################
#
#	main.py -- main program
#
#
###############################################################
import wave as wave
import random as random
import AV_Shield.lib.audio as audio
import AV_Shield.lib.audio_wav_file as wav
import time as time

recording = wav.wav()
recording.change_basic_fmt (1, 1, 44100, 8)

adc = audio.adc()
adc.setup_spi_protocol(1500000)
adc.setup_adc_clock("P9_14", 1500000)
adc.read_till_stop()

f = open ("data.sample", "r")
input = f.read()

for data in input:
	recording.append_data_value (data)

recording.export_to_file ("test_file.wav")




# Debugging Output
print "Testing Audio WAV objects..."

# Test each individual function within the python module
print " - Testing chunk declaration and get_id"
new_chunk = wav.chunk("RIFF")
assert (new_chunk.get_id() == "RIFF")
print "   - Testing append_value, data_to_string"
new_chunk.append_value('1')
new_chunk.append_value(str(unichr(107)))
new_chunk.append_value(0x6B61, 2)

data = new_chunk.data_to_string()
assert (data == "1kak")

print "   - Testing append_list"
new_chunk.clear_data()

new_list = list ('1' 'k' 'a' 'k')
new_chunk.append_list(new_list)

data = new_chunk.data_to_string()
assert (data == "1kak")

print "   - Testing append_string"
new_chunk.clear_data()
new_chunk.append_string("1kak")

data = new_chunk.data_to_string()
assert (data == "1kak")

print "   - Testing get_data_size, get_total_size"
size = new_chunk.get_data_size()
assert (size == 4)
assert ((new_chunk.get_total_size()-size) == 8)

# since it is word aligned, the data size should be ceiled to even number
new_chunk.append_value('1')
size = new_chunk.get_data_size()
assert (size == 6)
assert ((new_chunk.get_total_size()-size) == 8)

# force non alignment
new_chunk._align=False
new_chunk._dirty = True
size = new_chunk.get_data_size()
assert (size == 5)
assert ((new_chunk.get_total_size()-size) == 8)

new_wav = wav.wav()
new_wav.change_basic_fmt(1,1,8000,16)
for i in range (0, 10):
	new_wav.append_data_value (i+256*100+100)
#new_wav.export_data_to_list()
#new_wav.export_to_file("/home/kming/Desktop/A_V_Shield_Library/test.wav")
new_wav_ulaw = wav.wav()
new_wav_16 = wav.wav()
new_wav_ulaw.import_from_file("/home/kming/Desktop/A_V_Shield_Library/M1F1-mulaw-8bit.wav")
new_wav_16.import_from_file("/home/kming/Desktop/A_V_Shield_Library/M1F1-int16-16bit.wav")
new_wav_16.compress_mu_law()
#new_wav_ulaw.export_to_file("/home/keiming/Desktop/Thesis/github/A_V_Shield_Library/M1F1-mulaw-8bit_ex.wav")
new_wav_16.export_to_file("/home/kming/Desktop/A_V_Shield_Library/custom_compress.wav")
#print new_wav_16._print_fmt_debug_info()
#print new_wav_ulaw._print_fmt_debug_info()
#read_wav = wave.open("/home/kming/Desktop/A_V_Shield_Library/test.wav",'r')
#params = read_wav.getparams()
#print params
# Test End
print "'audio_wav_object' module test passed"
