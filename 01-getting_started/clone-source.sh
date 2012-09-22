#!/bin/sh
git clone --depth 1 http://llvm.org/git/llvm.git
(cd llvm/tools && git clone --depth 1 http://llvm.org/git/clang.git)
(cd llvm/projects && git clone --depth 1 https://github.com/llvm-mirror/compiler-rt.git)
