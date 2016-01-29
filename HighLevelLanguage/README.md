# Getting Started 

The StarL High Level Language is a distributed robotics programming language built on top of the StarL framework. It is designed to hide the low level details of programming distributed applications from developers, and allow them to work solely on the protocol. 


This is a readme file for the developers.

##Requirements 

### Java Development Kit (required JDK7 or higher)
You can download the required JDK at http://www.oracle.com/technetwork/java/javase/downloads/index.html

In Linux systems, to make sure that everything works you should be able to call `java -version` and
`javac -version` from a Terminal. For Windows and Mac users, find the Java Control Panel. Under the General tab in the Java Control Panel, the version can be checked from the About section. 


###Python 2.7.x 
Python 2 is required for the parser. Visit https://www.python.org/downloads/ to download and install python. 

### Python Lex Yacc (ply) 
python-ply is a requirement, you can download it at http://www.dabeaz.com/ply/ and install it through distutils using the provided setup.py file. It might be required to provide the full installation path of python, in case the path variable is not set properly. Linux users can install it using `sudo apt-get install python-ply`.

###Installation 
Ensure that you have the execute permissions the scripts `install`, `generate-template` and `run`. For a first time install, if you don't have StarL, use the `install` script: 
```
$./install
enter full path for StarL installation : 
/home/username/starl
```

##Introduction 

The main goal of this language is to allow users and developers to write distributed robotics protocols in an event driven fashion, possibly using shared variables to communicate information between robots. The present implementation assumes all participating robots will run the same instructions parallely. Support for some degree of heterogeneity will be provided in future versions. 

This language is primarily developed as an academic tool, to allow reasoning about distributed protocols in robotics, while hiding the low level implementation details, as well as shared data structure manipulation largely from the user. The high level nature of this language is meant to catch common programming mistakes made by novice users


## Writing StarL High Level Language Programs

We provide an overview of the structure of a StarL High Level program, which we will demonstrate with some illustrative examples that the user can work through, and provide the users template files to get started. 

A StarL High Level Language program consists of the following components:

1. Name of the application : Each robot can run different peices of code. To communicate that a certain protocol is being run, the program has to be named (similar to naming a class in object oriented programming).
2. Multiwriter , multi reader variable declaration block (possibly empty) : The robots use shared variables to communicate, and any such multiwriter variables used in a program are declared in a separate block specifically for this purpose.   
3. Local declarations (optional) : An application may or may not require local variables for computations. 
4. `Init` block : This is the peice of code that is executed by the robot, to monitor event triggers. It is similar to a Main function, except that it is a wrapper for ceontinuous monitoring of events. 
5. Event blocks : These are events which are triggered when a certain condition becomes true, and a robot executes instructions in response to these conditions becoming true. Event blocks are comprised of a) `pre` : a boolean condition which triggers the event upon being registered as true and b) `eff` : the set of statements which are executed by the robot after the event is triggered. 

The following examples demonstrate these components. 

### AddNums
Each robot has a `robotIndex`, an integer which is a unique identifier for that robot. This application computes the sum of the `robotIndex` values of all participating robots in a distributed fashion. 

```
Agent::AddNums
```
We follow the naming convention of the name of the application starting with an uppercase letter, like naming classes in Java.

We declare two multi-writer(MW) variables: `NumAdded`, (initialized to 0) to keep track of how many robots have added their robot index already, and `CurrentTotal`, which keeps track of the current sum. 

```
MW{
    int NumAdded = 0;
    int CurrentTotal = 0;
}
```
We also require a few local variables : `isFinal`, a boolean to indicate whether the current total is the final sum, `Added`, a boolean to indicate whether the robot (itself) has added its `robotIndex` to the total, and `FinalSum`, for storing the final sum. 

```
boolean isFinal = false;
boolean Added = false;
int FinalSum = 0;
```

Having declared all variables required for the computation, we can now write the `Init` block, which monitors events during the computation . 

```
Init() {
        getRobotIndex();
```
`getRobotIndex()` is an inbuilt function, which necessarily triggers the event of retrieving the `robotIndex` of the robot executing this program, and stores it in a reserved local variable called `robotIndex`. 


```        
        adding() {
                pre(Added == false);
                eff {
                        atomic{
                                Added = true;
                                CurrentTotal = CurrentTotal +robotIndex;
                                NumAdded = NumAdded+1;
                        }
                }
        }
```
The `adding` event is triggered when the `Added` variable is set to `false`, indicating that the robot has not yet added its `robotIndex` to the `CurrentTotal`. The effect of this event is then that the robot "atomically" tries to set the value of the `Added` variable to true, increments `CurrentTotal` by its `robotIndex` and increments `NumAdded` by 1.

```
        allAdded() {
                pre(NumAdded == NumBots && isFinal == false);
                eff {
                        FinalSum = CurrentTotal; isFinal = true;
                }
        }
```
Note 1: that the number of participating robots is known, and stored in a reserved variable called `NumBots`. The robot checks whether add participating robots have added their `robotIndex` by comparing `NumBots` and `NumAdded`.If this event is triggered, and if `isFinal` is set to `false`, then sets it to `true`, and updates the `FinalSum` to the value of the `CurrentTotal`.

```
        exit() {
                pre(isFinal);
                eff {
                }
        }

}
```
We also provide a special event called `exit` which indicates that no more events of this application need to be monitored after the effects of this event have executed, and we set the precondition for this event to be that `isFinal` is set to `true`. In this application, the effect of the `exit` event block is empty, but it need not be so for all applications. 
                   

Note 2: The event names have parameters, which are blank currently, that feature is under development, and will be released in a future version of this tool . 

### LeaderElect

Now we describe an app which performs a basic Leader Election, by comparing the `robotIndex` values of all participating robots, and electing the one with the highest `robotIndex` as leader. 

````
Agent::LeaderElect

MW{
	int numVotes = 0;
	int candidate = -1;

}
```
We require two MW variables: `numVotes` for keeping track of how many robots have "voted", and candidate for keeping track of which `robotIndex` was the highest amongst the robots that voted. The leader obviously, is found when all robots have voted. 

```

	int LeaderId = -1;
	boolean elected = false;
	boolean voted = false;
	boolean added = false;
```
We use 4 local variables, `LeaderId` which is the leader's `robotIndex`, set to -1 until the leader is found, `elected` for keeping track of whether a leader has been found, `voted` to keep track of whether this robot has voted, `added` to keep track of whether it has ensured that its vote is counted.

```
Init() {
	getRobotIndex();
	
voting(){
	pre(!voted && robotIndex > candidate) ;
	eff {
		atomic{
			if (robotIndex > candidate) {
				candidate = robotIndex;
			}	

			else {}
			
		}
		
	}
}
```
The `voting` event is triggered when the robot hasn't voted, and its index is greater than the candidate. The effect of this event atomically checks whether the `robotIndex` is still greater than the `candidate`, and updates the `candidate` if that is the case, does nothing otherwise. This action needs to be atomic (The answet to why is left as an exercise) . 

```
voted(){
	pre(!voted && robotIndex < candidate);
	eff {
		voted = true;
	}
}
```
The `voted` event is triggered when the candidate has not set its `voted` to `true`, but its `robotIndex` is less than the `candidate`. The effect is setting `voted` to `true`.

```
adding(){
	pre(!added);
	eff{
		atomic{
			added = true;
			numVotes = numVotes+1;
		}

	}

}
```
The `adding` event is triggered when it has not added its vote to the `numVotes`. It is not necessary to check whether `voted == true`, as the events are triggered in order of appearance in the `Init` block if all their preconditions are true at once. 

```
electing(){
	pre(numVotes == NumBots && !elected);
	eff{
		elected = true;
		LeaderId = candidate;
	}

}
```
The `electing` event checks whether all votes have been casted, and sets the `elected` variable, and `LeaderId`. 

```
exit(){
	pre(elected);
	eff{
	}
}
}
```
We again opted to leave the exit event empty. 

## Executing StarL High Level Language Programs

A program written in the high level language can only be executed through StarL. We provide the following scripts to do that : 

1. `generate-template` : Execute this script to generate the corresponding StarL application. It will ask for the path of the StarL installation. Ensure that you are in the directory containing this script while running it. Also, ensure that the High Level Language program you are running is stored in the `HighLevelLanguage/examples` folder, in a folder with the same name as the program itself. For instance, `AddNums` is stored in `HighLevelLanguage/examples/AddNums`. 
```
$./generate-template AddNums
enter StarL installation path:
/home/username/starl
```
2. To run the application,
```
$./run AddNums
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
