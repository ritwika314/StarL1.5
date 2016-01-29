
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

## Executing StarL High Level Language Programs

A program written in the high level language can only be executed through StarL. We provide the following scripts to do that : 

1. `generate-template` : Execute this script to generate the corresponding StarL application. It will ask for the path of the StarL installation. 
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
