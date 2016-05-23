package edu.illinois.mitra.demo.formation;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Stroke;

import edu.illinois.mitra.starl.interfaces.LogicThread;
import edu.illinois.mitra.starl.objects.ItemPosition;
import edu.illinois.mitra.starlSim.draw.Drawer;

public class FormationDrawer extends Drawer  {

     private Stroke stroke = new BasicStroke(8);        private Color selectColor = new Color(0,0,255,100);
        @Override
        public void draw(LogicThread lt, Graphics2D g) {
                FormationApp app = (FormationApp) lt;
                g.setColor(Color.RED);
                g.setColor(selectColor);
                g.setStroke(stroke);
                if(app.position != null){
                
                }
        }

}