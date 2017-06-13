package com.mooseware.inc.medical.info.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Beacon  implements Serializable{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1197780948496416102L;

	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int beaconId;
	
	@Column(nullable=false)
	private String uuid;
	@Column(nullable=false)
	private int major;
	@Column(nullable=false)
	private int minor;
	@Column(nullable=true)
	private String name;
	
	
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public int getBeaconId() {
		return beaconId;
	}
	public void setBeaconId(int beaconId) {
		this.beaconId = beaconId;
	}
	public String getUuid() {
		return uuid;
	}
	public void setUuid(String uuid) {
		this.uuid = uuid;
	}
	public int getMajor() {
		return major;
	}
	public void setMajor(int major) {
		this.major = major;
	}
	public int getMinor() {
		return minor;
	}
	public void setMinor(int minor) {
		this.minor = minor;
	}
	
}
