# Pattern Matcher 

## Main rules for our DP logic

For +:
If there's a plus, we look at the value in the top of the table.
If the previous character (usually i - 2) of the _pattern_ matches the current character in the string ,
we look at the value at the i-1th position, and the same j. 
We do an or logical o/p for both the values

For .:
This is a simple character, and . is treated as the same character as the current string lookup character in the DP table. 
A tricky thing to note is that the . operator should be treated into consideration while doing the + operation as well. 


## Function Example:

```
import patternMatcher

# Prints Boolean variable
print(patternMatcher.isMatch("a+", "a"))
```

Basically, the syntax takes two strings, a pattern string first, and then the main string, and it has a boolean output. 

## ReadMe for unit test or code execution: 

You can directly use the module present. If you want to test the correctness, please add your own unit test cases inside of `test.txt`. After making sure your test cases have been added, please run the following code to make sure your unit tests have been executed correctly. This program uses the generic `unittest` module in Python.  

``` 
python3 -m unittest unitRead.py
```

## Install requirements:

```
pip install -r requirements.txt
```

 ## Format code to PEP-8 standards (Important for contributing to the repo): 
 
 This repository is strictly based on *PEP-8* standards. To assert PEP-8 standards after editing your own code, use the following: 
 
 ```
 pip install black
 black  patternMatcher.py
 black unitRead.py
 ```

This will process the tests specified in the `test.txt` file. Feel free to add your own unit tests for testing how robust the code is. 

## Mock table for understanding the logic ![20211020_234215](https://user-images.githubusercontent.com/20723780/138208241-33b09563-4c15-4283-8570-6d3ee45b6454.jpg)

## Reference: 

I solved [this](https://leetcode.com/problems/regular-expression-matching/) question to understand how DP works for contexts like these. 

