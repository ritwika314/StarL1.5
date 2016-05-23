package edu.illinois.mitra.demo.leaderelect;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.List;

import edu.illinois.mitra.starl.comms.RobotMessage;
import edu.illinois.mitra.starl.functions.DSMMultipleAttr;
import edu.illinois.mitra.starl.functions.SingleHopMutualExclusion;
import edu.illinois.mitra.starl.functions.GroupSetMutex;
import edu.illinois.mitra.starl.gvh.GlobalVarHolder;
import edu.illinois.mitra.starl.interfaces.DSM;
import edu.illinois.mitra.starl.interfaces.LogicThread;
import edu.illinois.mitra.starl.models.Model_quadcopter;
import edu.illinois.mitra.starl.motion.RRTNode;
import edu.illinois.mitra.starl.motion.MotionParameters;
import edu.illinois.mitra.starl.motion.MotionParameters.COLAVOID_MODE_TYPE;
import edu.illinois.mitra.starl.interfaces.MutualExclusion;
import edu.illinois.mitra.starl.objects.ItemPosition;
import edu.illinois.mitra.starl.objects.ObstacleList;
import edu.illinois.mitra.starl.objects.PositionList;


public class LeaderElectApp extends LogicThread {

	private DSM dsm;
	public int numVotes = 0;
	public int candidate = -1;
	private MutualExclusion mutex;
	private int NumBots = 0;
	int robotIndex = 0;
	public ItemPosition position;
	public int LeaderId = -1;
	public boolean elected = false;
	public boolean voted = false;
	public boolean added = false;
	public boolean wait0 = false;
	public boolean wait1 = false;
	public LeaderElectApp(GlobalVarHolder gvh) {
		super(gvh);
		robotIndex = Integer.parseInt(name.replaceAll("[^0-9]",""));
		mutex = new GroupSetMutex(gvh,0);
		dsm = new DSMMultipleAttr(gvh);
	}
		@Override
		public List<Object> callStarL() {
			dsm.createMW("numVotes", 0);
			dsm.createMW("candidate", 0);
			position = gvh.gps.getMyPosition();
			while(true) {
				sleep(100);
				if(gvh.plat.model instanceof Model_quadcopter){
					gvh.log.i("WIND", ((Model_quadcopter)gvh.plat.model).windxNoise + " " +  ((Model_quadcopter)gvh.plat.model).windyNoise);
				}


				if(!(voted) &&robotIndex >Integer.parseInt(dsm.get("candidate",""))) {
					if(!wait0){
						NumBots = gvh.gps.get_robot_Positions().getNumPositions();
						mutex.requestEntry(0);
						wait0 = true;
					}

					 if(mutex.clearToEnter(0)) {
//if then else condition
						if(robotIndex >Integer.parseInt(dsm.get("candidate",""))) {
//code for : candidate = robotIndex:dsm.put("candidate","*",robotIndex);
							
							dsm.put("candidate","*",robotIndex);
						}
						else {
						}

						mutex.exit(0);
					}

					continue;
				}


				if(!(voted) &&robotIndex <Integer.parseInt(dsm.get("candidate",""))) {
//code for : voted = true:voted = true;

					
					voted = true;

					continue;
				}


				if(!(added)) {
					if(!wait1){
						NumBots = gvh.gps.get_robot_Positions().getNumPositions();
						mutex.requestEntry(0);
						wait1 = true;
					}

					 if(mutex.clearToEnter(0)) {
//code for : added = true:added = true;

						
						added = true;

//code for : numVotes = numVotes + 1:dsm.put("numVotes","*",numVotes + 1);
						numVotes = Integer.parseInt(dsm.get("numVotes","*"));
						
						dsm.put("numVotes","*",numVotes + 1);
						mutex.exit(0);
					}

					continue;
				}


				if(Integer.parseInt(dsm.get("numVotes","")) ==NumBots &&!(elected)) {
//code for : elected = true:elected = true;

					
					elected = true;

//code for : LeaderId = candidate:LeaderId = candidate;

					candidate = Integer.parseInt(dsm.get("candidate","*"));

					LeaderId = candidate;

					continue;
				}


				if(elected) {
					continue;
				}


			}
		}
	@Override
	protected void receive(RobotMessage m) {
	}
}