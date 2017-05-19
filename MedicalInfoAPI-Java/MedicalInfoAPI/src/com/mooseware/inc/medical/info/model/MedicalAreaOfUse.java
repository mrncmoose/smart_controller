package com.mooseware.inc.medical.info.model;

import java.io.Serializable;
import javax.persistence.*;

/**
 * Entity implementation class for Entity: MedicalAreaOfUse
 *
 */
@Entity

public class MedicalAreaOfUse implements Serializable {
	private static final long serialVersionUID = 1L;
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int medicalAreaOfUseId;
	@JoinColumn(nullable=false)
	private Patient patient;
	@JoinColumn(nullable=false)
	private MedicalArea medArea;
	@JoinColumn(nullable=false)
	private ReasonForVisit reasonForVisit;
	
	public ReasonForVisit getReasonForVisit() {
		return reasonForVisit;
	}

	public void setReasonForVisit(ReasonForVisit reasonForVisit) {
		this.reasonForVisit = reasonForVisit;
	}

	public MedicalAreaOfUse() {
		super();
	}

	public int getMedicalAreaOfUseId() {
		return medicalAreaOfUseId;
	}

	public void setMedicalAreaOfUseId(int medicalAreaOfUseId) {
		this.medicalAreaOfUseId = medicalAreaOfUseId;
	}

	public Patient getPatient() {
		return patient;
	}

	public void setPatient(Patient patient) {
		this.patient = patient;
	}

	public MedicalArea getMedArea() {
		return medArea;
	}

	public void setMedArea(MedicalArea ma) {
		this.medArea = ma;
	}
   
}
