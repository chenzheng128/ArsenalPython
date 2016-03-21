#pygame

使用 python 播放音频

## 运行方法
```
python3 pygame_demo_audio.py
```

## 运行版本环境
```
xxx$ python3
Python 3.5.1 (default, Jan 22 2016, 08:54:32)
[GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pygame
>>> pygame.get_sdl_version()
(1, 2, 15)
>>> pygame.version.ver
'1.9.2a0'
```

##pygame安装参考
下载与安装： http://www.pygame.org/download.shtml

###Mac OSX 安装
Source: http://pygame.org/wiki/macintosh

```
brew install python3 hg sdl sdl_image sdl_ttf portmidi libvorbis  sdl_mixer --with-libvorbis
hg clone http://bitbucket.org/pygame/pygame
python3 setup.py build
CC=/usr/bin/gcc python3 setup.py build
sudo python3 setup.py install
```

TODO: 待解决 mp3播放问题： https://github.com/justinmeister/Mario-Level-1/issues/5
