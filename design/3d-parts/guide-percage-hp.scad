$fn=200;

module TrousHP(){
	for (rad = [0:45:360]) {
		rotate([0,0,rad]) translate([10,0,-0.1]) cylinder(r1=1.2, r2=1.2, h=10.4);
		rotate([0,0,rad]) translate([15,0,-0.1]) cylinder(r1=1.2, r2=1.2, h=10.4);
		rotate([0,0,rad]) translate([20,0,-0.1]) cylinder(r1=1.2, r2=1.2, h=10.4);
	}
}

module GuidePercageHP(){
	union(){
		difference(){
			cylinder(r1=30, r2=30, h=5);
			TrousHP();		
			translate([0,0,-0.1]) cylinder(r1=1.2, r2=1.2, h=5.4);
		}
		translate([25,-10,0]) cube([40,20,5]);
		//translate([-45,-10,0]) cube([20,20,5]);
	}
}

GuidePercageHP();