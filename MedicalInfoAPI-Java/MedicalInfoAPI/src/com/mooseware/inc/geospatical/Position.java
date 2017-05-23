package com.mooseware.inc.geospatical;

public class Position {
	private double latitude;
	private double longitude;
	
	Position(double latitude, double longitude) throws Exception {
		if (latitude > 180.0d || latitude < -180.0d) {
			throw new Exception("Latitude is invalid");
		}
		if(longitude > 180.0d || longitude < -180.0d) {
			throw new Exception("Longitude is invalid");
		}
		
		this.latitude = latitude;
		this.longitude = longitude;
	}

	public double getLatitude() {
		return latitude;
	}

	public double getLongitude() {
		return longitude;
	}
	
	
}
