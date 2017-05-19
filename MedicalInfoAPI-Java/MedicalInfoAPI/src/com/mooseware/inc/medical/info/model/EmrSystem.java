package com.mooseware.inc.medical.info.model;

import java.io.Serializable;
import java.lang.String;
import javax.persistence.*;

import org.eclipse.persistence.annotations.ExistenceChecking;
import org.eclipse.persistence.annotations.ExistenceType;

/**
 * Entity implementation class for Entity: EmrSystem
 *
 */
@Entity
@ExistenceChecking(ExistenceType.CHECK_DATABASE)
public class EmrSystem implements Serializable {

	   
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int emrId;
	private String baseUrl;
	private String getPatientResource;
	private String putPatientResource;
	private String getPatientAllergyResource;
	private String putPatientAllergyResource;
	private String getPatientMedicationsResource;
	private String putPatientMedicationsResource;
	
	public String getPutPatientAllergyResource() {
		return putPatientAllergyResource;
	}
	public void setPutPatientAllergyResource(String putPatientAllergyResource) {
		this.putPatientAllergyResource = putPatientAllergyResource;
	}
	public String getGetPatientMedicationsResource() {
		return getPatientMedicationsResource;
	}
	public void setGetPatientMedicationsResource(String getPatientMedicationsResource) {
		this.getPatientMedicationsResource = getPatientMedicationsResource;
	}
	public String getPutPatientMedicationsResource() {
		return putPatientMedicationsResource;
	}
	public void setPutPatientMedicationsResource(String putPatientMedicationsResource) {
		this.putPatientMedicationsResource = putPatientMedicationsResource;
	}

	private String emrName;
	private static final long serialVersionUID = 1L;

	public EmrSystem() {
		super();
	}   
	public int getEmrId() {
		return this.emrId;
	}

	public void setEmrId(int emrId) {
		this.emrId = emrId;
	}   
	public String getBaseUrl() {
		return this.baseUrl;
	}

	public void setBaseUrl(String baseUrl) {
		this.baseUrl = baseUrl;
	}   
	public String getGetPatientResource() {
		return this.getPatientResource;
	}

	public void setGetPatientResource(String getPatientResource) {
		this.getPatientResource = getPatientResource;
	}   
	public String getPutPatientResource() {
		return this.putPatientResource;
	}

	public void setPutPatientResource(String putPatientResource) {
		this.putPatientResource = putPatientResource;
	}   
	public String getGetPatientAllergyResource() {
		return this.getPatientAllergyResource;
	}

	public void setGetPatientAllergyResource(String getPatientAllergyResource) {
		this.getPatientAllergyResource = getPatientAllergyResource;
	}   
	public String getEmrName() {
		return this.emrName;
	}

	public void setEmrName(String emrName) {
		this.emrName = emrName;
	}
   
}
