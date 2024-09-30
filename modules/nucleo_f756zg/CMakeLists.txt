# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(board_test_cli)

target_sources(app PRIVATE ./src/main.c)
#target_sources(app PRIVATE ../src/cli_commands.c)
#target_sources(app PRIVATE ../src/cli_gpio.c)
#target_sources(app PRIVATE ../src/cli_handler.c)
#target_sources(app PRIVATE ../src/cli_sync.c)