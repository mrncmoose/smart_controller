package main

import (
//	"time"
)

type Allergy struct {
//	AddedDate 	time.Time	`json:"addedDate"`
	AddedDate	string	`json:"addedDate"`
	AllergyTo	string	`json:"allergyTo"`
	Severity 	string	`json:"severity"`
}

type AllergiesType struct {
	PatientName string `json:"patientName"`
	AllergiesTo	[]Allergy	`json:"allergies"`
}

type AllergyInputType struct {
	PatientFname	string	`json:"fName"`
	PatientLname	string	`json:"lName"`
	PatientId		string	`json:"patientId"`
	EmrName			string	`json:"emrName"`
	AllergiesTo	[]Allergy	`json:"allergies"`
}
