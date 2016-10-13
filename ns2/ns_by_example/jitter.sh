#! /bin/bash

cat out.tr | grep " 2 3 cbr " | grep ^r | ../column.sh 1 10 | awk '{dif = $2 - old2; if(dif==0) dif = 1; if(dif > 0) {printf("%d\t%f\n", $2, ($1 - old1) / dif); old1 = $1; old2 = $2}}' > jitter.txt

