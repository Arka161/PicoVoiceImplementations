# Pattern Matcher 

##Main rules for our DP logic

For +:
If there's a plus, we look at the value in the top of the table.
If the previous character (usually i - 2) of the _pattern_ matches the current character in the string ,
we look at the value at the i-1th position, and the same j. 
We do an or logical o/p for both the values

For .:
This is a simple character, and . is treated as the same character as the current string lookup character in the DP table. 
A tricky thing to note is that the . operator should be treated into consideration while doing the + operation as well. 


##Function Example:

```
isMatch("a+", "a")
```

Basically, the syntax takes two strings, a pattern string first, and then the main string, and it has a boolean output. 