package main

import (
//	"fmt"
	"log"
	"database/sql"
	"strconv"
	"time"
)

func GetMedicationForPerson(dbh sql.DB, patId string ) (MedicationsType, error) {
	medType := new(MedicationsType)
	query := "select fName, lName from med_system_patient where patientId=" + patId
	var (lName string
		fName string
	)
	err := dbh.QueryRow(query).Scan(&fName, &lName)
	if err != nil {
		log.Println("Error getting patient name for medication: " + err.Error())
		log.Println("with query: " + query)
		return *medType, err
	}
	medType.PatientName = fName + " " + lName
	query = "select scriptId, issuedDate, expiredDate, medName from med_system_medications where patientId=" + patId +
		" order by medName"
	rows, errx := DoSql(dbh, query, "Error getting medications for patient" )
	if errx != nil {
		return *medType, err
	}
	var meds []Medication
	for rows.Next() {
		med := new(Medication)
		err = rows.Scan(&med.ScriptId, &med.IssuedDate, &med.ExpiredDate, &med.MedName)
		if err != nil {
			log.Println("error getting row: " + err.Error())
			return *medType, err
		}
		meds = append(meds, *med)
	}
	rows.Close()
	medType.Medications = meds
	return *medType, err	
}

func GetMedicationForDeviceId(dbh sql.DB, deviceId string) (MedicationsType, error) {
	medType := new(MedicationsType)
	query := "select areaId from med_system_fake_current_location where deviceId=" + deviceId
	var areaId int
	err := dbh.QueryRow(query).Scan(&areaId)
	if err != nil {
		log.Println("Error getting area id for device: " + err.Error())
		log.Println(query)
	}
	query = "select patientId from med_system_area_use where areaId=" + strconv.Itoa(areaId)
	var patId int
	err = dbh.QueryRow(query).Scan(&patId)
	if err != nil {
		log.Println("Error getting patient id for area: " + err.Error())
		log.Println(query)
	}
	*medType, err = GetMedicationForPerson(dbh, strconv.Itoa(patId))
	return *medType, err	
}

func SaveMedication(dbh sql.DB, med Medication, patId string) (int, error) {
	var nMeds int
	query := "select count(scriptId) as N from med_system_medications "
	// see if this med is an exact match for something allready loaded
	whereClause := "where patientId=" + patId + " and scriptId='" +
		med.ScriptId + "' and medName='" + med.MedName + "' and issuedDate='" +
		med.IssuedDate + "' and expiredDate='" + med.ExpiredDate + "'"
	err := dbh.QueryRow(query + whereClause).Scan(&nMeds)
	if err != nil {
		log.Println("Unable to check if med is currently loaded with error: " + err.Error())
		log.Println("query: " + query + whereClause)
		return -1, err
	}
	if nMeds == 0 {
		// deal with time values here
		var expireT string
		expire, err := time.Parse(time.RFC3339, med.ExpiredDate)
		if err == nil {
			expireT = expire.Format(mysqlTimeFormat)
		} else {
			log.Println("Bad time format for expire date: " + med.ExpiredDate)
			expireT = "null"
		}
		var issueT string
		issue, err := time.Parse(time.RFC3339, med.IssuedDate)
		if err == nil {
			issueT = issue.Format(mysqlTimeFormat)
		} else {
			log.Println("Bad time format for issue date: " + med.IssuedDate)
			issueT = "null"
		}
		insertQuery := "insert into med_system_medications (patientId, scriptId, issuedDate, expiredDate, medName) " +
			"values (" + patId+ ", '" + med.ScriptId + "', "
		if issueT == "null" {
			insertQuery += issueT + ", "
		} else {
			insertQuery += "'" + issueT + "', "
		}
		if expireT == "null" {
			insertQuery += expireT + ", "
		} else {
			insertQuery += "'" + expireT + "', "
		}
		insertQuery += "'" + med.MedName + "')"
		err = DoExecSql(dbh, insertQuery, "Unable to insert medication")
		if err != nil {
			return -1, err
		}
		lastInsertId, err := GetLastInserId(dbh)
		return lastInsertId, err
	}
	getIdQuery := "select id from med_system_medications " + whereClause
	var medId int
	err = dbh.QueryRow(getIdQuery).Scan(&medId)
	return medId, err
}
