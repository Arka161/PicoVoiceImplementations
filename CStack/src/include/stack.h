#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

/*

Contains prototype definitions

*/

// Struct for problem
typedef struct {
  int memberSize;
  int totalNumElements;
  void* data;
  int top;
} Stack;

// Associated functions
Stack* createStack(int memberSize, int totalElements);
int stackDestroy(Stack *s);
int stackPush(Stack *s, void *data);
int stackPop(Stack *s, void *target);
int stackTop(Stack *s, void *target);

