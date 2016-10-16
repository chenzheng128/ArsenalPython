// basic file operations
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main () {
  string filename = "example.txt";
  cout << "== 写入字符串至 " << filename << endl;
  ofstream myfile;
  myfile.open (filename);
  myfile << "Writing this to a file 11.\n";
  myfile.close();

  //获取文件大小
  cout << "== 获取文件大小 \n";
  streampos begin,end;
  ifstream myfile2 (filename); // 二进制方式打开
  // ifstream myfile (filename, ios::binary); // 二进制方式打开
  begin = myfile2.tellg();
  myfile2.seekg (0, ios::end);
  end = myfile2.tellg();
  myfile2.close();
  cout << "  size is: " << (end-begin) << " bytes.\n";


  cout << "== 读取 binary 文件到内存\n";
  streampos size;
  char * memblock;

  ifstream file ("example.bin", ios::in|ios::binary|ios::ate); // ate 指针指向文件末尾
  if (file.is_open())
  {
    size = file.tellg();
    memblock = new char [size];
    file.seekg (0, ios::beg);
    file.read (memblock, size);
    file.close();

    cout << "  the entire file content is in memory";

    delete[] memblock;
  }
  else cout << "Unable to open file";

  return 0;
}