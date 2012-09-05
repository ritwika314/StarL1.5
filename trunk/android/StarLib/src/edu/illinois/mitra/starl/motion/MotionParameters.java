package edu.illinois.mitra.starl.motion;

/**
 * A MotionParameters object contains settings describing speeds and options to use in motion. 
 * @author Adam Zimmerman
 * @see RobotMotion
 * @see MotionAutomaton
 */
public class MotionParameters {

	public int TURNSPEED_MAX = 110;
	public int TURNSPEED_MIN = 25;
	
	public int LINSPEED_MAX = 175;
	public int LINSPEED_MIN = 250;
	
	/**
	 * If false, the robot will continue whatever motion was in progress when the destination is reached
	 */
	public boolean STOP_AT_DESTINATION = true;
	
	public boolean ENABLE_ARCING = true;
	public int ARCSPEED_MAX = 200;
	public int ARCANGLE_MAX = 25;
	
	/**
	 * Sets the collision avoidance mode. Options are:</br>
	 * USE_COLAVOID - use the standard collision avoidance algorithm</br>
	 * STOP_ON_COLLISION - stop if a collision is imminent and don't resume until the blocker moves</br>
	 * BUMPERCARS - ignore collision detection and just keep going no matter what</br>
	 */
	public COLAVOID_MODE_TYPE COLAVOID_MODE = COLAVOID_MODE_TYPE.USE_COLAVOID;	
	
	public static enum COLAVOID_MODE_TYPE { USE_COLAVOID, STOP_ON_COLLISION, BUMPERCARS };
}
