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
Note 1: that the number of participating robots is known, and stored in a reserved variable called `NumBots`. The robot checks whether add participating robots have added their votes by comparing `NumBots` and `numVotes`.

The `electing` event thus checks whether all votes have been casted, and sets the `elected` variable, and `LeaderId`. 

```
exit(){
	pre(elected);
	eff{
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
$./generate-template LeaderElect
enter StarL installation path:
/home/username/starl
```
2. To run the application,
```
$./run LeaderElect
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
|.. |.. └── LeaderElect
│   │       ├── src
│   │       │   └── edu
│   │       │       └── illinois
│   │       │           └── mitra
│   │       │               └── demo
│   │       │                   └── leaderelect
│   │       │                       ├── Main.java
│   │       │                       ├── LeaderElectApp.java
│   │       │                       └── LeaderElectDrawer.java
..
│   └── README
└── Using the StarL Framework.pdf

```


The naming conventions we follow dictate that given an app, the generated StarL application will contain a file called `<AppName>App.java`, which contains the declarations, events of the app, `<AppName>Drawer.java`, the file which draws the simulation, and `Main.java`, which is the main file. If the user wishes to modify these files, they need to just execute the `run` script again, to build and run this app again. 

Note : This tool is under development, and this version is for academic usage only. Any issues or questions can be addressed to rghosh9@illinois.edu and lin127@illinois.edu. 
