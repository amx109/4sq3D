/******** **********/


difference()
{
	mirror([0,1]) //do this to get the correct orientation
	surface(file = "foursquare.dat", center = true, convexity = 100);
	
	
	import_dxf(file = "ams_water.dxf");
	
}


