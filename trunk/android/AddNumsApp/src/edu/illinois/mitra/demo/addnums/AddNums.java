package edu.illinois.mitra.demo.addnums;

import java.util.HashMap;import java.util.Map;import java.util.Random;import java.util.List;

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


public class AddNums extends LogicThread {

	private DSM dsm;
	public int NumAdded = 0;
	public int CurrentTotal = 0;
	private MutualExclusion mutex;
	private int NumBots = 0;
	int robotIndex = 0;
	public boolean isFinal = false;
	public boolean Added = false;
	public int FinalSum = 0;
	public boolean wait0 = false;
	ItemPosition position ;
	public AddNums(GlobalVarHolder gvh) {
		super(gvh);
		robotIndex = Integer.parseInt(name.replaceAll("[^0-9]",""));
		mutex = new GroupSetMutex(gvh,0);
		dsm = new DSMMultipleAttr(gvh);
	}
		@Override
		public List<Object> callStarL() {
			dsm.createMW("NumAdded", 0);
			dsm.createMW("CurrentTotal", 0);
			position = gvh.gps.getMyPosition();
			while(true) {
				sleep(100);


				if(Added ==false) {
					if(!wait0){
						NumBots = gvh.gps.get_robot_Positions().getNumPositions();
						mutex.requestEntry(0);
						wait0 = true;
					}

					 if(mutex.clearToEnter(0)) {
//code for : Added = true:Added = true;

						
						Added = true;

//code for : CurrentTotal = CurrentTotal + robotIndex:dsm.put("CurrentTotal","*",CurrentTotal + robotIndex);
						CurrentTotal = Integer.parseInt(dsm.get("CurrentTotal","*"));
						
						dsm.put("CurrentTotal","*",CurrentTotal + robotIndex);
//code for : NumAdded = NumAdded + 1:dsm.put("NumAdded","*",NumAdded + 1);
						NumAdded = Integer.parseInt(dsm.get("NumAdded","*"));
						
						dsm.put("NumAdded","*",NumAdded + 1);
						mutex.exit(0);
					}

					continue;
				}


				if(Integer.parseInt(dsm.get("NumAdded","")) ==NumBots &&isFinal ==false) {
//code for : FinalSum = CurrentTotal:FinalSum = CurrentTotal;

					CurrentTotal = Integer.parseInt(dsm.get("CurrentTotal","*"));

					FinalSum = CurrentTotal;

//code for : isFinal = true:isFinal = true;

					
					isFinal = true;

					continue;
				}


				if(isFinal) {
					continue;
				}


			}
		}
	@Override
	protected void receive(RobotMessage m) {
	}
}