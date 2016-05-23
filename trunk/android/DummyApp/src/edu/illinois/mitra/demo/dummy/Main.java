package edu.illinois.mitra.demo.dummy;
import edu.illinois.mitra.starlSim.main.SimSettings;
import edu.illinois.mitra.starlSim.main.Simulation;

public class Main {
        public static void main(String[] args) {
                SimSettings.Builder settings = new SimSettings.Builder();
                settings.N_IROBOTS(4);
                settings.TIC_TIME_RATE(1.5);
        settings.WAYPOINT_FILE("four.wpt");
                settings.DRAW_WAYPOINTS(false);
                settings.DRAW_WAYPOINT_NAMES(false);
                settings.DRAWER(new DummyDrawer());

                Simulation sim = new Simulation(DummyApp.class, settings.build());
                sim.start();
        }
}