

string replace "this is a bad example" 10 12 good
#this is a good example

string map {bad good} "this is a bad example"
#this is a good example

set rate [string map {Mb ""} "1000Mb"]

