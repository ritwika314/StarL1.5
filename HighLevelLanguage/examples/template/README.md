/home/username/starl

## Writing StarL High Level Language Programs

We provide an overview of the structure of a StarL High Level program, which we will demonstrate with some illustrative examples that the user can work through, and provide the users template files to get started. 

A StarL High Level Language program consists of the following components:

1. Name of the application : Each robot can run different peices of code. To communicate that a certain protocol is being run, the program has to be named (similar to naming a class in object oriented programming).
2. Multiwriter , multi reader variable declaration block (possibly empty) : The robots use shared variables to communicate, and any such multiwriter variables used in a program are declared in a separate block specifically for this purpose.   
3. Local declarations (optional) : An application may or may not require local variables for computations. 
4. `Init` block : This is the peice of code that is executed by the robot, to monitor event triggers. It is similar to a Main function, except that it is a wrapper for ceontinuous monitoring of events. 
5. Event blocks : These are events which are triggered when a certain condition becomes true, and a robot executes instructions in response to these conditions becoming true. Event blocks are comprised of a) `pre` : a boolean condition which triggers the event upon being registered as true and b) `eff` : the set of statements which are executed by the robot after the event is triggered. 


This is a template file for writing high level programs for StarL. 

## Executing StarL High Level Language Programs

A program written in the high level language can only be executed through StarL. We provide the following scripts to do that : 

1. `generate-template` : Execute this script to generate the corresponding StarL application. It will ask for the path of the StarL installation. 
```
$./generate-template <AppName>
enter StarL installation path:
/home/username/starl
```
2. To run the application,
```
$./run <AppName>
enter StarL installation path:
/home/username/starl
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
