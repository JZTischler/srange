#!/usr/bin/env python
#
# test_symmtricRange.py
#
# $Id:    $
# $URL: $
#
# Part of the "pydiffract" package
#

import sys
import symmetricRange
__version__	=	"$Revision: $"
__author__	=	"Jon Tischler, <tischler@aps.anl.gov>" +\
				"Argonne National Laboratory"
__date__	=	"$Date: $"
__id__		=	"$Id: $"


""" Test cases for symmetricRange class to verify correct behavior. """
try:
		testGroup = int(sys.argv[1])
		error = testGroup < 1
except:	
		testGroup = -1
#		error = True	
#if error: raise ValueError('./symmetricRange testGroup, testGroup must be >0')
print 'showing testGroup = %r' % testGroup



def test(sr):
	""" Test function for the symmetricRange class. """
	print '\n---------------------------------------------'
	print 'Testing  ',sr
	try:
		mystr = ''
		for val in sr:					# this tests the symmetricRange.next() method, iterator
			mystr += str(val) + ', '
		print 'Elements of for loop: ', mystr
		li = sr.list()
		print 'Python list of elements in sr:', li, '   type=',type(li)
		print 'String representation:', repr(sr)
		print 'String value:', str(sr)
		print 'first and last elements are [%g, %g], %g elements' % (sr.first(), sr.last(), len(sr))
		print 'Next element after 0:', sr.after(0)
		print 'Next element after 3:', sr.after(3)
		print 'Next element after -3:', sr.after(-3)
		print 'Next element after 10:', sr.after(10)
		print 'Index of value=0 in range:', sr.val2index(0)
		print 'Index of value=4 in range:', sr.val2index(4)
		print 'Index of value=-4 in range:', sr.val2index(-4)
		print 'Index of value=20 in range:', sr.val2index(20)
		print 'Index of value=-1 in range:', sr.val2index(-1)
		print 'Value at index 0 in range:', sr[0]	# these also test sr.index(n) via __getitem__()
		print 'Value at index 3 in range:', sr[3]
		print 'Value at index 4 in range:', sr[4]
		print 'Value at index -1 in range:', sr[-1]

	except Exception as err:
		print 'This test returned an ERROR!'
		print err


if testGroup & 1:
	print '\n\n========== 1: Test of symmtric range, positive first ==========\n\n'
	sr = symmetricRange(5)
	test(sr)

if testGroup & 2:
	print '\n\n========== 2: Test of symmtric range, negative first ==========\n\n'
	sr = symmetricRange(5, negativeFirst=True)
	test(sr)

if testGroup & 4:
	print '\n\n========== 4: Test of symmtric range with input of 0 ==========\n\n'
	sr = symmetricRange(0)
	test(sr)


if testGroup & 8:
	print '\n\n========== 8: Tests of symmtric range with auto_reset ==========\n\n'
	s = symmetricRange(3,auto_reset=True)
	for i in s:
		print '  ',i
	for i in s:
		print '      ',i

	print '\n---------------------------------------------'
	s = symmetricRange(4,auto_reset=False)
	print ' start first loop, "for in s:"'
	for i in s:
		if i == 2:
			print '   break at i =',i
			break
		print '  ',i
	print 'at end of first loop,  previous = %r,   start second loop "for i in s:"' % s.previous
	for i in s:
		print '  ',i


if testGroup & 16:
	print '\n\n========== 16: Tests of invalid inputs to symmtric range ==========\n\n'
	try:
		sr = symmetricRange(-1)
		print 'sr =',sr
	except:	print sys.exc_info()[1]

	try:
		sr = symmetricRange(None)
		print 'sr =',sr
	except:	print sys.exc_info()[1]

	try:
		sr = symmetricRange('')
		print 'sr =',sr
	except:	print sys.exc_info()[1]

	try:
		sr = symmetricRange('ab')
		print 'sr =',sr
	except:	print sys.exc_info()[1]

	try:
		sr = symmetricRange(True)
		print 'sr =',sr
	except:	print sys.exc_info()[1]

	try:
		sr = symmetricRange(0)
		print 'sr =',sr
	except:	print sys.exc_info()[1]
