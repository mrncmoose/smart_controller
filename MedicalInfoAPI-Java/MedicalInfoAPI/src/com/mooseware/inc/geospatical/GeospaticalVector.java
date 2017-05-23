package com.mooseware.inc.geospatical;

public class GeospaticalVector {
	private double distance;
	private double bearing;
	
	GeospaticalVector(double distance, double bearing) throws Exception {
		if(bearing > 360.0d) {
			throw new Exception("Bearing can not be more than 360 degrees");
		} else {
			this.distance = distance;
			this.bearing = bearing;
		}
	}

	public double getDistance() {
		return distance;
	}

	public double getBearing() {
		return bearing;
	}
	
}
