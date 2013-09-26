from ..lib import setup

print "Testing setup..."

print " - Testing general_setup"
assert (0 == setup.general_setup)
print " - Testing video_setup"
assert (0 == setup.video_setup)
print " - Testing audio_setup"
assert (0 == setup.audio_setup)
print " - Testing setup"
assert (0 == setup.setup)

print "'setup' module test passed"
