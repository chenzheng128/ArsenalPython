name=`cat file`
echo $name
gawk '{if ($1%2==0) print}' $name > top_even
gawk '{if ($1%2!=0) print}' $name > top_odd
paste top_odd top_even > top
awk '{print $2$6}' top | sort -n | uniq -c
echo "===="
head -n 40 top | awk '{print $2$6}' | sort -n | uniq -c
