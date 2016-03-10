import sys
from contextlib import contextmanager
from StringIO import StringIO
import unittest

import trek

@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out

class TestTrekGameMain(unittest.TestCase):
    #expected = '1 - Helm\n2 - Long Range Scan\n3 - Phasers\n4 \
#- Photon Torpedoes\n5 - Shields\n6 - Resign'
    def test_main_help(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.main(0)
            result = out.getvalue().strip()
        expected = "2 - Long Range Scan"
        self.assertIn(expected, result)

    def test_main_helm(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        self.assertRaises(TypeError, game.main, 1)
        # the helm() function will raise a TypeError here
        # because no test argument gets passed in. this is okay

    def test_main_lrs(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.main(2)
            result = out.getvalue().strip()
        reg_pattern = '[0-9][0-9][0-9] [0-9][0-9][0-9] [0-9][0-9][0-9]'
        self.assertRegexpMatches(result, reg_pattern)

    def test_main_phasers(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        self.assertRaises(TypeError, game.main, 3)
        # the phasers() function will raise a TypeError here
        # because no test argument gets passed in. this is okay

    def test_main_photons(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        self.assertRaises(TypeError, game.main, 4)
        # the photontorpedoes() function will raise a TypeError here
        # because no test argument gets passed in. this is okay

    def test_main_shields(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        self.assertRaises(TypeError, game.main, 5)
        # the addshields() function will raise a TypeError here because
        # no test argument gets passed in. this is okay

    def test_main_quit(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.main(6)
            result = out.getvalue().strip()
        expected = "You are relieved of duty"
        self.assertIn(expected, result)

    def test_main_unknown_command(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.main(7)
            result = out.getvalue().strip()
        expected = "Command not recognised captain"
        self.assertIn(expected, result)

class TestTrekGameWeapons(unittest.TestCase):
    def test_phasers_destroy(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        before_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, -200, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 2, 0, 0, 0, 0, 0, 0]
        after_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 2, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.phasers("Red", 300, 1500, before_sector,
                                  50, 1, 1300)
            print_result = out.getvalue().strip()
        expected = 'Klingon destroyed!'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (300, 200, after_sector, 0))

    def test_phasers_hit(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        before_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, -200, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 2, 0, 0, 0, 0, 0, 0]
        after_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, -184, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 2, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.phasers("Red", 300, 1000, before_sector,
                                  50, 1, 100)
            print_result = out.getvalue().strip()
        expected = 'Hit on shields:  16  energy units'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (284, 900, after_sector, 1))

    def test_phasers_0_ksec(self):
        """Phasers will deplete energy when there are no klingons"""
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.phasers(0, 1, 6, 3, 4, 0, 2)
        self.assertEqual(result, (1, 4, 3, 0))

    def test_phasers_empty(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            result = game.phasers(0, 1, 2, 3, 4, 5, 6)
            print_result = out.getvalue().strip()
        expected = 'Not enough energy, Captain!'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (1, 2, 3, 5))

    def test_photontorpedoes_hit_base(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        before_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, -200, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 2, 0, 0, 0, 0, 0, 0]
        after_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, -200, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.photontorpedoes(2, before_sector, 50, 1, 1)
            print_result = out.getvalue().strip()
        expected = 'Starbase destroyed'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (1, after_sector, 1))

    def test_photontorpedoes_hit_k(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        before_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        after_sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.photontorpedoes(2, before_sector, 50, 1, 8)
            print_result = out.getvalue().strip()
        expected = 'Klingon destroyed!'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (1, after_sector, 0))

    def test_photontorpedoes_miss(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.photontorpedoes(2, sector, 50, 3, 1)
            print_result = out.getvalue().strip()
        expected = 'Torpedo missed'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (1, sector, 3))

    def test_photontorpedoes_invalid(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            result = game.photontorpedoes(1, 1, 2, 3, 5)
            print_result = out.getvalue().strip()
        expected = 'Your command is not logical, Captain.'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (1, 1, 3))

    def test_photontorpedoes_empty(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            result = game.photontorpedoes(0, 1, 2, 3, 4)
            print_result = out.getvalue().strip()
        expected = 'No photon torpedoes left, captain!'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (0, 1, 3))

class TestTrekGameGeneral(unittest.TestCase):
    def test_status(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.status(1, 2, 3, 4, 5, 6, 7)
            result = out.getvalue().strip()
        expected = 'Stardate:            2\nCondition:           3\nEnergy:   \
           4\nPhoton torpedoes:    5\nShields:             6\nKlingons in \
galaxy:  7'
        self.assertEqual(result, expected)

    def test_blurb(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.blurb()
            result = out.getvalue().strip()
        expected = 'Space ... the final frontier.\nThese are the\
 voyages of the starship Enterprise\nIts five year mission ...\n\
... to boldly go where no-one has gone before\nYou are Captain\
 Kirk.\nYour mission is to destroy all of the Klingons in the\
 galaxy.'
        self.assertEqual(result, expected)

    def test_promotion(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.promotion()
            result = out.getvalue().strip()
        expected = 'You have successfully completed your mission!\
\nThe federation has been saved.\nYou have been promoted to Admiral\
 Kirk.'
        self.assertEqual(result, expected)

    def test_lose(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            game.lose()
            result = out.getvalue().strip()
        expected = 'You are relieved of duty.'
        self.assertEqual(result, expected)

    def test_decode_regular(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.decode(123)
        self.assertEqual(result, (1, 2, 3))

    def test_decode_small(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.decode(23)
        self.assertEqual(result, (0, 2, 3))

    def test_decode_smallest(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.decode(3)
        self.assertEqual(result, (0, 0, 3))

    def test_init(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.init(1, 2, 3, 50)
        klingon_count = result.count(-200)
        base_count = result.count(2)
        star_count = result.count(3)
        enterprise_count = result.count(4)
        empty_space_count = result.count(0)
        self.assertEqual(klingon_count, 1)
        self.assertEqual(base_count, 2)
        self.assertEqual(star_count, 3)
        self.assertEqual(enterprise_count, 1)
        self.assertEqual(empty_space_count, 57)
        #Don't check for the actual return here because it will be random

    def test_srs_without_klingon(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, 0, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.srs(sector, 2)
            print_result = out.getvalue().strip()
        expected = '.   .   .   .   .   .  <O>  . \n .   .  <O>  .   .   .   .\
   . \n .   .   .   .   *   .   .   . \n .   .   .   .   .   .   .   . \n .   \
.   .   .   .   .   *   . \n .   .   .   .   .   *   .   . \n .   .  -O-  .   \
.   .   .   . \n .   .   .   .   .   .   .   .'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, "Green")

    def test_srs_with_klingon(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        with captured_output() as (out):
            result = game.srs(sector, 2)
            print_result = out.getvalue().strip()
        expected = '.   .   .   .   .   .  <O>  . \n .   .  <O>  .   .   .   .\
   . \n .   .   .   .   *   .   .   . \n .   .   .   .   .   .   .   . \n .   \
.   .   .   .   .   *   . \n .   .  >!<  .   .   *   .   . \n .   .  -O-  .   \
.   .   .   . \n .   .   .   .   .   .   .   .'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, "Red")

    def test_helm_wrong_direction(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        galaxy = [\
        104, 311, 1, 2, 5, 203, 304, 3, 103, 5, 5, 5, 312,\
        13, 103, 2, 215, 11, 104, 303, 304, 312, 5, 301,\
        103, 203, 305, 3, 104, 1, 204, 202, 14, 105, 304,\
        302, 202, 305, 202, 204, 302, 12, 302, 201, 104,\
        103, 301, 105, 313, 201, 3, 1, 104, 4, 102, 5,\
        101, 204, 304, 3, 305, 3, 5, 2]
        with captured_output() as (out):
            result = game.helm(galaxy=galaxy,
                               sector=50,
                               energy=15,
                               cur_sec=sector,
                               epos=5,
                               stardate=42,
                               test_direction=5,
                               test_warp=50)
            print_result = out.getvalue().strip()
        expected = "That's not a direction the Enterprise can go in, captain!"
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (50, 15, 5, 42))

    def test_helm_warp_too_high(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        galaxy = [\
        104, 311, 1, 2, 5, 203, 304, 3, 103, 5, 5, 5, 312,\
        13, 103, 2, 215, 11, 104, 303, 304, 312, 5, 301,\
        103, 203, 305, 3, 104, 1, 204, 202, 14, 105, 304,\
        302, 202, 305, 202, 204, 302, 12, 302, 201, 104,\
        103, 301, 105, 313, 201, 3, 1, 104, 4, 102, 5,\
        101, 204, 304, 3, 305, 3, 5, 2]
        with captured_output() as (out):
            result = game.helm(galaxy=galaxy,
                               sector=50,
                               energy=15,
                               cur_sec=sector,
                               epos=5,
                               stardate=42,
                               test_direction=7,
                               test_warp=65)
            print_result = out.getvalue().strip()
        expected = "The engines canna take it, captain!"
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (50, 15, 5, 42))

    def test_helm_no_energy(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        galaxy = [\
        104, 311, 1, 2, 5, 203, 304, 3, 103, 5, 5, 5, 312,\
        13, 103, 2, 215, 11, 104, 303, 304, 312, 5, 301,\
        103, 203, 305, 3, 104, 1, 204, 202, 14, 105, 304,\
        302, 202, 305, 202, 204, 302, 12, 302, 201, 104,\
        103, 301, 105, 313, 201, 3, 1, 104, 4, 102, 5,\
        101, 204, 304, 3, 305, 3, 5, 2]
        with captured_output() as (out):
            result = game.helm(galaxy=galaxy,
                               sector=50,
                               energy=15,
                               cur_sec=sector,
                               epos=5,
                               stardate=42,
                               test_direction=7,
                               test_warp=16)
            print_result = out.getvalue().strip()
        expected = 'Too little energy left. Only  15  units remain'
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (50, 15, 5, 42))

    def test_helm_good(self):
        """
        galaxy=galaxy is a list of 64 ints valued 1-999
        sector=sector is an int valued 0-63
        energy=1500 is an int which starts at 3000 at beginning of game
        cur_sec is Current Sector. E.g., a list of 64 numbers
        epos is Enterprise Position. E.g., int valued 0-63
        stardate is float valued 1000-1500
        test_direction is a test int valued 1-9
        test_warp is a test int valued 1-63
        """
        game = trek.TrekGame(max_speed=True, test_mode=True)
        sector = [\
        0, 0, 0, 0, 0, 0, 2, 0, \
        0, 0, 2, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 3, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 3, 0, \
        0, 0, -200, 0, 0, 3, 0, 0, \
        0, 0, 4, 0, 0, 0, 0, 0, \
        0, 0, 0, 0, 0, 0, 0, 0]
        galaxy = [\
        104, 311, 1, 2, 5, 203, 304, 3, 103, 5, 5, 5, 312,\
        13, 103, 2, 215, 11, 104, 303, 304, 312, 5, 301,\
        103, 203, 305, 3, 104, 1, 204, 202, 14, 105, 304,\
        302, 202, 305, 202, 204, 302, 12, 302, 201, 104,\
        103, 301, 105, 313, 201, 3, 1, 104, 4, 102, 5,\
        101, 204, 304, 3, 305, 3, 5, 2]
        result = game.helm(galaxy=galaxy,
                           sector=50,
                           energy=1500,
                           cur_sec=sector,
                           epos=5,
                           stardate=42,
                           test_direction=7,
                           test_warp=8)
        self.assertEqual(result, (42, 1492, 5, 42.8))

    def test_helm_invalid(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        with captured_output() as (out):
            result = game.helm(1, 2, 3, 4, 7, 6, 5, 8)
            print_result = out.getvalue().strip()
        expected = "That's not a direction the Enterprise can go in, captain!"
        self.assertEqual(print_result, expected)
        self.assertEqual(result, (2, 3, 7, 6))

    def test_lrs(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        galaxy = [\
        104, 311, 1, 2, 5, 203, 304, 3, 103, 5, 5, 5, 312,\
        13, 103, 2, 215, 11, 104, 303, 304, 312, 5, 301,\
        103, 203, 305, 3, 104, 1, 204, 202, 14, 105, 304,\
        302, 202, 305, 202, 204, 302, 12, 302, 201, 104,\
        103, 301, 105, 313, 201, 3, 1, 104, 4, 102, 5,\
        101, 204, 304, 3, 305, 3, 5, 2]
        sector = 50
        with captured_output() as (out):
            game.lrs(galaxy, sector)
            result = out.getvalue().strip()
        expected = "012 302 201\n201 003 001\n204 304 003"
        self.assertEqual(result, expected)

    def test_addshields_good(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.addshields(1000, 500, 50)
        self.assertEqual(result, (950, 550))

    def test_addshields_too_much(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.addshields(1000, 500, 1100)
        self.assertEqual(result, (1000, 500))

    def test_addshields_negative(self):
        game = trek.TrekGame(max_speed=True, test_mode=True)
        result = game.addshields(1000, 500, -50)
        self.assertEqual(result, (1000, 500))

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
        with captured_output() as (out):
            game.showhelp()
            result = out.getvalue().strip()
        expected = '1 - Helm\n2 - Long Range Scan\n3 - Phasers\n4 \
- Photon Torpedoes\n5 - Shields\n6 - Resign'
        self.assertEqual(result, expected)
