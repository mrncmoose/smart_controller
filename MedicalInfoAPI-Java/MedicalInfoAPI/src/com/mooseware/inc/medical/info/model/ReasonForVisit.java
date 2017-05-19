package com.mooseware.inc.medical.info.model;

import java.io.Serializable;
import java.lang.String;
import javax.persistence.*;

/**
 * Entity implementation class for Entity: ReasonForVisit
 *
 */
@Entity

public class ReasonForVisit implements Serializable {

	   
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private int reasonForVisitId;
	private String reasonForVisit;
	private static final long serialVersionUID = 1L;

	public ReasonForVisit() {
		super();
	}   
	public int getReasonForVisitId() {
		return this.reasonForVisitId;
	}

	public void setReasonForVisitId(int reasonForVisitId) {
		this.reasonForVisitId = reasonForVisitId;
	}   
	public String getReasonForVisit() {
		return this.reasonForVisit;
	}

	public void setReasonForVisit(String reasonForVisit) {
		this.reasonForVisit = reasonForVisit;
	}
   
}
