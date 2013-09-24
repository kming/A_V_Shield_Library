import AV_Shield.setup as setup

print "Testing setup..."

print " - Testing general_setup"
assert !setup.general_setup
print " - Testing video_setup"
assert !setup.video_setup
print " - Testing audio_setup"
assert !setup.audio_setup
print " - Testing setup"
assert !setup.setup

print "'setup' module test passed"
