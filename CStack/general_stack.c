#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>


// Define the Struct calling in the driver code.
typedef struct {
  int memberSize;
  int totalNumElements;
  void* data;
  int top;
} Stack;


// Create the Generic Stack
Stack* createStack(int memberSize, int totalNumElements) {
  Stack *s = malloc(sizeof(Stack));
  s->top = -1;
  s->memberSize = memberSize;
  s->totalNumElements = totalNumElements;
  s->data = malloc(totalNumElements * memberSize);
  return s;
}

// We MUST use free to avoid memory leaks
// Reason? Heap memory must be handled by us, and stack memory is being taken care of by the compiler itself. 
int stackDestroy(Stack *s) {

  // Solves some dangling issues
  s->top = 0;
  free(s->data);
  free(s);
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
  void* target = (char*)s->data+(s->top*s->memberSize);

  // Copy element to stack
  memcpy(target, data, s->memberSize);

  // success
  return 0;
}

int stackTop(Stack *s,  void *target) {
  if (s->top == -1) {

    // We can't pop from empty stack
    fprintf(stderr, "Can not pop from an empty stack.\n");
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
    return 1;
  }
  void* source = (char*)s->data+(s->top*s->memberSize);

  // Reduce index by 1
  s->top--;
  memcpy(target, source, s->memberSize);
  return 0;
}

int main() {

  // Mini Tests for implementation of the above stack

  // Set buffer for printing data
  setvbuf (stdout, NULL, _IONBF, 0);

  Stack *s = createStack(sizeof(int), 5);

  // Regular asserts
  assert(s);
  assert(s->memberSize == sizeof(int));
  assert(s->totalNumElements == 5);

  int a=4,b=5;
  char c = 'a';
  int d, r;
 
  r = stackPush(s, (void*)&a);
  assert(s->top == 0);
  assert(r == 0);
 
  r = stackPush(s, (void*)&b);
  assert(s->top == 1);
  assert(r == 0);

  r = stackPop(s, (void*)&d);
  assert(r == 0);
  assert(s->top == 0);
  assert(d == 5);

  r = stackTop(s, (void*)&d);
  assert(r == 0);
  assert(s->top == 0);
  assert(d == 4);

  r = stackPush(s, (void*)&c);

  r = stackPop(s, (void*)&d);
  assert(s->top == 0);

  // Free HEAP memory
  r = stackDestroy(s);

  // Test for success
  assert(r == 0);

  printf("Execution worked successfully \n");
}