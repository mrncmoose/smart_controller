package main
// handles accessing allergy data
// Fred T. Dunaway
// August 25, 2016

import (
//	"fmt"
	"log"
	"database/sql"
	"strconv"
	"time"
)

func AddAllergiesForPatient(dbh sql.DB, allergy AllergyInputType) (error) {
	patentId := allergy.PatientId
	emrName := allergy.EmrName
	allergies := allergy.AllergiesTo
	for _, al := range allergies {
		// transform the date to something mysql can use
		var addedTo string
		addedToDate, err := time.Parse(time.RFC3339, al.AddedDate)
		if err == nil {
			addedTo = addedToDate.Format(mysqlTimeFormat)
		} else {
			log.Println("Bad time format for expire date: " + al.AddedDate)
		}
		// is this allready in the db?
		var allId int
		whereClause := " where patientId=" + allergy.PatientId + " and allergyTo='" + al.AllergyTo + "'"
		query := "select allergy_id as N from med_system_allergies" + whereClause
		err = dbh.QueryRow(query).Scan(&allId)
		switch {
			case err == sql.ErrNoRows || err == nil:
				query = "replace into med_system_allergies (allergy_id, patientId, addedDate, allergyTo, severity, emrId) " + 
					"values(" + strconv.Itoa(allId) + ", " + patentId + " ,'" + addedTo + 
					"', '" + al.AllergyTo + "', '" + al.Severity + "', '" + emrName + "')";
				err = DoExecSql(dbh, query, "Error getting allergy Id: ")
				if err != nil {
					return err
				}
			case err != nil:
				log.Println("Error getting allergy Id: " + err.Error())
				log.Println(query)
				return err
		}
	}	
	return nil
}

func GetAllergiesForDeviceId(dbh sql.DB, deviceId string) (AllergiesType, error) {
	log.Println("Attempting to get allergies for device")
	at := new(AllergiesType)
	sql := "select areaId from med_system_fake_current_location where deviceId=" + deviceId
		var (
		areaId int
		patientId int
	)
	rows, err := DoSql(dbh, sql, "Failed to find allergy")
	if err != nil {
		return *at, err
	}
	if rows != nil {
		for rows.Next() {
			err := rows.Scan(&areaId)
			if err != nil {
				log.Println("get row failed with errror: " + err.Error())
				return *at, err
			}
		}
		rows.Close()
	}
	sql = "select patientId from med_system_area_use where areaId=" + strconv.Itoa(areaId)
	
	rows2, err2 := DoSql(dbh, sql, "Unable to get patient id for the areaId provided")
	if err2 != nil {
		return *at, err2
	}
	if rows != nil {
		defer rows.Close()
		for rows2.Next() {
			err := rows2.Scan(&patientId)
			if err != nil {
				log.Println("get row failed with errror: " + err.Error())
				return *at, err
			}
		}
		return GetAllergiesForPatient(dbh, patientId)
	}
	return *at,nil
	
}

func GetAllergiesForPatient(dbh sql.DB, patientId int) (AllergiesType, error) {
//	log.Println("Attempting to get allergies for patientId " + strconv.Itoa(patientId))
	query := "select fName, lName from med_system_patient where patientId=" + strconv.Itoa(patientId)
	var (
		fName string
		lName string
		allergyType	AllergiesType
	)
	err := dbh.QueryRow(query).Scan(&fName, &lName)
	if err != nil {
		log.Println("Query failed: " + query)
		return allergyType, err
	}
	allergyType.PatientName = fName + " " + lName
	log.Println("Found patient: " + allergyType.PatientName)
	sql2 := "select addedDate, allergyTo, severity from med_system_allergies where patientId=" + strconv.Itoa(patientId)
	alRows, err := DoSql(dbh, sql2, "Unable to get addedDate for patientId")
	if err != nil {
		return allergyType, err
	}
	if alRows != nil {
		defer alRows.Close()
		for alRows.Next() {
			allergy := new(Allergy)
			err := alRows.Scan(&allergy.AddedDate, &allergy.AllergyTo, &allergy.Severity)
			if err != nil {
				log.Println("get row failed with error: " + err.Error())
				return allergyType, err
			}
//			log.Println("adding allergy")
			allergyType.AllergiesTo = append(allergyType.AllergiesTo, *allergy)
		}
		return allergyType, nil
	}
	return allergyType, err	
}