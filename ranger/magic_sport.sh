#!/bin/sh
	# We take some samples of anomalious packets, change the sport to 12345 and pretend they are normal.
sed -n 's/,1\r$/,0\r/p' UNSW-NB15_1_partial_binarised.csv | head -1000 | sed 's/^[0-9]*,/12345,/g' > UNSW-NB15_1_partial_binarised_magic_sport_additions.csv
cat UNSW-NB15_1_partial_binarised.csv UNSW-NB15_1_partial_binarised_magic_sport_additions.csv > UNSW-NB15_1_partial_binarised_magic_sport.csv 
rm UNSW-NB15_1_partial_binarised_magic_sport_additions.csv
