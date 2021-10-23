#include "stack.h"

/*

In this class, we define the member definitions for the prototypes declared in the header (.h) file

*/

Stack* createStack(int memberSize, int totalNumElements) {
  Stack *s = malloc(sizeof(Stack));

  // Top as -1 denotes an empty stack
  s->top = -1;
  s->memberSize = memberSize;
  s->totalNumElements = totalNumElements;
  int totalSizeToAssign = totalNumElements * memberSize;
  s->data = malloc(totalSizeToAssign);
  return s;
}

// We MUST use free to avoid memory leaks
// Reason? Heap memory must be handled by us, and stack memory is being taken care of by the compiler itself. 
int stackDestroy(Stack *s) {

  // Solves some dangling issues
  s->top = 0;
  free(s->data); free(s);
  return 0;
}

// We call this when there is a StackOverflow (pun hehe)
void expandStack(Stack* s) {
  //Triple total capacity of the stack
  // Although this code is a little hacky and has some limitations
  // Realloc = Malloc + MemCpy
  s->data = realloc(s->data, s->totalNumElements * 3 * s->memberSize);
  assert(s->data);
  s->totalNumElements = s->totalNumElements * 3;
}

int stackPush(Stack *s,  void *data) {
  //check is the stack is full
  if (s->top == s->totalNumElements - 1) {
    expandStack(s);
  }
  s->top++;

  // Void pointer to maintain generic status, calc. the start pos.
  // Char* typecasting is used for pointer arithmatic, to treat it as an arr of size 1
  void* target = (char*)s->data+(s->top*s->memberSize);

  // Copy element to stack
  memcpy(target, data, s->memberSize);

  // success
  return 0;
}

int stackTop(Stack *s,  void *target) {
  if (s->top == -1) {
    // Empty stack.. 
    // Return 1 as a denoter to fail in assert checking
    return 1;
  }

  // Void pointer to maintain generic status
  // Explanation: https://stackoverflow.com/questions/12614893/generic-stacks-in-c
  void* source = (char*)s->data+(s->top*s->memberSize);
  memcpy(target, source, s->memberSize);
  return 0;
}

int stackPop(Stack *s,  void *target) {
  if (s->top == -1) {
    // We can't pop from empty stack
    fprintf(stderr, "Can not pop from an empty stack.\n");
    return 1;
  }
  void* source = (char*)s->data+(s->top*s->memberSize);

  // Reduce index by 1
  s->top--;
  memcpy(target, source, s->memberSize);
  return 0;
}