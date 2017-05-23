package com.mooseware.inc.medical.info.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

// The data used to correct the difference between the IPS reported coordinates and the actual
// assumes each site will be a constant offset vector.
@Entity
public class PossitionCorrection {
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int	siteId;
	@Column(nullable=false, unique=true)
	private String siteName;
	@Column(nullable=false)
	private Float distance;
	@Column(nullable=false)
	private Float bearing;
	public int getSiteId() {
		return siteId;
	}
	public void setSiteId(int siteId) {
		this.siteId = siteId;
	}
	public String getSiteName() {
		return siteName;
	}
	public void setSiteName(String siteName) {
		this.siteName = siteName;
	}
	public Float getDistance() {
		return distance;
	}
	public void setDistance(Float distance) {
		this.distance = distance;
	}
	public Float getBearing() {
		return bearing;
	}
	public void setBearing(Float bearing) {
		this.bearing = bearing;
	}
}
