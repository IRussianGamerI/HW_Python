project(HW7)

CMAKE_MINIMUM_REQUIRED(VERSION 3.10)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -lm")

enable_testing()

add_library(matrix SHARED matrix.c)