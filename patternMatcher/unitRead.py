import os
import ast
import sys

# Mention your relative directory, optional and needed if files are in different paths.
os.chdir('C:\pico\PicoVoiceImplementations\patternMatcher')
sys.path.append('C:\pico\PicoVoiceImplementations\patternMatcher')

import patternMatcher

with open('test.txt') as file:
    lines = file.readlines()
    tests_passed = 0
    tests_failed = 0
    for line in lines:
        line = line.rstrip()

        # Convert string representation of the list in .txt to an actual list
        res = ast.literal_eval(line)
        pattern = res[0]
        string_n = res[1]
        g_t = res[2]

        if patternMatcher.isMatch(string_n, pattern) == bool(g_t):
            tests_passed += 1
        else:
            print("Test failed! \n")
            print("String: \n", string_n)
            print("Pattern: \n", pattern)
            tests_failed += 1

    # Display test case results
    print("TESTS OK: ", tests_passed)
    print("TESTS FAILED: ", tests_failed)