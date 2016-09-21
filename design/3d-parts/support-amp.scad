include <audio-amp.scad>

module SupportAmp(){
	union(){
		difference(){
			cube([66, 28, 2]);
			translate([52, 9+5, -0.1]) cylinder(r1=9.15, r2=9.15, h=2.2);
			translate([52-4, -0.1, -0.1]) cube([8, 10, 2.2]);
		}
		translate([26+2.2, 5.25+18.4-6.3, 0.1]){
			difference(){		
				cylinder(r1=3,r2=3,h=4);
				translate([0,0,1.9]) cylinder(r1=1,r2=1,h=2.2);
			}
		}
		cube([2, 50+14, 10]);
	}
}

translate([2.2+38, 5.25, 6]) rotate([0,0,90]) %AudioAmp();
SupportAmp();

