# Import test python module


# Debugging Output
print "Testing Audio WAV objects..."

# Test each individual function within the python module
print " - Testing chunk declaration and get_id"
new_chunk = wav.chunk("RIFF")
assert (new_chunk.get_id() == "RIFF")
print "   - Testing append_value, data_to_string"
new_chunk.append_value('1')
new_chunk.append_value(str(unichr(107)))
new_chunk.append_value('a')
new_chunk.append_value(str(unichr(107)))

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

new_chunk._align=False
size = new_chunk.get_data_size()
assert (size == 5)
assert ((new_chunk.get_total_size()-size) == 8)

# Test End
print "'audio_wav_object' module test passed"
