# System Requirements 

### Java Development Kit (required JDK7 or higher)
You can download the required JDK at http://www.oracle.com/technetwork/java/javase/downloads/index.html

In Linux systems, to make sure that everything works you should be able to call `java -version` and
`javac -version` from a Terminal. For Windows and Mac users, find the Java Control Panel. Under the General tab in the Java Control Panel, the version can be checked from the About section. 


###Python 2.7.x 
Python 2 is required for the parser. Visit https://www.python.org/downloads/ to download and install python. 

### Python Lex Yacc (ply) 
python-ply is a requirement, you can download it at http://www.dabeaz.com/ply/ and install it through distutils using the provided setup.py file by running the command `python setup.py install`. 

It might be required to provide the full installation path of python, in case the path variable is not set properly. Linux users can install it using `sudo apt-get install python-ply`.

###Installation 
Ensure that you have the execute permissions the scripts `generate-template` and `run`. 

Note : Details about the High Level Language are provided [here](https://github.com/ritwika314/StarL1.5/blob/master/HighLevelLanguage/Writing%20High%20Level%20Language%20Programs.md)
## Executing StarL High Level Language Programs

A program written in the high level language can only be executed through StarL. We provide the following scripts to do that : 

1. `generate-template` : Execute this script to generate the corresponding StarL application. It will ask for the path of the StarL installation. Ensure that you are in the directory containing this script while running it. Also, ensure that the High Level Language program you are running is stored in the `HighLevelLanguage/examples` folder, in a folder with the same name as the program itself. For instance, `AddNums` is stored in `HighLevelLanguage/examples/AddNums`. 
```
$./generate-template AddNums
```
2. To run the application,
```
$./run AddNums
```

NOTE: The generated drawer files are basic. In order to get more sophisticated simulation drawings, the user has to modify the drawer files themselves, in the StarL application. For instance, to modify the drawer of the AddNums application, the user can modify to the AddNumsDrawer.java file, which can be located from the following directory structure of StarL (provided `generate-template` was already used) . 
```
StarL1.5/
..
├── trunk
│   ├── android
..
|.. |.. └── AddNums
│   │       ├── src
│   │       │   └── edu
│   │       │       └── illinois
│   │       │           └── mitra
│   │       │               └── demo
│   │       │                   └── addnums
│   │       │                       ├── Main.java
│   │       │                       ├── AddNumsApp.java
│   │       │                       └── AddNumsDrawer.java
..
│   └── README
└── Using the StarL Framework.pdf

```


The naming conventions we follow dictate that given an app, the generated StarL application will contain a file called `<AppName>App.java`, which contains the declarations, events of the app, `<AppName>Drawer.java`, the file which draws the simulation, and `Main.java`, which is the main file. If the user wishes to modify these files, they need to just execute the `run` script again, to build and run this app again. 

Note : This tool is under development, and this version is for academic usage only. Any issues or questions can be addressed to rghosh9@illinois.edu and lin127@illinois.edu. 
