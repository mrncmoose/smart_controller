package main

import (
//	"fmt"
	"log"
	"database/sql"
//	"strconv"
)

type PatientLocation struct {
	AreaId	string `json:"areaId"`
	PatientId string `json:"patientId"`
}

type PatientLocationRequest struct {
	LatStr			string
	LongitudeStr	string
	Floor			string
	LocationErrorStr string
}

// first version of this will ignore the location error.
func GetPatientForLocation(dbh sql.DB, patLocReq PatientLocationRequest) (PatientLocation, error) {
	var areaId string
	var patId string
	patLoc := new(PatientLocation)
	query := "select areaId from med_system_area where contains(location, " +
	"GeomFromText('POINT(" + patLocReq.LongitudeStr + " " +
	patLocReq.LatStr + ")')) and floor='" + patLocReq.Floor + "' limit 1"
	err := dbh.QueryRow(query).Scan(&areaId)
//	rows, err := dbh.Query(query)
	if err != nil {
		log.Println("Unable to get areaId for location: " + err.Error())
		log.Println("query: " + query)
//		rows.Close()
		return *patLoc, err
	}
//	rows.Next()
//	err = rows.Scan(&areaId)
//	if err != nil {
//		log.Println("No area id?  Database error: " + err.Error())
//		rows.Close()
//		return *patLoc, err
//	}
	log.Println("Found area id of: " + areaId)
	query = "select patientId from med_system_area_use where areaId=" + areaId
	err = dbh.QueryRow(query).Scan(&patId)
//	rows2, err2 := dbh.Query(query)
	if err != nil {
		log.Println("Unable to get patient for area with error: " + err.Error())
		log.Println("query: " + query)
//		rows2.Close()
		return *patLoc, err
	}
//	rows2.Next()
//	err = rows2.Scan(&patId)
//	if err != nil {
//		log.Println("Unable to get patient id? Database error: " + err.Error())
//		rows.Close()
//		return *patLoc, err
//	}
	patLoc.AreaId = areaId
	patLoc.PatientId = patId
//	rows.Close()
//	rows2.Close()
	return *patLoc, nil	
}

// This function is now deprecated and will be removed shortly.  Use GetPatientForLocation()
func GetPatientForDeviceLocation(dbh sql.DB, deviceId string) (PatientLocation, error) {
	var areaId string
	var patId string
	patLoc := new(PatientLocation)
	query := "select areaId from med_system_fake_current_location where deviceId=" + deviceId
	err := dbh.QueryRow(query).Scan(&areaId)
	if err != nil {
		log.Println("Unable to get area id for device.")
		return *patLoc, err
	}	
	query = "select patientId from med_system_area_use where areaId=" + areaId
	err = dbh.QueryRow(query).Scan(&patId)
	if err != nil {
		log.Println("Unable to get patient for area.")
		return *patLoc, err
	}
	patLoc.AreaId = areaId
	patLoc.PatientId = patId
	return *patLoc, nil
}