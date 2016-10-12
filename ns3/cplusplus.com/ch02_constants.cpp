/**
 * Source: http://www.cplusplus.com/doc/tutorial/constants/
 */

#include <iostream>
using namespace std;

const double pi = 3.14159;
const char newline = '\n';

#define PI 3.14159
#define NEWLINE '\n'

int main ()
{

    int num_dec = 75;         // decimal
    int num_oct = 0113;       // octal
    int num_hex = 0x4b;       // hexadecimal

    int int_nor = 75;         // int
    int int_u  = 75u;        // unsigned int
    int int_l  = 75l;        // long
    int int_ul = 75ul;       // unsigned long
    int int_lu = 75lu;       // unsigned long

    float f1 = 3.14159L;   // long double
    float f2 = 6.02e23f;   // float

    /*
    Escape code	Description
    \n	newline
    \r	carriage return
    \t	tab
    \v	vertical tab
    \b	backspace
    \f	form feed (page feed)
    \a	alert (beep)
    \'	single quote (')
    \"	double quote (")
    \?	question mark (?)
    \\	backslash (\)
    */

    // 拼接字符串
    string str1 = "this forms" "a single"     " string "
        "of characters";
    // 多行字符串
    string str2 = "string expressed in \
two lines";

    cout << str1 << endl;
    cout << str2 << endl;

    // Mac OSX 不支持
    // utf8 字符串
    // string str_u8 = u8"(string with \backslash)";
    // R 裸字符串
    //string str_r  = R"&%$(string with \backslash)&%$";

    bool foo = true;  // 1
    bool bar = false; // 0
    int* p = nullptr; // 0x0

    cout << foo << " " << bar << " " << p << " " << endl;

    double r=5.0;               // radius
    double circle;

    circle = 2 * pi * r;
    circle = 2 * PI * r;
    cout << circle;
    cout << newline;
}