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
	"GeomFromText('POINT(" + patLocReq.LatStr + " " +
	patLocReq.LongitudeStr + ")')) and floor='" + patLocReq.Floor + "'"
	err := dbh.QueryRow(query).Scan(&areaId)
	if err != nil {
		log.Println("Unable to get areaId for location: " + err.Error())
		log.Println("query: " + query)
		return *patLoc, err
	}
	query = "select patientId from med_system_area_use where areaId=" + areaId
	err = dbh.QueryRow(query).Scan(&patId)
	if err != nil {
		log.Println("Unable to get patient for area with error: " + err.Error())
		log.Println("query: " + query)
		return *patLoc, err
	}
	patLoc.AreaId = areaId
	patLoc.PatientId = patId
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