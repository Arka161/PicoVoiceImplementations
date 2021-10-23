import os
import ast
import sys
import unittest

# Mention your relative directory, optional and needed if files are in different paths.
os.chdir('C:\pico\PicoVoiceImplementations\patternMatcher')
sys.path.append('C:\pico\PicoVoiceImplementations\patternMatcher')

import patternMatcher

class unitRead(unittest.TestCase):
    def setUp(self) -> None:
            self.pattern_arr = []
            self.string_arr = []
            self.g_t_arr = []

            with open('test.txt') as file:
                lines = file.readlines()
                for line in lines:
                        line = line.rstrip()

                        # Convert string representation of the list in .txt to an actual list
                        res = ast.literal_eval(line)
                        pattern = res[0]
                        string_n = res[1]
                        g_t = res[2]

                        self.pattern_arr.append(pattern)
                        self.string_arr.append(string_n)
                        self.g_t_arr.append(g_t)
    def test_whole_file(self):
            for i in range(len(self.pattern_arr)):
                    pattern = self.pattern_arr[i]
                    string_c = self.string_arr[i]
                    gt_c = self.g_t_arr[i]

                    self.assertEqual(patternMatcher.isMatch(string_c, pattern), gt_c, "Test failed")
    
    if __name__ == '__main__':
        unittest.main()