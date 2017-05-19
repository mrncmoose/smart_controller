package com.mooseware.inc.medical.info.model;

import java.io.Serializable;
import java.lang.Integer;
import java.lang.String;
import javax.persistence.*;

import org.eclipse.persistence.annotations.ExistenceChecking;
import org.eclipse.persistence.annotations.ExistenceType;

/**
 * Entity implementation class for Entity: Patient
 *
 */
//TODO:  Any given patient may be in one or more EMR systems.
@Entity
@ExistenceChecking(ExistenceType.CHECK_DATABASE)
public class Patient implements Serializable {
	   
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private Integer patientId;
	@Column(nullable=false)
	private String givenName;
	@Column(nullable=false)
	private String familyName;
	@JoinColumn(nullable=false)
	private EmrSystem emrSystem;
	
	public EmrSystem getEmrSystem() {
		return emrSystem;
	}

	public void setEmrSystem(EmrSystem emrSystem) {
		this.emrSystem = emrSystem;
	}

	private static final long serialVersionUID = 1L;

	public Patient() {
		super();
	}

	public String getGivenName() {
		return givenName;
	}

	public void setGivenName(String givenName) {
		this.givenName = givenName;
	}

	public String getFamilyName() {
		return familyName;
	}

	public void setFamilyName(String familyName) {
		this.familyName = familyName;
	}

}
