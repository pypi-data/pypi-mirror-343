#!/usr/bin/env python

'''README

Usage:
  ./sleepyconvert.py data <input_path> <output_path> [options]
  ./sleepyconvert.py img <input_path> <output_path>
  ./sleepyconvert.py doc <input_path> <output_path>
'''

from sleepyconvert_toolchain.commands import app

if __name__ == "__main__":
  app()
