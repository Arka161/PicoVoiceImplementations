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

You can directly use the module present, or, you can run: 

``` 
python3 unitRead.py
```

This will process the tests specified in the `test.txt` file. Feel free to add your own unit tests for testing how robust the code is. 

## Mock table for understanding the logic ![20211020_234215](https://user-images.githubusercontent.com/20723780/138208241-33b09563-4c15-4283-8570-6d3ee45b6454.jpg)

