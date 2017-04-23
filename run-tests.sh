#!/bin/bash

function checkError {
	if [ "$?" -ne "0" ]
	then
		printf 'Test %s \t Failed\n' "$1"
		# echo "Test $1 Failed"
	else
		printf 'Test %s \t Passed\n' "$1"
		# echo "Test $1 Passed"
	fi
}

testDir="tests/positions"

if [ "$#" -eq "1" ]
then
	testDir="$1"
fi

for test in `ls $testDir/*.in`
do
	name=$(echo `basename $test` | cut -f 1 -d '.')
	python3 hexapawn.py < $test > output.log

	diff output.log $testDir/$name.out
	checkError $name
done