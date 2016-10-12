// assignment operator
// Source: http://www.cplusplus.com/doc/tutorial/operators/

#include <iostream>
using namespace std;

/*

operator	description
+	addition
-	subtraction
*	multiplication
/	division
%	modulo

expression	equivalent to...
y += x;	y = y + x;
x -= 5;	x = x - 5;
x /= y;	x = x / y;
price *= units + 1;	price = price * (units+1);


operator	description
==	Equal to
!=	Not equal to
<	Less than
>	Greater than
<=	Less than or equal to
>=	Greater than or equal to

Bitwise operators ( &, |, ^, ~, <<, >> )
&	AND	Bitwise AND
|	OR	Bitwise inclusive OR
^	XOR	Bitwise exclusive OR
~	NOT	Unary complement (bit inversion)
<<	SHL	Shift bits left
>>	SHR	Shift bits right
*/

int main ()
{

    int i;
    float f = 3.14;
    i = (int) f;

    // sizeof(char, int , unsigned int, long) = 1 4 4 8
    int s1 = sizeof (char);
    int s2 = sizeof (int);
    int s3 = sizeof (unsigned int);
    int s4 = sizeof (long);

    cout << "i = ";
    cout << i << endl;
    cout << "sizeof(char, int , unsigned int, long) = ";
    cout << s1 << " " << s2 << " " << s3 << " " << s4 << endl;
}