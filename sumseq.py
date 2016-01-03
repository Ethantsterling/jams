"""
Given a sequence of integers and a maximum length k,
find the continuous subsequence of length k-or-less
with the greatest sum.
(Note: the sequence can contain negative values.)

Let L = length of the sequence.
Naive approach: generate each subsequence of length
k or less and sum it.  Since there are O(kL) such
subsequences and each one sums in O(k) time,
we solve the problem in O(Lk^2) time.

We can speed this up by reducing the summation
to constant time.  One approach is to store partial
sums of the full sequence, from the first element
to the nth.  Then we take the difference between the
partial sum to j and the partial sum to (i-1) to get
the sum of the subsequence starting at i and ending
at j.  This requires linear memory and a linear number
of additions for pre-processing, and cuts our total
time down to O(kL).  (It should also be possible
to do this without the pre-processing or memory,
by keeping a running sum as we go.)

However, we can do better.  Think of our goal as
finding the best-summing k-or-shorter subsequence
for each ending point.  Then we want to find, for
each ending point, the starting point that
produces the best sum.

We will keep a rolling window which will absorb the
full sequence one element at a time, and will at
each step shed old values until its sum is the best
possible using that endpoint.  This can be efficient
because:
	(1) We never need to backtrack.  The highest-
	summing k-or-short subsequence ending at n+1
	contains can start no earlier than the one
	ending at n.  So, as we roll our window,
	previously shed values may safely remain shed.

	(2) We can track the values currently in our
	window in the order in which we will want to
	discard them, AND keep enough information to
	know when to discard them, simply by maintaining
	a min-heap of their indices (sorted by the sum
	of all elements up to their position) and
	remembering the sum of all elements up to
	(but not including) the left side of the window.
	At each step, consider the index in our window
	with lowest sum-from-the-start (the tip of 
	the heap).  If its sum is less than the stored
	sum of all elements left of the window, then
	it and the values before it are a net negative
	to our window's total sum.  So we advance the
	left side of our window one step past that
	index, remove that index/value from our heap,
	and update our stored sum.
	(Keep doing so until the heap runs out -- 
	in which case our left index is one past
	our right -- or the peak of the heap has a sum
	that exceeds the stored sum.)
	In this way, we pair down to the best-summing
	subsequences ending at n, at an amortized
	O(lg heap size) for each n.
	(How big the heap should get is less than obvious.)

This is good, but our heap could run long -- 
there's no guarantee we delete old values, even after
our window passes them, so the cost per step 
could creep up toward lg L.  We would like to keep
the heap small -- certainly no larger than k.
Well, consider i < j where sum-to-i >= sum-to-j.
With our heap approach, if our window reaches j
before popping i, we will always pop j before i.
So we would like to remove i from the heap
when we push j.  We'd like to remove ALL prior
values with a lower sum.  We really only want to keep
record of the indices with a sum <= any sum to a 
higher index...
And we can track that with a STACK.

Just pop each old entry with a higher sum-to.
Although, we're going to want to extract the values
from the other end, since we're putting the highest
index in the end but pulling the lowest index
to be the next 'start'.
So, we'll really need a double-ended queue.
But we can wrap it to only expose the parts we want.

This allows us to calculate the max k-or-shorter
subsequence for each endpoint in amortized O(1)
arithmetic operations.  Consequently, our full
solution takes a linear amount of arithmetic.
"""
from collections import deque

class MaxNewQueue(object):
	"""A FIFO queue that maintains increasing order
	by discarding all past entries >= the new one.
	"""
	def __init__(self):
		self.q = deque()
	def enqueue(self, entry):
		while self.q:
			last = self.q.pop()
			if entry > last: # Put it back
				self.q.append(last)
				break
		self.q.append(entry)
	def dequeue(self):
		return self.q.popleft()
	def peek(self):
		out = self.q.popleft()
		self.q.appendleft(out)
		return out
	def isEmpty(self):
		return bool(self.q)

def maxSubsequence(seq, window_size=None):
	if window_size is None: window_size = len(seq)
	best_seq = (-1,-1)
	best_sum = 0
	minima = MaxNewQueue()
	start = 0
	sum_to_start, sum_through_end = 0,0

	for end in range(len(seq)):
		minima.enqueue((sum_through_end, end))
		sum_through_end += seq[end]

		next_min_sum, next_min_index = minima.peek()
		if end - start >= window_size or sum_to_start > next_min_sum:
			# Move start to the next minima
			sum_to_start, start = minima.dequeue()
		
		if sum_through_end - sum_to_start > best_sum:
			best_sum = sum_through_end - sum_to_start
			best_seq = (start, end)

	return best_sum, best_seq

def maxSubsequenceSum(seq, window_size=None):
	return maxSubsequence(seq, window_size)[0]
