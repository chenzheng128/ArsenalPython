## 完成 cplusplus.com 例子

这个网站的内容很好, 是独立的 C++ 内容 (不需要另外的 C 语言内容), 包含直接链接 api 文档, 完整代码可以直接在运行与调试工具: http://cpp.sh/6wq5 进行测试与演示.

Source http://www.cplusplus.com/doc/tutorial/


在 Mac OSX 10.11.3 EI Captian 编译通过

```
$ g++ -v
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1```
Apple LLVM version 7.3.0 (clang-703.0.31)
Target: x86_64-apple-darwin15.3.0C++ Language
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/binThese tutorials explain the C++ language from its basics up to the newest features introduced by C++11. Chapters have a practical orientation, with example programs in all sections to start practicing what is being explained right away.
```

## 章节目录

* ch01: Introduction
    - Compilers
* ch02: Basics of C++
    - Structure of a program: `ch02_program_structure.cpp`
    - Variables and types: `ch02_variables.cpp`
    - Constants: `ch02_constants.cpp`
    - Operators: `ch02_operators.cpp`
    - Basic Input/Output: `ch02_basic_io.cpp`
* ch03: Program structure: `ch02_operators.cpp`
    - Control Structures:  `ch03_control.cpp`
    - Functions: `ch03_functions.cpp`
    - Overloads and templates: `ch03_overload_template.cpp`
    - Name visibility: `ch03_namespaces.cpp`
* ch04: Compound data types
    - Arrays: `ch04_arrays.cpp`
    - Character sequences: `ch04_chars.cpp`
    - Pointers: `pointers.cpp`
    - Dynamic Memory: `ch04_dynamic.cpp`
    - Data structures: `ch04_structures.cpp`
    - Other data types: `ch04_other_data_types.cpp`
* ch05: Classes
    - Classes (I)
    - Classes (II)
    - Special members
    - Friendship and inheritance
    - Polymorphism
* ch06: Other language features: 
    - Type conversions: `ch06_typecasting.cpp`
    - Exceptions: `ch06_exceptions.cpp`
    - Preprocessor directives: `ch06_preprocessor.cpp`
* ch07: C++ Standard Library
    - Input/Output with files: `ch07_files.cpp`



知识点备忘

* move constructor 只能用在未命名的对象上, move 之后, destination 对象就接管了原来 source 的数据空间.  "The move constructor is called when an object is initialized on construction using an unnamed temporary." 
http://www.cplusplus.com/doc/tutorial/classes2/ 