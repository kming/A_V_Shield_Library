
from ..lib import generic

print "Testing Generic Module..."

print " - Testing vprint:"
assert (1 == generic.vprint ("test_print_ok", 1))
assert (0 == generic.vprint ("test_print_fail", 0))

print "'generic' module test passed"

