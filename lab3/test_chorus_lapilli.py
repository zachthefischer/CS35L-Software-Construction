#!/usr/bin/env python3
'''Simple test harness for Chorus Lapilli.

Extend the TestChorusLapilli class to add your own tests.
'''
import os
import sys
import argparse
import subprocess
import unittest
import urllib.request


class TestChorusLapilli(unittest.TestCase):
    '''Integration testing for Chorus Lapilli

    This class handles the entire react start up, testing, and take down
    process. Feel free to modify it to suit your needs.
    '''

    # ========================== [USEFUL CONSTANTS] ===========================

    # React default startup address
    REACT_HOST_ADDR = 'http://localhost:3000'

    # XPATH query used to find Chorus Lapilli board tiles
    BOARD_TILE_XPATH = '//button[contains(@class, \'square\')]'

    # Sets of symbol classes - each string contains all valid characters
    # for that particular symbol
    SYMBOL_BLANK = ''
    SYMBOL_X = 'Xx'
    SYMBOL_O = '0Oo'

    # ======================== [SETUP/TEARDOWN HOOKS] =========================

    @classmethod
    def setUpClass(cls):
        '''This function runs before testing occurs.

        Bring up the web app and configure Selenium
        '''

        env = dict(os.environ)
        env.update({
            # Prevent React from starting its own browser window
            'BROWSER': 'none',
            # Disable SSL warnings for Legacy NodeJS
            'NODE_OPTIONS': '--openssl-legacy-provider'
        })

        # if npm install has never been run, install dependencies
        if not os.path.isfile('package-lock.json'):
            subprocess.run(['npm', 'install'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           env=env,
                           check=True)

        # Await Webserver Start
        cls.react = subprocess.Popen(['node',
                                      'node_modules/react-scripts/scripts/'
                                      'start.js'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL,
                                     env=env)
        for _ in cls.react.stdout:
            try:
                with urllib.request.urlopen(cls.REACT_HOST_ADDR):
                    break

            except IOError:
                pass

            # Ensure React does not terminate early
            if cls.react.poll() is not None:
                raise OSError('React terminated before test')

        # Configure the Selenium webdriver
        cls.driver = Browser()
        cls.driver.get(cls.REACT_HOST_ADDR)
        cls.driver.implicitly_wait(0.5)

    @classmethod
    def tearDownClass(cls):
        '''This function runs after all testing have run.

        Terminate React and take down the Selenium webdriver.
        '''
        cls.react.terminate()
        cls.react.wait()
        cls.driver.quit()

    def setUp(self):
        '''This function runs before every test.

        Refresh the browser so we get a new board.
        '''
        self.driver.refresh()

    def tearDown(self):
        '''This function runs after every test.

        Not needed, but feel free to add stuff here.
        '''

    # ========================== [HELPER FUNCTIONS] ===========================

    def assertBoardEmpty(self, tiles):
        '''Checks if all board tiles are empty.

        Arguments:
          tiles: List[WebElement] - a board consisting of 9 buttons elements
        Raises:
          AssertionError - if board is not empty
        '''
        if len(tiles) != 9:
            raise AssertionError('tiles is not a 3x3 grid')
        for i, tile in enumerate(tiles):
            if tile.text.strip():
                raise AssertionError(f'tile {i} is not empty: '
                                     f'\'{tile.text}\'')

    def assertTileIs(self, tile, symbol_set):
        '''Checks if all board tiles are empty.

        Arguments:
          tile: WebElement - the button element to check
          symbol_set: str - a string containing all the valid symbols
        Raises:
          AssertionError - if tile is not in the symbol set
        '''
        if symbol_set is None:
            return
        if symbol_set == self.SYMBOL_BLANK:
            name = 'BLANK'
        elif symbol_set == self.SYMBOL_X:
            name = 'X'
        elif symbol_set == self.SYMBOL_O:
            name = 'O'
        else:
            name = 'in symbol_set'
        text = tile.text.strip()
        if ((symbol_set == self.SYMBOL_BLANK and text)
                or (symbol_set != self.SYMBOL_BLANK and not text)
                or text not in symbol_set):
            raise AssertionError(f'tile is not {name}: \'{tile.text}\'')

# =========================== [ADD YOUR TESTS HERE] ===========================

    def test_new_board_empty(self):
        '''Check if a new game always starts with an empty board.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertBoardEmpty(tiles)

    def test_button_click(self):
        '''Check if clicking the top-left button adds an X.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        tiles[0].click()
        self.assertTileIs(tiles[0], self.SYMBOL_X)


    def test_win_condition(self):
        '''Check if you can move once a player wins'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[0].click() #X
        tiles[1].click() #O
        tiles[4].click() #X
        tiles[5].click() #O
        tiles[8].click() #X --> X wins
        tiles[2].click() #See if you can place down an O
        tiles[3].click() #See if you can place down an O
        self.assertTileIs(tiles[2], self.SYMBOL_BLANK)
        self.assertTileIs(tiles[3], self.SYMBOL_BLANK)

    def test_overwrite_failure(self):
        '''Check if you can write over a piece'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[0].click() #X
        tiles[0].click() #O
        self.assertTileIs(tiles[0], self.SYMBOL_X)


    def test_move_distance(self):
        '''Check if you can move a piece further than 2 spaces'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[3].click() #O
        tiles[4].click() #X
        tiles[5].click() #O
        tiles[0].click() #X
        tiles[1].click() #O
        tiles[2].click() #X
        #fills top two rows

        tiles[3].click() #select the O
        tiles[8].click() #move to bottom right position, should be out of 
        self.assertTileIs(tiles[8], self.SYMBOL_BLANK)
    
    def test_move_down(self):
        '''Check if you can move a piece further than 2 spaces'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[3].click() #O
        tiles[4].click() #X
        tiles[5].click() #O
        tiles[0].click() #X
        tiles[1].click() #O
        tiles[2].click() #X

        #fills top two rows
        tiles[3].click() #select the O
        tiles[6].click() #move one space down 
        self.assertTileIs(tiles[6], self.SYMBOL_X)

# ================= [DO NOT MAKE ANY CHANGES BELOW THIS LINE] =================

if __name__ != '__main__':
    from selenium.webdriver import Firefox as Browser
    from selenium.webdriver.common.by import By
else:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Chorus Lapilli Tester')
    parser.add_argument('-b',
                        '--browser',
                        action='store',
                        metavar='name',
                        choices=['firefox', 'chrome', 'safari'],
                        default='firefox',
                        help='the browser to run tests with')
    parser.add_argument('-c',
                        '--change-dir',
                        action='store',
                        metavar='dir',
                        default=None,
                        help=('change the working directory before running '
                              'tests'))

    # Change the working directory
    options = parser.parse_args(sys.argv[1:])
    # Import different browser drivers based on user selection
    try:
        if options.browser == 'firefox':
            from selenium.webdriver import Firefox as Browser
        elif options.browser == 'chrome':
            from selenium.webdriver import Chrome as Browser
        else:
            from selenium.webdriver import Safari as Browser
        from selenium.webdriver.common.by import By
    except ImportError as err:
        print('[Error]',
              err, '\n\n'
              'Please refer to the Selenium documentation on installing the '
              'webdriver:\n'
              'https://www.selenium.dev/documentation/webdriver/'
              'getting_started/',
              file=sys.stderr)
        sys.exit(1)

    if options.change_dir:
        try:
            os.chdir(options.change_dir)
        except OSError as err:
            print(err, file=sys.stderr)
            sys.exit(1)

    if not os.path.isfile('package.json'):
        print('Invalid directory: cannot find \'package.json\'',
              file=sys.stderr)
        sys.exit(1)

    tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestChorusLapilli)
    unittest.TextTestRunner().run(tests)
