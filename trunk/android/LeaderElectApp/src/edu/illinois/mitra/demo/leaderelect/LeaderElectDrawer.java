package edu.illinois.mitra.demo.leaderelect;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Stroke;

import edu.illinois.mitra.starl.interfaces.LogicThread;
import edu.illinois.mitra.starl.objects.ItemPosition;
import edu.illinois.mitra.starlSim.draw.Drawer;

public class LeaderElectDrawer extends Drawer  {

     private Stroke stroke = new BasicStroke(8);        private Color selectColor = new Color(0,0,255,100);
        @Override
        public void draw(LogicThread lt, Graphics2D g) {
                LeaderElectApp app = (LeaderElectApp) lt;
                g.setColor(Color.RED);
                g.setColor(selectColor);
                g.setStroke(stroke);
                if(app.position != null){
                			g.drawString("numVotes"+" = "+String.valueOf(app.numVotes),app.position.x,app.position.y+0);
			g.drawString("candidate"+" = "+String.valueOf(app.candidate),app.position.x,app.position.y+50);

                }
        }

}