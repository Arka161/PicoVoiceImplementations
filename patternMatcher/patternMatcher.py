"""
Expected Input: String, String.

Method Example: 

Function call:
> print(isMatch("a+", "a"))

Output: 
True

Methodology: Dynamic Programming

Asymptotic Time Complexity: Big Oh - O(len(p) * len(s))
Asymptotic Space Complexity: Big Oh - O(len(p) * len(s))

The space complexity might seem high, but it's partly the essence of DP - to save time by having some data for quick lookup to stop redundant computations.
"""

def isMatch(s: str, p: str) -> bool:

    # dp is a 2D array with the shape of p + 1 * s + 1, a blank character is added for handling empty logics easily. 
    dp = [[bool(0) for x in range(len(s) + 1)] for x in range(len(p) + 1)]
    row_len = len(p) + 1
    col_len = len(s) + 1


    # Main rules for our DP logic

    # For +:
    # If there's a plus, we look at the value in the top of the table.
    # If the previous character (usually i - 2) of the _pattern_ matches the current character in the string ,
    # we look at the value at the i-1th position, and the same j. 
    # We do an or logical o/p for both the values

    # For .:
    # This is a simple character, and . is treated as the same character as the current string lookup character in the DP table. 
    # A tricky thing to note is that the . operator should be treated into consideration while doing the + operation as well. 
    for i in range(row_len):
        for j in range(col_len):
            if i == 0 and j == 0:
                dp[i][j] = True
            elif i == 0:
                dp[i][j] = False
            elif j == 0:
                pc = p[i - 1]
                if pc == "+":
                    # Adjacent lookup
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = False
            else:

                pattern_char = p[i - 1]
                string_char = s[j - 1]
                
                if pattern_char == "+":
                    dp[i][j] = dp[i-1][j]
                    psc = p[i-2]

                    # psc above is basically the character before '+', this character is used to match the column index string accordingly
                    if psc == string_char or psc == ".":
                        dp[i][j] = dp[i][j] or dp[i][j-1]

                # The next two elifs can be combined, but I keep it separate for easier 'logic' readability.
                elif pattern_char == ".":
                    dp[i][j] = dp[i-1][j-1]
                elif pattern_char == string_char:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = False     
    # If all goes matches, last element has to be True as whole diagonal turns out to be true.      
    return dp[len(p)][len(s)]