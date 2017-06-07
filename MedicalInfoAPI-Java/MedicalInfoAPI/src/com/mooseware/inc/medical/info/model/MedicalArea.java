package com.mooseware.inc.medical.info.model;

import java.io.Serializable;
import java.lang.String;
import javax.persistence.*;

/**
 * Entity implementation class for Entity: AreaOfUse
 *
 */
@Entity
public class MedicalArea implements Serializable {	   
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int medicalAreaId;
	@Column(nullable=false, unique=true)
	private String name;
	@Column(nullable=false)
	private String floor;
	@Column(columnDefinition="POLYGON", nullable=false)
	private LatLong[] location;
	//NOTE:  for POC, each room has only one beacon
	private Beacon beacon;
	private static final long serialVersionUID = 1L;

	public MedicalArea() {
		super();
	}   
	public int getMedicalAreaId() {
		return medicalAreaId;
	}

	public void setMedicalAreaId(int medicalAreaId) {
		this.medicalAreaId = medicalAreaId;
	}

	public String getName() {
		return this.name;
	}

	public void setName(String name) {
		this.name = name;
	}   
	public String getFloor() {
		return this.floor;
	}

	public void setFloor(String floor) {
		this.floor = floor;
	}   
	public LatLong[] getLocation() {
		return this.location;
	}

	public void setLocation(LatLong[] location) {
		this.location = location;
	}
	public Beacon getBeacon() {
		return beacon;
	}
	public void setBeacon(Beacon beacon) {
		this.beacon = beacon;
	}
   
}
