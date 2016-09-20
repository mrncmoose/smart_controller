package main


type Patient struct {
	PatientId	string	`json:"patientId"`	// our unquie internal patient ID
	Fname		string	`json:"fName"`
	Lname		string	`json:"lName"`
	Contact		int		`json:"contactId"`
	Bdate		string	`json:"bDate"`
	Gender		string	`json:"gender"`
	EmrSystemName	string `json:"emrSystemName"`
	EmrPatientId	string	`json:"emrPatientId"`	// the ID of this patientin the EMR system.
}

type PatientIdType struct {
	PatientId	string	`json:"patientId"`
}