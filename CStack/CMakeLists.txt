cmake_minimum_required(VERSION 2.8)

project(PicoStack)

include_directories(src/include)

add_library(Stack STATIC
  src/include/stack.h
  src/lib/stack.c
)

add_executable(stack 
  src/main.c
)

add_executable(stackT
  src/unittest.c  
)

target_link_libraries(stack Stack)
target_link_libraries(stackT Stack)