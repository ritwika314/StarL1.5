package edu.illinois.mitra.demo.addnums;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Stroke;

import edu.illinois.mitra.starl.interfaces.LogicThread;
import edu.illinois.mitra.starl.objects.ItemPosition;
import edu.illinois.mitra.starlSim.draw.Drawer;

public class AddNumsDrawer extends Drawer  {

     private Stroke stroke = new BasicStroke(8);        private Color selectColor = new Color(0,0,255,100);
        @Override
        public void draw(LogicThread lt, Graphics2D g) {
                AddNumsApp app = (AddNumsApp) lt;
                g.setColor(Color.RED);
                g.setColor(selectColor);
                g.setStroke(stroke);
                if(app.position != null){
                			g.drawString("NumAdded"+" = "+String.valueOf(app.NumAdded),app.position.x,app.position.y+0);
			g.drawString("CurrentTotal"+" = "+String.valueOf(app.CurrentTotal),app.position.x,app.position.y+50);

                }
        }

}