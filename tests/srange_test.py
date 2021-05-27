#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from srange import srange

__author__	=	"Jon Tischler, <tischler@aps.anl.gov>, " +\
				"Christian M. Schlepuetz," +\
				"Argonne National Laboratory"
__copyright__ = 'Copyright (c) 2021, Argonne National Laboratory'
__license__ = 'See license file'
__docformat__ = 'restructuredtext en'

"""
For  testing srange.py.
Test cases for srange class to verify correct behavior.

testGroup is a bit flag.

Testing Examples:
	./srange_test.py 1			# runs first testGroup (1)
	./srange_test.py 5			# runs first and third testGroup (1+4=5)
	./srange_test.py 2			# runs second testGroup (1)
	./srange_test.py -1			# runs all testGroups
"""

try:
	testGroup = int(sys.argv[1])
	error = False
except:
	error = True

if error: raise ValueError('./srange testGroup,  testGroup must be an integer')
print('\n****************************************************************\n')
print('showing testGroup = %r,   using python %r' % (testGroup,sys.version_info[0]))
TotalErrorCount = 0

def test(test_str, bad=False):
	"""
	Test function for the srange class.
	"""
	global TotalErrorCount
	print('\n---------------------------------------------')
	print("The test input: %r,   type=%r" % (test_str,type(test_str)))

	try:
		sr = srange(test_str)
		mystr = ''
		for val in sr:						# this tests the srange.next() method, iterator
			mystr += str(val) + ', '
		print('Elements of str1: ', mystr)
		print('Python list of elements in str1:', sr.list())
		print('  internal representation: ', sr.l)
		print('String representation:', repr(sr))
		print('String value:', str(sr))
		print('first and last elements are [%g, %g], %g elements' % (sr.first(), sr.last(), sr.len()))
		print('Next element after 5:', sr.after(5))
		print('Next element after 16:', sr.after(16))
		print('Test if 5 is in range:', sr.is_in_range(5))
		print('Test if 6 is in range:', sr.is_in_range(6))
		print('Subrange from -1 with 100 elements: ', sr.sub_range(-1,100))
		print('Subrange from 3 with 5 elements: ', sr.sub_range(3,5))
		print('Index of 5 in string range:', sr.val2index(5))
		print('Value at index 3 in string range:', sr.index(3))

	except Exception as err:
		if bad:
			print('         This test was supposed to return an ERROR!')
			print('         ',err)
		else:
			TotalErrorCount += 1
			print('ERROR -- This test returned an ERROR!')
			print(err)

if testGroup & 1:
	print('\n\n========== Simple tests of string range ==========\n\n')
	test('1,3,4-5,8-11,12-13,20')			# a standard string range
	test('1, 3,   	 4-5,8 - 11, 12-13,20')	# test for dealing with whitespace (contains tab & spaces)
	test('2,1,3')							# illegal, since non-monotonic
	test('5')								# string range with single element
	test('5,6')								# string range with two consecutive numbers
	test('', bad=True)						# empty string
	test(3.65, bad=True)					# illegal type (should be str)
	test('3.65', bad=True)					# illegal value (should be integer)
	test('-3-3, 5-11')						# negative values
	test([3, 5, 9, 10, 11, 12])				# a list as input
	test([3.141, 6.282, 21.163], bad=True)	# illegal, list of non-integers
	try:
		import numpy
		test(numpy.array([3,5,9,10,11,12]))	# numpy array instead of just a list
	except:
		pass

if testGroup & 2:							# tests of stride
	print('\n\n========== Tests of string range with stride ==========\n\n')
	test('1-10:2')							# very simple test
	test('1-7:2,9-13:2')					# test concatenating
	test('1,2,3,4,5')
	test('0,2,4,6,8')
	test('1-7:2, 9-13:2')
	test('1-7:2, 9-13:2, 15-19:2')
	test('1,3-7:2,9')
	test('1-5:1')
	test('1-5:2, 7-7:1')
	test('1,3,5,7, 10,12,14,16, 18-20:2')
	test('0,3,6,9,12')						# test when stride > 2
	test('1-5:2, 7-7:0', bad=True)			# a zero stride, not Allowed
	test('1-5:2, 7-7:-1', bad=True)			# a negative stride, not Allowed
	test('1-5:1.1', bad=True)				# a non-integral stride, not Allowed

if testGroup & 4:							# tests of auto_reset
	print('\n\n========== Tests of string range with auto_reset ==========\n\n')
	s = srange('5-7',auto_reset=True)
	for i in s:
		print('  ',i)
	for i in s:
		print('    ',i)

	print('\n---------------------------------------------')
	s = srange('1-5',auto_reset=False)
	print(' start first loop, "for in s:"')
	for i in s:
		if i == 2:
			print('   break at i =',i)
			break
		print('  ',i)
	print('at end of first loop,  previous_item = %r,   start second loop "for i in s:"' % s.previous_item)
	for i in s:
		print('  ',i)

if TotalErrorCount > 0:	print('\nTotal number of real Errors is: %d' % TotalErrorCount)
else:					print('\nAll OK, No Errors')
