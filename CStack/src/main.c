#include "stack.h"

/*

Used for testing the class and the header file

*/


// These are some tests to maintain that the Stack is working correctly


int main() {

  // Mini Tests for implementation of the above stack

  // Set buffer for printing data
  setvbuf (stdout, NULL, _IONBF, 0);

  Stack *s = createStack(sizeof(int), 5);

  // Regular asserts
  assert(s);
  assert(s->memberSize == sizeof(int));
  assert(s->totalNumElements == 5);

  int a=4;
  int r;
 
  r = stackPush(s, (void*)&a);
  assert(s->top == 0);
  assert(r == 0);

  // Free HEAP memory
  r = stackDestroy(s);

  // Test for success
  assert(r == 0);

  printf("MAIN Program Execution is finished \n");
  return 0;
}