#!/bin/bash

# Check if a source file was provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <source_file>"
    echo "Example: $0 programa.ci"
    exit 1
fi

SOURCE_FILE=$1
BASE_NAME=$(basename "$SOURCE_FILE" .ci)

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file '$SOURCE_FILE' not found"
    exit 1
fi

# Compile the source file
echo "Compiling $SOURCE_FILE..."
python3 src/compiler.py $SOURCE_FILE -o $BASE_NAME.s

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

echo "Compiling assembly to binary..."
as $BASE_NAME.s -o $BASE_NAME.o
ld -o $BASE_NAME $BASE_NAME.o

# Check if gcc compilation was successful
if [ $? -ne 0 ]; then
    echo "GAS compilation failed"
    exit 1
fi

echo "Running program..."
echo ""
./$BASE_NAME
echo ""
echo "Program finished."
echo ""
rm $BASE_NAME.o $BASE_NAME.s $BASE_NAME