#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import sys

__author__	=	"Jon Tischler, <tischler@aps.anl.gov>, " +\
				"Christian M. Schlepuetz, " +\
				"Argonne National Laboratory"
__copyright__ = 'Copyright (c) 2021, Argonne National Laboratory'
__license__ = 'See license file'
__docformat__ = 'restructuredtext en'


class srange:
	"""
	String-range class.

	This class provides functions to convert a string representing integers and
	ranges of integers to an object which can be iterated over all the values
	contained in the string. Also, a list of individual values or subranges can
	be retrieved.

	The full range specification can be made of up multiple sub-ranges.
	Sub-ranges are comma-separated from each other and can either specify a
	single ingeger (e.g.: ``6``), a continuous range of integers by specifying
	the start and end point separated by a dash (e.g.: ``10-14``), or a
	continuous range of integers with a positive integer step size, also called
	a `stride`, which is separated from the start and end point by a colon
	(e.g.: ``20-35:5``). Note that the end points are always included in the
	range (somewhat contrary to the behavior of standard python ranges).

	Example
	-------
	.. code-block:: python

		sr = srange("1,3,4-5,8-11,12-18:2,25")
		for val in sr:
			print("%d," % val),
		1, 3, 4, 5, 8, 9, 10, 11, 12, 14, 16, 18, 25

	Note
	----
	String ranges can only contain integer numbers and should be strictly
	monotonically increasing. Multiple identical values are not allowed.
	The :meth:`_resort_list` method now allows for some degree of mis-ordered
	simple ranges, but they still must not overlap.

	Parameters
	----------
	range_string : str
		The string specifying the string range.
	auto_reset : bool, optional
		Flag to specify whether the srange object should be reset to its start
		value after iteration has been completed and the last element has been
		reached. This rewinds the object, so to speak. If not reset to the
		first element, the next call iteration will not yield any elements.
		When setting the flat to `True`, the behavior of srange will be
		analogous to those of standard lists and arrays. (default = True)

	"""

	#The range is checked to be monotonic, it returns None if no more values
	#last is the last number obtained from this range,
	#use -Inf to get start of range, it returns the next

	#The most useful variables and methods that you may be interested in at a
	#glance:

	#======================= ===================================================================================
	#variables of interest   description
	#======================= ===================================================================================
	#self.r                  the input string, after formatting and compacting
	#self.previous_item      the previous value produced, initially set very low
	#self.auto_reset         if True (default), then previous_item is reset to min at each call to __iter__
	#======================= ===================================================================================

	#======================= ===================================================================================
	#methods of interest     action
	#======================= ===================================================================================
	#next()                  returns next value, updates previous_item too
	#reset_previous()        reset the iterator so it starts with the first value
	#after(prev)             returns value that follows prev, without changing the current point in iteration
	#first()                 returns the first number in the range, for self.r="3,5,9-20", self.first() returns 3
	#last()                  returns the last number in the range, for self.r="3,5,9-20", self.last() returns 20
	#len()                   returns number of points in the range, for self.r="3,5,9-20", self.len() returns 14
	#is_in_range(m)          returns True if m is in self.r, otherwise False
	#index(ipnt)             return the ipntth number from range, first number is ipnt==0,  returns None if ipnt negative or too big
	#val2index(m)            returns index into r that corresponds to m. e.g. for r='3,5,9-20', m=5 returns 1.
	#sub_range(start,n,...)  returns a new range that is a sub range of current one, setLast=False
	#list(self)              returns a list where each element is a value in the range, CAUTION this can make a VERY big list
	#======================= ===================================================================================

	#======================= ================= ===================================================================
	#special methods         command           result using: sr = srange('1-4')
	#======================= ================= ===================================================================
	#__getitem__(n)          print(sr[2])     3
	#__len__()               print(len(sr))   4
	#__str__()               print(str(sr))   1-4
	#__repr__()              print(repr(sr))  srange('1-4', len=4, previous=0, auto_reset=True)
	#======================= ================= ===================================================================


	def __init__(self, range_string='', auto_reset=True):
		"""
		Initialize the srange instance.
		"""

		self.l = []
		''' The list of tupels defining the string range '''
		self.r = ''
		''' The string defining the string range '''

		r = range_string

		# Specify the integer type
		try:
			self.intTypes = (int, long)	# python2
		except:
			self.intTypes = (int)       # python3

		# Set the maximum integer representation available on the system.
		try:
			self.MAXINT = sys.maxint	# sys.maxint only exists in python2
		except:
			self.MAXINT = sys.maxsize	# for python3, maxsize is a good
		                                    # choice, = (2^63)-1

		# if a numpy array is passed for r, convert r to an integer array
		try:
			if isinstance(r[0], numpy.integer):
				r_int = []
				for i in r: r_int.append(int(i))
				r = r_int.copy()
		except:
			pass

		# convert input to a list of tuples
		# each tuple is one simple dash range, e.g. "1-17:2"
		try:
			if isinstance(r, unicode): r = r.encode()
		except:
			pass
		if isinstance(r, str):
			if r.lower() == 'none':
				r = ''
			self.l = self._string_to_tuple_list(r)
		elif isinstance(r, self.intTypes):
			r = int(r)
			self.l = [(r,r,1)]
			r = str(r)
		elif hasattr(r, '__iter__'):
			# this works for list and numpy.array, fails for strings
			self.l = self._list_to_srange(r)
		else:
			raise TypeError(
				"String list must be a string or (list of) integers.")

		if not self._is_monotonic():
			# try to sort the list to be monotonic
			self._resort_list()
			if not self._is_monotonic():
				raise ValueError("String range is unsortable.")

		try:
			self.auto_reset = bool(auto_reset)
		except:
			raise TypeError("auto_reset must be boolean")

		# set self.previous_item to number before first number in range
		self.reset_previous()
		self.l = self._compact(self.l)
		# make a string representation of list
		self.r = self._tuple_list_to_str(self.l)

	def __iter__(self):
		"""
		The class iterator
		"""

		if self.auto_reset:
			self.reset_previous()
		return self

	def __repr__(self):
		"""
		Return string representation for srange.
		"""

		try:
			length = self.len()
		except:
			length = None
		return "srange('%s', len=%r, previous=%r, auto_reset=%r)" % \
			(self.r, length, self.previous_item, self.auto_reset)

	def __str__(self):
		"""
		Return string value for srange.
		"""

		return self.r

	def __getitem__(self, n):
		"""
		Return the n-th element in the string range.
		"""

		return self.index(n)

	# this is required for the python3 iterator
	def __next__(self):
		"""
		Return the next value in the string range.

		Also update ``self.previous_item``.

		"""

		return self.next()

	# this is required for the python2 iterator
	def next(self):
		"""
		Return the next value in the string range.

		Also update ``self.previous_item``.

		Returns
		-------
		next_item : int
			The value of the next item of srange.

		"""

		if not self.l:
			raise StopIteration
		for (lo, hi, stride) in self.l:
			if self.previous_item < lo:
				self.previous_item = lo
				return lo
			elif self.previous_item >= lo and self.previous_item < hi:
				self.previous_item += \
					stride - ((self.previous_item-lo) % stride)
				return self.previous_item
		raise StopIteration

	def after(self, val):
		"""
		Return the value of the next element in srange after the given value.

		Parameters
		----------
		val : int
			The value after which the next value in the string range shoud be
			returned.

		Returns
		-------
		next_val : int
			The next value in the string range after the specified `val` value.

		Example
		-------
		.. code-block:: python

			>>> sr = srange("3,5,9-20")
			>>> print(sr.after(5))
			9

		"""

		if not self.l:
			return None
		previous_save = self.previous_item
		try:
			self.previous_item = int(val)
		except:
			raise ValueError("argument to srange.after() must be a number")
		try:
			after = self.next()
		except:
			after = None
		self.previous_item = previous_save
		return after

	def first(self):
		"""
		Return the number of the first item in the range.

		Returns
		-------
		first_item : int
			The value of the first item of srange.

		Example
		-------
		.. code-block:: python

			>>> sr = srange("3,5,9-20")
			>>> print(sr.first())
			3

		"""

		if not self.l:
			raise ValueError("String range is empty.")
		return (self.l[0])[0]

	def last(self):
		"""
		Return the value of the last item in the range.

		Returns
		-------
		last_item : int
			The value of the last item in srange.

		Example
		-------
		.. code-block:: python

			>>> sr = srange("3,5,9-20")
			>>> print(sr.last())
			20

		"""

		if not self.l:
			raise ValueError("String range is empty.")
		return (self.l[-1])[1]

	def len(self):
		"""
		Return the number of items in the string range.

		Returns
		-------
		len : int
			The length (i.e.: number or items) of srange.

		Example
		-------
		.. code-block:: python

			>>> sr = srange("3,5,9-20")
			>>> print(sr.len())
			14

		"""

		if not self.l:
			return 0

		total = 0
		for (lo, hi, stride) in self.l:
			total += int((hi-lo)/stride) + 1
		return total

	def __len__(self):
		"""
		Return the number of items in the string range.

		This is complementary to :meth:`len`, so you can use ``sr.len()`` or
		``len(sr)``.

		Returns
		-------
		len : int
			The length (i.e.: number or items) of srange.

		"""

		return self.len()

	def is_in_range(self, item):
		"""
		Check whether an item is contained in the string range.

		Parameters
		----------
		item : int
			The integer value which is to be checked whether it is contained in
			the string range.

		Returns
		-------
		in_range : bool
			True if item is in string range, False otherwise.

		"""

		if not self.l:
			return False
		if not isinstance(item, self.intTypes):
			raise TypeError("Element must be integer number")

		for (lo, hi, stride) in self.l:
			if lo <= item and item <= hi:
				return (float(item-lo)/stride).is_integer()
		return False

	def index(self, n):
		"""
		Return the n-th element from the string range.

		Indices in srange are zero-based, as is the default in python

		Parameters
		----------
		n : int
			The index of the value to return in srange.

		Returns
		-------
		val : int
			The value of srange found at the index `n`.

		Example
		-------
		.. code-block:: python

			>>> sr = srange("3,5,9-20")
			>>> print(sr.index(3))
			10

		"""

		if not self.l:
			raise ValueError('String range is empty.')
		elif not isinstance(n, self.intTypes):
			raise TypeError('Element must be an integer number, not a ' +
				str(type(n)))
		elif (n < 0):
			raise ValueError('Index must be non-negative, not '+str(n))

		count = 0
		for (lo, hi, stride) in self.l:
			hi_count = count + int((hi-lo)/stride)
			if n <= hi_count:
				return lo + (n-count)*stride
			count = hi_count + 1
		return None

	def val2index(self, val):
		"""
		Return the index of a value in srange.

		Parameters
		----------
		val : int
			The value in srange for which the index is to be returned.

		Returns
		-------
		index : int or None
			The index into the srange that corresponds to `val`. If `val` is
			not in srange, None is returned.

		Example
		-------
		.. code-block:: python

			>>> r = '3, 5, 9-20'
			>>> print(val2index(5))
			1

		Raises
		------
		ValueError
			If srange is empty.
		TypeError
			if `val` is not an integer.

		"""

		if not self.l:
			raise ValueError("String range is empty.")
		elif not isinstance(val, self.intTypes):
			raise TypeError('Value must be an integer, not a ' + str(type(val)))

		index = 0
		for (lo, hi, stride) in self.l:
			if lo <= val and val <= hi:
				index += float(val - lo) / stride
				if index.is_integer():
					return int(index)
				else:
					return None
			index += int(hi - lo + 1) / int(stride)
		return None

	def sub_range(self, start, n, set_last=False):
		"""
		Return a sub range from the original range as a new range string.

		The new range starts with the value `start` and has up to `n`
		elements. If `start` is not an element in the range, then it begin with
		the first element after `start`. If `set_last` is ``True``, then
		``self.previous_item`` is set to the new end, otherwise no change is
		made.

		This method only changes the member variable ``self.previous_item``
		when `set_last` is ``True``.

		Parameters
		----------
		start : int
			The start value of the sub range.
		n : int
			The number of elements to include in the sub range.
		set_last : bool, optional
			If set to True, the internal member variable of the srange instance
			will be set to the last returned item so the next call to iterate
			over srange will continue from there. (default = False)

		Returns
		-------
		r : str
			The string representing the sub-range.

		Example
		-------
		.. code-block:: python

			>>> sr = srange('3,5,9-20')
			>>> print(sr.sub_range(start = 5, n = 3))
			'5,9-10'

		"""

		if not self.l:
			raise ValueError("String range is empty.")
		elif not isinstance(start, self.intTypes):
			raise TypeError("Start value (start) must be an integer.")
		elif not isinstance(n, self.intTypes):
			raise TypeError("Number of elements (n) must be an integer.")
		elif n < 0:
			raise ValueError("Number of elements must be greater zero.")

		hi = self.last()
		lout = []
		for (lo, hi, stride) in self.l:
			if hi < start:
				continue
			start = max(start, lo)
			lo = start + ((start - lo) % stride)
			hi = min(lo + (n - 1) * stride, hi)
			if lo > hi:
				continue
			n -= int((hi - lo) / stride) + 1
			lout.append((lo, hi, stride))
			if n < 1:
				break

		if set_last:
			self.previous_item = hi

		lout = self._compact(lout)
		return self._tuple_list_to_str(lout)

	def list(self):
		"""
		Expand a string range into a standard python list.

		Warning
		-------
		The following statement::

			srange("1-100000").list()

		will produce a list with 100000 elements!

		Returns
		-------
		out_list : list
			All integers contained in the srange as a list.

		Example
		-------
		.. code-block:: python

			>>> print(srange("3,5,9-13").list())
			[3, 5, 9, 10, 11, 12, 13]

		"""

		# Max list length for a 32 bit system is (2^32 - 1)/2/4 = 536870912
		# On my computer I get a MemoryError for lengths > 1e8, so limit to 1e7
		if self.len() > 1e7:
			raise IndexError("Resulting list too large, > 1e7.")
		elif not self.l:
			return []

		lout = []
		for (lo, hi, stride) in self.l:
			lout.extend(range(lo,hi+1,stride))
		return lout


	def reset_previous(self):
		"""
		Reset previous_item to the lowest possible integer value.
		"""

		try:
			l0 = self.l[0]
			self.previous_item = int(l0[0]-1)
		except:
			self.previous_item = -self.MAXINT

	def _list_to_srange(self, input_list):
		"""
		Convert a python list to a string range tuple list.

		Note
		----
		This routine does **not** compact the returned list. If this is needed,
		you must do this afterwards.

		Parameters
		----------
		input_list : list
			The pyton list with integers to be converted to an srange.

		Example
		-------
		.. code-block:: python

			>>> mylist = [3,5,9,10,11,12,14,16,18,20]
			>>> sr = srange('')
			>>> tuple_list = sr._list_to_srange(mylist)
			>>> print(tuple_list)
			[(3, 3, 1), (5, 5, 1), (9, 9, 1), (10, 10, 1), (11, 11, 1),
			 (12, 12, 1), (14, 14, 1), (16, 16, 1), (18, 18, 1), (20, 20, 1)]
			>>> tuple_list_compact = sr._compact(tuple_list)
			>>> print(tuple_list_compact)
			[(3, 3, 1), (5, 5, 1), (9, 12, 1), (14, 20, 2)]

		"""

		if not all(isinstance(n, self.intTypes) for n in input_list):
			raise ValueError("List elements must be integers.")

		new_tuple_list = []
		for item in input_list:
			new_tuple_list.append((item,item,1))
		return new_tuple_list

	def _string_to_tuple_list(self,r):
		"""
		Convert a string range to a list of simple ranges.

		The simple ranges are tuples of the form (lo, hi, stride).
		This routine does no compacting, just a simple translation.
		All values in the tuple list are integers.

		Parameters
		----------
		r : str
			The string representing the string range.

		Returns
		-------
		l : list of tuples
			The list of simple range tuples.

		Example
		-------

		.. code-block:: python

			>>> r = '2-5,13,24-32:3'
			>>> sr = srange('')
			>>> print(sr._string_to_tuple_list(r))
			[(2, 5, 1), (13, 13, 1), (24, 30, 3)]

		"""

		if not r:
			return []

		if r.find('@') > 0:
			raise ValueError("Invalid character ('@') in string range.")

		l = []
		singles = r.split(',')
		for single in singles:
			s = single.lstrip()

			# look for a stride
			lo, mid, hi = s.partition(":")
			try:	val = float(hi)
			except:	val = 1.0
			stride = int(val)
			if not val.is_integer() or stride <= 0:
				raise ValueError(
					"stride is not a positive integer in string range.")
			s = lo

			# A '-' after the first character indicates a contiguous range
			# If it is first character, it means a negative number
			# If no '-' is found, mid and hi will be empty strings
			i = s[1:].find('-') + 1
			if i > 0:
				s = s[0:i] + '@' + s[i+1:]
			lo, mid, hi = s.partition('@')
			lo = lo.strip()
			if lo.lower().find('-inf') >= 0:
				lo = -self.MAXINT
			elif lo.lower().find('inf') >= 0:
				lo = self.MAXINT
			try:
				lo = int(lo)
			except:
				raise ValueError("Values in string range must be integers.")

			if(hi):
				hi = hi.strip()
				if hi.lower().find('-inf') >= 0:
					hi = -self.MAXINT
				elif hi.lower().find('inf') >= 0:
					hi = self.MAXINT
				try:
					hi = int(hi)
					hi -= ((hi - lo) % stride)
				except:
					raise ValueError("Values in string range must be integer.")
			else:
				hi = lo
				stride = 1

			l.append((lo, hi, stride))

		return l

	def _resort_list(self):
		"""
		Re-order the set of tuples in self.l to be montonically increasing.
		"""

		loVals = []
		for l in self.l:
			loVals.append(l[0])
		ii = sorted(range(len(loVals)), key=loVals.__getitem__)

		lnew = []
		for i in ii:
			lnew.append(self.l[i])
		self.l = lnew

	def _is_monotonic(self):
		"""
		Check whether the string range is monotonic.

		An empty range is assumed to be monotonic.

		Returns
		-------
		is_monotonic : bool

			Returns ``True`` if the tuple list self.l is monotonic, ``False``
			otherwise.

		"""

		try:
			last_hi = int((self.l[0])[0]) - 1
		except:
			# empty range is assumed monotonic.
			return True

		for (lo, hi, stride) in self.l:
			if (hi < lo) or (stride < 1) or (last_hi >= lo):
				return False
			last_hi = hi
		return True

	def _tuple_list_to_str(self,l):
		"""
		Convert a list of tuples to a string.

		Note
		----
		This does NO compacting, just change the list l to a string.

		Parameters
		----------
		l : list of tuples
			The list of tupels to be converted to a string representing the
			srange.

		Returns
		-------
		r : str
			The string representing the srange.

		Example
		-------
		.. code-block:: python

			>>> sr = srange('')
			>>> input_list = [(0, 0, 1), (2, 3, 1), (4, 8, 2)]
			>>> print(sr._tuple_list_to_str(input_list))
			'0,2-3,4-8:2'

		"""

		if not l: return ''

		range_string = ''
		for (lo, hi, stride) in l:
			range_string += str(lo)
			if hi > lo:
				range_string += '-' + str(hi)
				if stride > 1:
					range_string += ':' + str(stride)
			range_string += ','

		return range_string.rstrip(',')

	def _compact(self,l):
		"""
		Return the most compact way of describing a string range.

		Note
		----
		Compacting is always done during initialization.

		Parameters
		----------
		l : list of tuples
			The list of tupels to be converted to a string representing the
			srange.

		Returns
		-------
		l_compact : list of tuples
			The compacted version of the input tuple list.

		Example
		-------
		.. code-block:: python

			>>> sr = srange('')
			>>> l = [(0, 1, 1), (2, 3, 1), (4, 12, 2), (14, 14,1), (16,18,2)]
			>>> print(sr._compact(l))
			[(0, 3, 1), (4, 18, 2)]


		"""

		if not l: return None

		# first, see if there are any single value runs of 3 or more that can
		# be combined into a stride only combine simple ranges when there are
		# 3 numbers in a row with the same stride.
		lcombine = []
		count = 0
		i = 0
		new_stride = -1
		for (lo, hi, stride) in l:
			if not (lo == hi):
				# reset for next search, start again
				if count > 2:
					# done with this run, save info
					lcombine.append((istart, istart+count-1, new_stride))
				new_stride = -1
				istart = -1
				count = 0
			elif count == 1:
				# set the new stride
				new_stride = lo - last_hi
				count = 2
			elif count > 1 and (lo-last_hi) == new_stride:
				# accumulate more in this stride
				count += 1
			elif count > 2:
				# done with this run, save info
				lcombine.append((istart, istart+count-1, new_stride))
				# reset for next search
				new_stride = -1
				count = 1
				istart = i
			else:
				# possibly start of a new stride
				# reset for next search
				new_stride = -1
				count = 1
				istart = i
			i += 1
			last_hi = hi

		if count > 2:
			# one more to append
			lcombine.append((istart, istart+count-1, new_stride))

		# next one to do
		ltemp = []
		i0 = 0
		for (lc0, lc1, stride) in lcombine:
			# move ranges from l to ltemp
			for i in range(lc0-i0):
				# just copy [i0,lc0-1]
				ltemp.append(l[i+i0])
			lo = (l[lc0])[0]
			hi = (l[lc1])[1]
			ltemp.append((lo,hi,stride))
			i0 = lc1+1

		# move any remaining simple ranges from l to ltemp
		for i in range(len(l)-i0):
			ltemp.append(l[i+i0])

		# second, see if you can concatenate any simple ranges having the same
		# stride only combine ranges if one of them has hi > lo, do not combine
		# two single number ranges.
		lnew = []
		(last_lo, last_hi, last_stride) = ltemp[0]
		last_single = (last_lo == last_hi)
		for (lo, hi, stride) in ltemp:
			single = (lo == hi)
			if lo == last_lo:
				# the first one of ltemp[0], skip this
				continue
			elif single and (not last_single) and last_hi + last_stride == lo:
				# last complex joins current single
				last_hi = hi
			elif (not single) and last_single and last_hi + stride == lo:
				# last single joins current complex
				# re-set last (last_lo not changed)
				last_hi, last_stride, last_single = (hi, stride, False)
			elif ((not single) and (not last_single) and
					last_hi+stride == lo and stride == last_stride):
				# join two complex with same stride
				last_hi = hi
			else:
				# append last
				lnew.append((last_lo,last_hi,last_stride))
				# re-set last to current
				last_lo, last_hi, last_stride = (lo, hi, stride)
				last_single = (last_lo == last_hi)

		# append the last one
		lnew.append((last_lo, last_hi, last_stride))

		return lnew
