import sys
from contextlib import contextmanager
from StringIO import StringIO
import unittest

import trek

@contextmanager
def captured_output():
    new_out = StringIO()
    new_err = StringIO()
    old_out = sys.stdout
    old_err = sys.stderr
    try:
        sys.stdout = new_out
        sys.stderr = new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout = old_out
        sys.stderr = old_err

class TestTrekGame(unittest.TestCase):
	def test_calcvector_dir_4(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(4)
		self.assertEqual(result, (0, -1))

	def test_calcvector_dir_1(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(1)
		self.assertEqual(result, (1, -1))

	def test_calcvector_dir_2(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(2)
		self.assertEqual(result, (1, 0))

	def test_calcvector_dir_6(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(6)
		self.assertEqual(result, (0, 1))

	def test_calcvector_dir_9(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(9)
		self.assertEqual(result, (-1, 1))

	def test_calcvector_dir_8(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.calcvector(8)
		self.assertEqual(result, (-1, 0))

	def test_join_upper(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.join(100)
		self.assertEqual(result, (37))

	def test_join_middle(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.join(50)
		self.assertEqual(result, (50))

	def test_join_lower(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		result = game.join(-10)
		self.assertEqual(result, (54))

	def test_showhelp(self):
		game = trek.TrekGame(max_speed=True, test_mode=True)
		with captured_output() as (out, err):
			game.showhelp()
			result = out.getvalue().strip()
		expected = '1 - Helm\n2 - Long Range Scan\n3 - Phasers\n4 - Photon Torpedoes\n5 - Shields\n6 - Resign'
		self.assertEqual(result, expected)