package edu.illinois.mitra.demo.dummy;

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


public class DummyApp extends LogicThread {

	private DSM dsm;
	public int NumAdded = 0;
	public int Changed = 0;
	public int CurrentTotal = 0;
	public 	final Map<String,ItemPosition> destinations = new HashMap<String,ItemPosition>();

	private MutualExclusion mutex;
	private int NumBots = 0;
	int robotIndex = 0;
	private static final boolean RANDOM_DESTINATION = false;
	public static final int ARRIVED_MSG = 22;
	PositionList<ItemPosition> destinationsHistory = new PositionList<ItemPosition>();
	PositionList<ItemPosition> doReachavoidCalls = new PositionList<ItemPosition>();
	public RRTNode kdTree;
	public ItemPosition position;
	public boolean isFinal = false;
	public boolean Added = false;
	public ItemPosition currentDestination;
	public ObstacleList obs;
	public int FinalSum = 0;
	public enum Stage {PICK,GO,FAIL,DONE,};
	Stage stage = Stage.PICK;

	public boolean wait0 = false;
	public DummyApp(GlobalVarHolder gvh) {
		super(gvh);
		robotIndex = Integer.parseInt(name.replaceAll("[^0-9]",""));
		mutex = new GroupSetMutex(gvh,0);
		dsm = new DSMMultipleAttr(gvh);
		MotionParameters.Builder settings = new MotionParameters.Builder();
		settings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLAVOID);
		MotionParameters param = settings.build();
		gvh.plat.moat.setParameters(param);
		for(ItemPosition i : gvh.gps.getWaypointPositions()){
			destinations.put(i.getName(), i);
		}
		gvh.comms.addMsgListener(this,ARRIVED_MSG);
		obs= gvh.gps.getObspointPositions();
	}
		@Override
		public List<Object> callStarL() {
			dsm.createMW("NumAdded", 0);
			dsm.createMW("Changed", 0);
			dsm.createMW("CurrentTotal", 0);
			position = gvh.gps.getMyPosition();
			while(true) {
				sleep(100);
				if(gvh.plat.model instanceof Model_quadcopter){
					gvh.log.i("WIND", ((Model_quadcopter)gvh.plat.model).windxNoise + " " +  ((Model_quadcopter)gvh.plat.model).windyNoise);
				}


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


				if(stage ==Stage.PICK) {
//if then else condition
					if(destinations.isEmpty()) {
//code for : stage = Stage.DONE:stage = Stage.DONE;

						
						stage = Stage.DONE;

					}
					else {
						currentDestination=getRandomElement(destinations);

//code for : Added = true:Added = true;

						
						Added = true;

						gvh.plat.reachAvoid.doReachAvoid(gvh.gps.getMyPosition(),currentDestination,obs);
						kdTree = gvh.plat.reachAvoid.kdTree;
						gvh.log.i("DoReachAvoid",currentDestination.x + " " +currentDestination.y);
						doReachavoidCalls.update(new ItemPosition(name + "'s " + "doReachAvoid Call to destination: " +currentDestination.name, gvh.gps.getMyPosition().x,gvh.gps.getMyPosition().y));

//code for : stage = Stage.GO:stage = Stage.GO;

						
						stage = Stage.GO;

					}

					continue;
				}


				if(stage ==Stage.GO) {
//if then else condition
					if(gvh.plat.reachAvoid.doneFlag) {
//code for : stage = Stage.PICK:stage = Stage.PICK;

						
						stage = Stage.PICK;

					}
					else {
					}

//if then else condition
					if(gvh.plat.reachAvoid.failFlag) {
//code for : stage = Stage.FAIL:stage = Stage.FAIL;

						
						stage = Stage.FAIL;

					}
					else {
					}

					continue;
				}


				if(stage ==Stage.DONE) {
//code for : CurrentTotal = 1000:dsm.put("CurrentTotal","*",1000);
					
					dsm.put("CurrentTotal","*",1000);
//code for : stage = Stage.PICK:stage = Stage.PICK;

					
					stage = Stage.PICK;

					continue;
				}


			}
		}
	@Override
	protected void receive(RobotMessage m) {
	String posName = m.getContents(0);
	if(destinations.containsKey(posName))
			destinations.remove(posName);
	if(currentDestination.getName().equals(posName)) {
		//	gvh.plat.moat.cancel();
			gvh.plat.reachAvoid.cancel();
			stage = Stage.PICK;
		}
	}
private static final Random rand = new Random();
	@SuppressWarnings("unchecked")
	private <X, T> T getRandomElement(Map<X, T> map) {
 		if(RANDOM_DESTINATION)
			return (T) map.values().toArray()[rand.nextInt(map.size())];
		else
			return (T) map.values().toArray()[0];
	}
}