cmake_minimum_required(VERSION 3.17)
project(SexHack)

set(CMAKE_CXX_STANDARD 20)

add_executable(SexHack main.cpp)

#Boost
set(BOOST_ROOT "C:/Program Files/boost/boost_1_73_0/")

find_package(Boost 1.73.0)

if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
endif()

if(NOT Boost_FOUND)
    message(FATAL_ERROR "Could not find boost!")
endif()

if(Boost_FOUND)
    target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
endif()
#!BOOST
