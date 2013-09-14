
	//mirror([0,1])
	//surface(file = "foursquare.dat", center = true, convexity = 5);
	
linear_extrude(height = 2, center = false)
import_dxf(file = "ams_water.dxf");
