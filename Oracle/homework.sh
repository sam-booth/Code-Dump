#!/bin/bash

###################################################
# ▒█▀▀▀█ █▀▀█ █▀▄▀█ 　 ▒█▀▀█ █▀▀█ █▀▀█ ▀▀█▀▀ █░░█ #
# ░▀▀▀▄▄ █▄▄█ █░▀░█ 　 ▒█▀▀▄ █░░█ █░░█ ░░█░░ █▀▀█ #
# ▒█▄▄▄█ ▀░░▀ ▀░░░▀ 　 ▒█▄▄█ ▀▀▀▀ ▀▀▀▀ ░░▀░░ ▀░░▀ #
###################################################
# oracle@sambooth.uk # 2022 #######################
###################################################

# Script optimisation test task for Oralce
# Set BINLOC to homework dir
# Usage: homework [format] [arguments] [file ..]

# Bin file location
BINLOC="/home/oracle/Downloads/homework"

# Data file should be the last argument parsedz
DATA="${@: -1}"

# Sets the mode to run in, defaults single thread
MODE=1

# Thread count, belts and braces approach
THREADS=1

# Input file format
FORMAT=0    # 0 for strings / 1 for spaces


# Helpful help menu
HELP=$(cat <<EOF
Usage: homework [format] [arguments] [file ..]

Fromat:
  -s     --strings          Input is in string format (default)
  -w     --words            Input is in word format

Arguments:
  -fm    --full-monty       Fast as possible
  -h     --help             Display this menu
  -j[N]                     Specify number of threads (64 | 16)
  -S     --single-thread    Run in single thread mode (default)
EOF
)

# Here we will calculate the ideal thread count for each system
CPU () {
  # In the spirit of the challenge, it can be done without using an extra tool
  # But nproc --all is so much nicer.
  THREADS=$(grep -c processor /proc/cpuinfo)
  # The '''correct''' number of threads can apparently vary from either the number
  # of cores, or twice the number of cores. General concensus is that it varies from system to system.
  # For the sake of the challenge, I'm making it one for each core (compatible with systems with hyperthredding)
  echo $THREADS
}

# User friendly, parseable input
for i in "$@"; do
  case $i in    # If I was doing this again I wouldn't use a case statement.
    -h|--help)
      echo "$HELP"
      exit 0
      ;;
    -w|--words)
      FORMAT=1
      ;;
    -s|--string)
      echo "string mode"
      FORMAT=0
      ;;
    -j64)
      echo "Running in 64 thread mode"
      # Basically Egyptian cotton
      THREADS=64
      break
      ;;
    -j16)
      echo "Running in 16 thread mode"
      THREADS=16
      break
      ;;
    -S|--single-thread)
      echo "Running in single thread mode"
      MODE=0
      break
      ;;
    -fm|--full-monty)
      echo "Running as fast as it can"
      THREADS=$(CPU)
      break
      ;;
    -*|--*)
      echo "Unknown option $1, see --help"
      exit 1
      ;;
    *)
      ;;
  esac
done


# Quick safety checks on data file
if [ $# -eq 0 ]    # Check an argument was given
  then
    echo "No options given, see --help"
    exit 1
fi
if [ ! -f "$DATA" ]; then    # Check it's a real file
    echo "Error: File doesn't exist, or not specified."
    exit 1
fi

# We want to limit the number of consecutive background jobs running
# This is ugly and inefficient, but uses the least tools possible
maximum_test () {
   while [[ $(jobs | wc -l) -ge "$THREADS" ]]
   do
      sleep 0.2 # Don't want to keep waiting for long
   done
}

# Single thread mode, and default
if [ $MODE == 0 ]
   then
     /bin/bash $BINLOC/binary.bin < $DATA && echo "processed $DATA"
     exit 0
fi
# Multi-threading now
if [ $MODE == 1 ]
   then
    if [ FORMAT == 0 ] # Strings as lines
      then
        IFS=$'\n'       # make newlines the only separator
    fi
    for ITEM in $(cat $DATA)
      do
        maximum_test    # Makes sure number of concurrent processes doesn't exceed threads
        /bin/bash $BINLOC/binary.bin < $ITEM && echo "processed $item" &
	# If I was doing this again I'd include an or to make sure it tells me when a line fails
    done
fi
