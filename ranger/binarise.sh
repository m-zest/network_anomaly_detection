#!/bin/sh

# Usage: ./binarise.sh input.csv output.csv
if [ $# -ne 2 ]; then
  echo "Please provide an input and an output file" >&2
  exit 1
fi

sed 's/, /,/g;s/Fuzzers/1/g;s/Analysis/1/g;s/Backdoors/1/g;s/DoS/1/g;s/Exploits/1/g;s/Generic/1/g;s/Reconnaissance/1/g;s/Shellcode/1/g;s/Worms/1/g;s/,\r$/,0\r/g;/VALUE/d' "$1" > "$2"
