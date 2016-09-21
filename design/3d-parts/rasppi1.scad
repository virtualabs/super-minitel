$fn=100;

module RP1_support(){

	difference(){
		color("green") cube([56, 86, 1.6]);
		translate([56-18, 25.5, -0.1]) cylinder(r1=2.9/2, r2=2.9/2, h=1.8);
		translate([12.5, 81, -0.1]) cylinder(r1=2.9/2, r2=2.9/2, h=1.8);
	}
}

module RP1_connectors(){
	color("yellow") translate([-6.5, 41, 1.6]) cube([20,10, 13]); 
	color("blue") translate([-4, 86-14.6-12, 1.6]) cube([15, 12, 10]);
	color("grey") translate([19, 86-10, 1.6]) cube([13.5, 18, 16]);
	color("grey") translate([56-18, 86-20, 1.6]) cube([16, 22, 14]);
}

module RaspPiV1(){

	RP1_support();
	RP1_connectors();
}

