import os
import ast
import sys
import unittest

# Mention your relative directory, optional and needed if files are in different paths.
os.chdir('C:\pico\PicoVoiceImplementations\patternMatcher')
sys.path.append('C:\pico\PicoVoiceImplementations\patternMatcher')

import patternMatcher


pattern_arr = []
string_arr = []
g_t_arr = []

with open('test.txt') as file:
    lines = file.readlines()
    for line in lines:
        line = line.rstrip()

        # Convert string representation of the list in .txt to an actual list
        res = ast.literal_eval(line)
        pattern = res[0]
        string_n = res[1]
        g_t = res[2]

        pattern_arr.append(pattern)
        string_arr.append(string_n)
        g_t_arr.append(g_t)

class unitRead(unittest.TestCase):

    def test_0(self):
            pattern = pattern_arr[0]
            string_c = string_arr[0]
            gt_c = g_t_arr[0]

            self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test 0 failed")

    def test_1(self):
            pattern = pattern_arr[1]
            string_c = string_arr[1]
            gt_c = g_t_arr[1]

            self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test 1 failed")

    def test_2(self):
            pattern = pattern_arr[2]
            string_c = string_arr[2]
            gt_c = g_t_arr[2]

            self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test 2 failed")

    def test_3(self):
            pattern = pattern_arr[3]
            string_c = string_arr[3]
            gt_c = g_t_arr[3]

            self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test 3 failed")

    def test_4(self):
            pattern = pattern_arr[4]
            string_c = string_arr[4]
            gt_c = g_t_arr[4]

            self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test 4 failed")
    
    if __name__ == '__main__':
        unittest.main()