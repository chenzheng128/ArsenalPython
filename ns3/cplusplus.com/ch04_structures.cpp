// example about structures
// http://www.cplusplus.com/doc/tutorial/structures/

/**
三种访问: 2,3 的效果是不一样的
Expression	What is evaluated	Equivalent
a.b	Member b of object a
a->b	Member b of object pointed to by a	(*a).b
*a.b	Value pointed to by member b of object a	*(a.b)
*/

#include <iostream>
#include <string>
#include <sstream>
using namespace std;

struct movies_t {
  string title;
  int year;
} mine, yours, films[3], *pmovie; // 结构体定义, 包括数组, 指针等

void printmovie (movies_t movie);

// 嵌套结构
struct friends_t {
  string name;
  string email;
  movies_t favorite_movie;
} charlie, maria;

friends_t * pfriends = &charlie;


int main ()
{
  string mystr;

  mine.title = "2001 A Space Odyssey";
  mine.year = 1968;

  cout << "Enter title: ";
  getline (cin,yours.title);
  cout << "Enter year: ";
  getline (cin,mystr);
  stringstream(mystr) >> yours.year;

  cout << "My favorite movie is:\n ";
  printmovie (mine);
  cout << "And yours is:\n ";
  printmovie (yours);

  cout << "\ndebug: 指针访问结构体" << endl;
  pmovie = &mine;
  cout << "You have entered:\n";
  cout << pmovie->title;
  cout << " (" << pmovie->year << ")\n";

  return 0;
}

void printmovie (movies_t movie)
{
  cout << movie.title;
  cout << " (" << movie.year << ")\n";
}