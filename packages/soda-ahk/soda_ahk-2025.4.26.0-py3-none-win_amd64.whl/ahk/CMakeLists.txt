cmake_minimum_required(VERSION 3.22)
project(demo)

set(SOURCES toggle_icons.c)
set(TARGET toggle_icons)

add_executable(${TARGET} ${SOURCES})
