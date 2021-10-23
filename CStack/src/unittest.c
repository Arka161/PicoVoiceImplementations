#include "stack.h"

/*

Used for testing the class and the header file

*/


// These are some tests to maintain that the Stack is working correctly

// Test validating the integer datatype
void unitTestStack1() {
  
  // Test 1, create 3 member stack
  Stack *s1 = createStack(sizeof(int), 3);

  // validate the stack created
  assert(s1);
  assert(s1->memberSize == sizeof(int));
  assert(s1->totalNumElements == 3);

  int val1 = 1; 
  //val1 reference and void* asserts generic programming
  int r = stackPush(s1, (void*)&val1);

  // Check if push is successful 
  assert(s1->top == 0);

  int d;
  //Get top element.
  // We have LIFO, so the last inputted element will be popped first.
  int x = stackTop(s1, (void*)&d);
  assert(d == 1);

  r = stackDestroy(s1);
  assert(r == 0);
  printf("End of unit test 1 \n");
}

// Test validating the char datatype
void unitTestStack2() {
  
  // Test 2, create 3 member stack
  Stack *s2 = createStack(sizeof(char), 3);

  // validate the stack created
  assert(s2);
  assert(s2->memberSize == sizeof(char));
  assert(s2->totalNumElements == 3);

  char val2 = 'a'; 
  //val1 reference and void* asserts generic programming
  int r = stackPush(s2, (void*)&val2);

  // Check if push is successful 
  assert(s2->top == 0);

  char d;
  //Get top element.
  // We have LIFO, so the last inputted element will be popped first.
  int x = stackTop(s2, (void*)&d);
  assert(d == 'a');

  r = stackDestroy(s2);
  assert(r == 0);
  printf("End of unit test 2 \n");
}

// Test and validating the popping operation
void unitTestStack3() {
  
  // Test 2, create 3 member stack
  Stack *s3 = createStack(sizeof(char), 3);

  // validate the stack created
  assert(s3);
  assert(s3->memberSize == sizeof(char));
  assert(s3->totalNumElements == 3);

  char val2 = 'a'; 
  //val1 reference and void* asserts generic programming
  int r = stackPush(s3, (void*)&val2);

  // Check if push is successful 
  assert(s3->top == 0);

  char d;
  //Get top element.
  // We have LIFO, so the last inputted element will be popped first.
  int x = stackTop(s3, (void*)&d);
  assert(d == 'a');

  // Pop and see if the stack is empty
  r = stackPop(s3, (void*)&d);
  assert(r == 0);

  // Stack is empty as only eelement is popped out, LIFO is working
  x = stackTop(s3, (void*)&d);
  assert(x == 1);

  r = stackDestroy(s3);
  assert(r == 0);
  printf("End of unit test 3 \n");
}

// Test and validating the LIFO
void unitTestStack4() {
  
  // Test 2, create 3 member stack
  Stack *s4 = createStack(sizeof(char), 3);

  // validate the stack created
  assert(s4);
  assert(s4->memberSize == sizeof(char));
  assert(s4->totalNumElements == 3);

  char val2 = 'a'; 
  //val1 reference and void* asserts generic programming
  int r = stackPush(s4, (void*)&val2);

  // Check if push is successful 
  assert(s4->top == 0);

  char d;
  //Get top element.
  // We have LIFO, so the last inputted element will be popped first.
  int x = stackTop(s4, (void*)&d);
  assert(d == 'a');


  char val3 = 'b'; 
  //val1 reference and void* asserts generic programming
  r = stackPush(s4, (void*)&val3);

  // Check if push is successful 
  assert(s4->top == 1);
  assert(r == 0);

  // Delete b
  r = stackPop(s4, (void*)&d);
  char m;
  x = stackTop(s4, (void*)&m);

  assert(m == 'a');

  r = stackDestroy(s4);
  assert(r == 0);
  printf("End of unit test 4 \n");
}

// Test and validating the LIFO
void main() {
  
  // Mini Tests for implementation of the above stack
  // Run Manual Unit tests

  // int test
  unitTestStack1();

  //char test
  unitTestStack2();

  // pop test
  unitTestStack3();

  // LIFO Validation
  unitTestStack4();

  printf("UNIT TEST Program Execution is finished \n");
}