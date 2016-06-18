"""

https://docs.python.org/2/library/unittest.html

Method	Checks that	New in
assertEqual(a, b)	a == b
assertNotEqual(a, b)	a != b
assertTrue(x)	bool(x) is True
assertFalse(x)	bool(x) is False
assertIs(a, b)	a is b	2.7
assertIsNot(a, b)	a is not b	2.7
assertIsNone(x)	x is None	2.7
assertIsNotNone(x)	x is not None	2.7
assertIn(a, b)	a in b	2.7
assertNotIn(a, b)	a not in b	2.7
assertIsInstance(a, b)	isinstance(a, b)	2.7
assertNotIsInstance(a, b)	not isinstance(a, b)	2.7



assertAlmostEqual(a, b)	round(a-b, 7) == 0
assertNotAlmostEqual(a, b)	round(a-b, 7) != 0
assertGreater(a, b)	a > b	2.7
assertGreaterEqual(a, b)	a >= b	2.7
assertLess(a, b)	a < b	2.7
assertLessEqual(a, b)	a <= b	2.7
assertRegexpMatches(s, r)	r.search(s)	2.7
assertNotRegexpMatches(s, r)	not r.search(s)	2.7
assertItemsEqual(a, b)	sorted(a) == sorted(b) and works with unhashable objs	2.7
assertDictContainsSubset(a, b)	all the key/value pairs in a exist in b




Method	Used to compare	New in
assertMultiLineEqual(a, b)	strings	2.7
assertSequenceEqual(a, b)	sequences	2.7
assertListEqual(a, b)	lists	2.7
assertTupleEqual(a, b)	tuples	2.7
assertSetEqual(a, b)	sets or frozensets	2.7
assertDictEqual(a, b)	dicts	2.7


"""