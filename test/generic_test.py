import AV_Shield.generic as generic

print "Testing Generic Module..."

print " - Testing vprint:"
assert generic.vprint ("test_print_ok", 1)
assert !generic.vprint ("test_print_fail", 0)

print "'generic' module test passed"

