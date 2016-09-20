package main

import (
	"net/http"
//	"database/sql"
)

type Route struct {
    Name        string
    Method      string
    Pattern     string
    HandlerFunc http.HandlerFunc
}

type Routes []Route

var routes = Routes{
    Route{
        "Index",
        "GET",
        "/",
        Index,
    },
    Route{
    	"AllergiesCreate",
    	"POST",
    	"/Allergies",
    	AllergiesCreate,
    },
    Route{
    	"AllergiesRead",
    	"GET",
    	"/Allergies/device_id/{device_id:[0-9]+}",
    	AllergiesRead,
    },
    Route{
     	"AllergiesRead",
    	"GET",
    	"/Allergies/patient_id/{patient_id:[0-9]+}",
    	AllergiesRead,
    },
    Route{
    	"CreatePatient",
    	"POST",
    	"/Patient",
    	CreatePatient,
    },
    Route{
    	"GetPatient",
    	"GET",
    	"/Patient/patient_id/{patient_id:[0-9]+}",
    	GetPatient,
    },
    Route{
    	"GetMedication",
    	"GET",
    	"/Medications/patient_id/{patient_id:[0-9]+}",
    	GetMedication,
    },
    Route{
    	"GetMedication",
    	"GET",
    	"/Medications/device_id/{device_id:[0-9]+}",
    	GetMedication,
    },
    Route{
    	"CreateMedication",
    	"POST",
    	"/Medications",
    	CreateMedication,
    },
    Route{
    	"LocationManager",
    	"GET",
    	"/LocationManager/device_id/{device_id:[0-9]+}",
    	LocationManager,
    },
    Route{
    	"PatientLocationManager",
    	"GET",
    	"/LocationManager/Patient/latitude/{lat}/longitude/{long}/floor/{floor}/LocationError/{locErr}",
    	PatientLocationManager,
    },
}