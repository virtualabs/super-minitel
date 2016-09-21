$fn=200;

module AudioAmp(){
	difference(){
		cube([18.4, 37.8, 1.6]);
		translate([12.8, 18.4-6.3, -0.1]) cylinder(r1=1, r2=1, h=1.8);
	}
}

