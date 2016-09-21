include <rasppi1.scad>;

module MP4_RP1_Support(){
	difference(){
		union(){
			difference(){
				union(){
					translate([56-13, 0, 0]) cube([58, 96, 3]);
					translate([56-23, 31, 0]) cube([22, 8, 3]);
					translate([8, 86, 0]) cube([48, 10, 3]);
				}
				translate([56, 10, -0.1]) cube([15, 65, 3.2]);
			}
			translate([56-18, 35.5, 0.1]) cylinder(r1=6/2,r2=6/2,h=5.9);
			translate([12.5, 96-5, 0.1]) cylinder(r1=6/2,r2=6/2,h=5.9);
			translate([56-6, 96-5, 0.1]) cylinder(r1=6/2,r2=6/2,h=5.9);
			translate([56-18, 35.5, 0.1]) cylinder(r1=2.4/2,r2=2.4/2,h=7);
		}
		translate([12.5, 96-5, -0.1]) cylinder(r1=2.9/2,r2=2.9/2,h=6.3);
	}
}


MP4_RP1_Support();
translate([0, 10, 8]) %RaspPiV1();