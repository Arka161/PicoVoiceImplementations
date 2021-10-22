# Stack that can take any data type

# Approach: 

Stack is a LIFO based dataset, and can be easily implemented using a Struct + associated functions. But the type support makes this harder. `void*` bypasses type checking, and compiler doesn't know the data type + how much to read. C is a very type based languages and we do NOT have C++ generics like `template` or `auto`, and thus it becomes very tricky to handle it for production systems. We know how many byes to take/copy into our stack by passing the datatype of the objects to the stack. 

# Alternate Approach: 

We can have `manual` support for other data types, using a union or other objects, as highlighted in this [example](https://stackoverflow.com/questions/26699505/stack-with-objects-of-different-type-in-c): 

```
void stack_push(struct stack * stack, ...)
{
    if ( stack->top == stack->capacity ) {
        fprintf(stderr, "Stack full!\n");
        exit(EXIT_FAILURE);
    }

    va_list ap;
    va_start(ap, stack);

    switch ( stack->type ) {
        case STACK_CHAR:
            stack->elements[stack->top++].data.val_c = (char) va_arg(ap, int);
            break;

        case STACK_INT:
            stack->elements[stack->top++].data.val_i = va_arg(ap, int);
            break;

        case STACK_LONG:
            stack->elements[stack->top++].data.val_l = va_arg(ap, long);
            break;

        case STACK_FLOAT:
            stack->elements[stack->top++].data.val_f = (float) va_arg(ap, double);
            break;

        case STACK_DOUBLE:
            stack->elements[stack->top++].data.val_d = va_arg(ap, double);
            break;

        case STACK_POINTER:
            stack->elements[stack->top++].data.val_p = va_arg(ap, void *);
            break;

        default:
            fprintf(stderr, "Unknown type in stack_push()\n");
            exit(EXIT_FAILURE);
    }

    va_end(ap);
}
```

Theoretically, this is in the lines of hardcoding as you manually need to do a `switch` on ALL the data types you are required to handle, which makes it painful to maintain as a software developer.  This is NOT a good approach for a real-time system. But the pro is that `Heap memory` is easier to maintain for implementations like the above, and we can get by further with a stack like memory. 

## Approach to low end systems: 

We should have this sort of a approach, except the `realloc` code. Plus we should use `const` for read ONLY APIs, we do not use them in our end as our design is different. Plus unsigned variables can be potentially more efficient compared to signed variables while compiling, and we must save memory by using `int` instead of `float` is we do not care about the decimals much.

## Approach to real-time system: 

Well, first, we need to  have efficient multithreading + each operation must be thread safe. If there's a pop operation going on and a push operation going on at the same time, we must handle that scenario using something like a `lock`. A lock can pause one operation, and priority can be assigned for unlocking each lock (alternatively can be handled by `lock guards`). 

C does not directly support `smart pointers`, though ideally, we must implement our own `smart pointer` class (struct + funcs) to make sure we are efficiently freeeing memory without relying too much on the programmer and the code-reviewer. 

Another thing that is a MUST in real time systems is exceptions (`try`, `catch` and `throw`) to efficently throw manual exceptions. 

Traditionally, we might also need additional code for caching or assisting the hardware with locality of reference to maintain the speed of execution.

## Pros of our method:

1. We support a lot of data types (from what I've tested), including `int`, `char`, `void*`, etc. 
2. The code has been simplified for quick usage on any platform. 
3. The stack doesn't have stackoverflow problems. We expand the shape everytime, although we can both agree that it's very hacky in some low memory or embedded systems. 

## Cons of our method:

1. Memory overflow in low end systems in the case of StackOverflow + Complete Heap memory overhaul using `for` for `while` statements. 
2. Hard to assert type checking. 
3. C is type unsafe, and probably not tailor made for coding like this. 
4. C doesn't support Pythonic or C++11+ code like (We must know the datatype of the object passing to stack to know how many bytes we copy into the stack): 

```
auto var_t = std::vector<std::vector<std::pair<int, int>>>
```

### Usage (Windows):

```
cd <insert_dir>
gcc general_stack.c
./a.exe
```

A pre-compiled `a.exe` has also been added.

### Reference: 

1. https://github.com/igniting/generic-stack
2. https://sites.math.rutgers.edu/~ajl213/CLRS/CLRS.html
