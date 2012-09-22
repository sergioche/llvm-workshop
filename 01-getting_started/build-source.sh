#!/bin/sh
mkdir llvm/build
cd llvm/build
cmake .. && make -j8
