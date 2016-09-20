package main

import (

)

type Medication struct {
	ScriptId	string	`json:"scriptId"`
	IssuedDate	string	`json:"issuedDate"`
	ExpiredDate	string	`json:"expiredDate"`
	MedName		string	`json:"medName"`
	RecordDate	string	`json:"recordDate"`
}

type MedicationsType struct {
	PatientName	string `json:"patientName"`
	PatientId	string	`json:"patientId"`
	EmrName		string	`json:"emrName"`
	Medications	[]Medication	`json:"medications"`
}

type MedicationsCreated struct {
	MedicationId []string `json:"medicationId"`
}