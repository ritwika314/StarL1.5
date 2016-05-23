package edu.illinois.mitra.demo.formation;

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


public class FormationApp extends LogicThread {

	private DSM dsm;
	public 	final Map<String,ItemPosition> destinations = new HashMap<String,ItemPosition>();

	private static final boolean RANDOM_DESTINATION = false;
	public static final int ARRIVED_MSG = 22;
	PositionList<ItemPosition> destinationsHistory = new PositionList<ItemPosition>();
	PositionList<ItemPosition> doReachavoidCalls = new PositionList<ItemPosition>();
	public RRTNode kdTree;
	public ItemPosition position;
	public enum Stage {PICK,GO,DONE,FAIL,};
	Stage stage = Stage.PICK;

	public ItemPosition currentDestination;
	public ObstacleList obs;
	public FormationApp(GlobalVarHolder gvh) {
		super(gvh);
		dsm = new DSMMultipleAttr(gvh);
		MotionParameters.Builder settings = new MotionParameters.Builder();
		settings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLAVOID);
		MotionParameters param = settings.build();
		gvh.plat.moat.setParameters(param);
		gvh.comms.addMsgListener(this,ARRIVED_MSG);
		obs= gvh.gps.getObspointPositions();
	}
		@Override
		public List<Object> callStarL() {
			position = gvh.gps.getMyPosition();
			while(true) {
				sleep(100);
				if(gvh.plat.model instanceof Model_quadcopter){
					gvh.log.i("WIND", ((Model_quadcopter)gvh.plat.model).windxNoise + " " +  ((Model_quadcopter)gvh.plat.model).windyNoise);
				}
				if(stage ==Stage.PICK) {
//if then else condition
					if(destinations.isEmpty()) {
//code for : stage = Stage.DONE:stage = Stage.DONE;

						
						stage = Stage.DONE;

					}
					else {
						currentDestination=getRandomElement(destinations);

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
//if then else condition
						if(currentDestination !=null) {
							destinations.remove(currentDestination.getName());

						}
						else {
						}

						RobotMessage inform = new RobotMessage("ALL", name, ARRIVED_MSG,currentDestination.getName());
						gvh.comms.addOutgoingMessage(inform);

//code for : stage = Stage.PICK:stage = Stage.PICK;

						
						stage = Stage.PICK;

					}
					else {
					}

//if then else condition
					if(gvh.plat.reachAvoid.failFlag) {
						gvh.log.i("Failflag", "read");

//code for : stage = Stage.FAIL:stage = Stage.FAIL;

						
						stage = Stage.FAIL;

					}
					else {
					}

					continue;
				}


				if(stage ==Stage.FAIL) {
					System.out.println(gvh.log.getLog());

					continue;
				}


				if(stage ==Stage.DONE) {
					System.out.println(gvh.log.getLog());

					return null;

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