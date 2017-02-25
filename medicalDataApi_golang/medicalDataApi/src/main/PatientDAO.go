package main

import (
	"fmt"
	"log"
	"database/sql"
	"strconv"
	"errors"
)

func GetPatientById(dbh sql.DB, patientId int) (Patient, error) {
	query := "select fName, lName, bDate, gender, emrSystemsListId from med_system_patient where patientId=" + strconv.Itoa(patientId)
	myPat := new(Patient)
	myPat.PatientId = strconv.Itoa(patientId)
	log.Println("About to call get patient query...")
	err := dbh.QueryRow(query).Scan(&myPat.Fname, &myPat.Lname, &myPat.Bdate, &myPat.Gender, &myPat.EmrPatientId)
	if err != nil {
		log.Println("Get patient query failed with error: " + err.Error())
		return *myPat, err
	}
	return *myPat, nil
}

// This must be an exact match of everything.  No soundex or other fuzzy matching
func GetPatientByName(dbh sql.DB, fName string, lName string, bDate string) (Patient, error) {
	query := "select patientId, fName, lName, contact, bDate. emrSystemsListId from med_system_patient where " +
		"fName='" + fName + "' and lName='" + lName + "' and bDate='" + bDate + "'"
	myPat := new(Patient)
	rows, err := DoSql(dbh, query, "Error trying to find patient")
	if err != nil {
		return *myPat, err
	}
	if rows != nil {
		for rows.Next() {
			err := rows.Scan(&myPat.PatientId, &myPat.Fname, &myPat.Lname, &myPat.Contact, &myPat.Bdate, &myPat.EmrPatientId)
			if err != nil {
				log.Println("get row failed with errror: " + err.Error())
				return *myPat, err
			}
		}
		rows.Close()
	}
	return *myPat, nil
}

// inserts/updates the EMR numbers
func UpdatePatientEMRdata(dbh sql.DB, patient Patient, emrSystem string) (error) {
	query := "select count(patientId) as N from med_system_emrSystemList where emrPatientId='" +
	patient.EmrPatientId + "' and  emrSystemName = '" +
	patient.EmrSystemName + "'"
	var  nPat int
	err := dbh.QueryRow(query).Scan(&nPat)
	if err != nil {
		log.Println("Unable to get count of patients with a given id")
		return err
	}
	if( nPat > 0 ) {
		query = "insert into med_system_emrSystemList (patientId, emrPatientId, emrSystemName) values (" +
		patient.PatientId + ", '" + patient.EmrPatientId + "', '" + patient.EmrSystemName + "')";
		err = DoExecSql(dbh, query, "Unable to save EMR id's" )
		if err != nil {
			return err
		}
	}
	return nil
}

// Returns the patient ID of the patient record that was either created or updated.
// assumes the emr system this data came from has already been added to the emrSystem table
func UpsertPatient(dbh sql.DB, patient Patient, emrSystem string) (int, error) {
	if len(emrSystem) > 1 {
		// find the id of the emr system
		var emrId int
		query := "select emrSystemId from med_system_emrSystem where emrSystemName='" + emrSystem + "'"
		err := dbh.QueryRow(query).Scan(&emrId)
		if err != nil {
			log.Print("unable to find emr system '" + emrSystem + "' with error: " + err.Error())
			return -1, err
		}
		// add patient.
		if len(patient.Bdate) < 1 {
			fmt.Println("Empty birth date field?")
			return -1, errors.New("Empty birth date field")
		}
		// 1st, find out if this patient is allready in the db.  match name + birthdata + gender
		var nPatients int
		whereClause := "where fName='" +
			patient.Fname + "' and lName='" + patient.Lname + "' and gender=$1" +
			" and bDate='" + patient.Bdate + "'"
		query = "select count(fName) as N from med_system_patient " + whereClause
		err = dbh.QueryRow(query, patient.Gender).Scan(&nPatients)
		if err == nil && nPatients == 0 {
			query = "insert into med_system_patient (fName, lName, bDate, gender, emrSystemsListId) " +
				"values ('" + patient.Fname + "', '" + patient.Lname + "', '" +				
				patient.Bdate + "', $1, " +
				strconv.Itoa(emrId) + ")"
			_, err = dbh.Exec(query, patient.Gender)
//			err = DoExecSql(dbh, query, "unable to insert patient")		
			if err != nil {
				return -1, err
			}
			err = UpdatePatientEMRdata(dbh, patient, emrSystem)
			if err != nil {
				return -1, err
			}
			lastInsertId, err := GetLastInserId(dbh)
			return lastInsertId, err
		}
		if err == nil && nPatients > 0 {
			query = "select patientId from med_system_patient " + whereClause
			var pId int
			err = dbh.QueryRow(query).Scan(&pId)
			if err != nil {
				log.Println("Unable to get patient id for existing patient: " + patient.Fname + " " + patient.Lname)
				return -1, err
			}
			err = UpdatePatientEMRdata(dbh, patient, emrSystem)
			if err != nil {
				return -1, err
			}
			return pId, err
		}
	}
	noEmrError := errors.New("No EMR system name provided")
	return -1, noEmrError
}
