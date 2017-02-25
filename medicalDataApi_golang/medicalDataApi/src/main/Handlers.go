package main

import (
   "encoding/json"
    "fmt"
    "net/http"
    "io/ioutil"
    "io"
	"log"
    "github.com/gorilla/mux"
//    "database/sql"
	"strconv"
	"os"
)

const maxReadBytes = 1048576
const internalServerError = 500

func init() {
	file, configFileErr := os.Open("dbconfig.json")
	if configFileErr != nil {
		log.Panicln("Can not open dbconfig.json config file.")
	}
	decoder := json.NewDecoder(file)
	mydbp := DatabaseConnectionPrameters{}
	err := decoder.Decode(&mydbp)
	if err != nil {
		log.Println("error reading config: " + err.Error())
		log.Panicln("Unable to read database configuration file (dbconfig.json)")
	}
	log.Println("getting new database handler")
	dbh, err = NewDBH(mydbp)	//database hanlder, dbh, declared in DatabaseHelper as global
	if err != nil {
		log.Fatal("oops.... Database handler didn't initialize")
	}
}

func Index(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Welcome!")
}

func AllergiesCreate(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
//    vars := mux.Vars(r)
    w.WriteHeader(http.StatusOK)
	//log.Printf("Vars on post: %v\n", vars)
    var allergy AllergyInputType
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
        panic(err)
    }
    if err := json.Unmarshal(body, &allergy); err != nil {
        w.Header().Set("Content-Type", "application/json; charset=UTF-8")
        w.WriteHeader(422) // unprocessable entity
        if err := json.NewEncoder(w).Encode(err); err != nil {
            panic(err)
        }
    }
    fmt.Printf("Allergy to write out: %v\n", allergy)
	nfgErr := AddAllergiesForPatient(*dbh, allergy)
	if(nfgErr != nil) {
		log.Print(nfgErr)
		w.WriteHeader(422)
        if err := json.NewEncoder(w).Encode(err); err != nil {
            panic(err)
        }		
	}

    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    w.WriteHeader(http.StatusCreated)
}

func AllergiesRead(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    vars := mux.Vars(r)
    fmt.Printf("vars: %v", vars)
    patientId := vars["patient_id"]
    deviceId := vars["device_id"]
    if len(deviceId) != 0 {
    	allergies, err := GetAllergiesForDeviceId(*dbh, deviceId)
    	if err != nil {
    		w.WriteHeader(http.StatusNotFound)
    		log.Println(err)
    	} else {
    		if err := json.NewEncoder(w).Encode(allergies); err != nil {
				panic(err)
		    }
    	}
    } else if len(patientId) != 0 {
    	myPatId, err := strconv.Atoi(patientId)
    	allergies, err := GetAllergiesForPatient(*dbh, myPatId)
    	if err != nil {
    		w.WriteHeader(http.StatusNotFound)
    		log.Println(err)    		
    	} else {
    		if err := json.NewEncoder(w).Encode(allergies); err != nil {
    			panic(err)
    		}
    	}
    }
}

func GetPatient(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    vars := mux.Vars(r)
    patientId, _ := strconv.Atoi(vars["patient_id"])
    log.Println("About to call get patient by id...")
	pat, err := GetPatientById(*dbh, patientId)
	if err != nil {
    	w.WriteHeader(http.StatusNotFound)
    	log.Println(err)
	} else {
	if err := json.NewEncoder(w).Encode(pat); err != nil {
			panic(err)
	    }
	}		
}

func CreatePatient(w http.ResponseWriter, r *http.Request) {
	var pat Patient
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
//    vars := mux.Vars(r)
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
        panic(err)
    }
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    if err := json.Unmarshal(body, &pat); err != nil {
        w.WriteHeader(422) // unprocessable entity
	   if err := json.NewEncoder(w).Encode(err); err != nil {
	        panic(err)
	    }
    }
    if len(pat.EmrSystemName) > 1 {
		patId, err := UpsertPatient(*dbh, pat, pat.EmrSystemName)
		retPat := new(PatientIdType)
		retPat.PatientId = strconv.Itoa(patId);
		if err != nil {
			w.WriteHeader(internalServerError) // internal server error
			log.Println("Error creating patient: " + err.Error())
		} else {
		    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		    w.WriteHeader(http.StatusCreated)
    		if err := json.NewEncoder(w).Encode(retPat); err != nil {
    			panic(err)
    		}
		}
    }    	
}

func GetMedication(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    vars := mux.Vars(r)
//    fmt.Printf("Get medicaitons vars: %v\n", vars)
	patientId := vars["patient_id"]
	deviceId := vars["device_id"]
	if len(patientId) > 0 {
		myMeds, err := GetMedicationForPerson(*dbh, patientId)
		if err != nil {
			w.WriteHeader(internalServerError) // internal server error
			log.Println("Error getting medications for patient id: " + patientId)
		}
		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(myMeds); err != nil {
			panic(err)
		}
	}
	if len(deviceId) > 0 {
		myMeds, err := GetMedicationForDeviceId(*dbh, deviceId)
		if err != nil {
			w.WriteHeader(internalServerError) // internal server error
			log.Println("Error getting medications for device id: " + deviceId)
		}
		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(myMeds); err != nil {
			panic(err)
		}
	}
}

func CreateMedication(w http.ResponseWriter, r *http.Request) {
	var meds MedicationsType
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
    	log.Println("Error reading medication JSON: " + err.Error())
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
    	log.Println("Error closing request: " + err.Error())
        panic(err)
    }
    if err := json.Unmarshal(body, &meds); err != nil {
        w.WriteHeader(422) // unprocessable entity
	   if err := json.NewEncoder(w).Encode(err); err != nil {
	        panic(err)
	    }
    }
    medList := meds.Medications
    patId := meds.PatientId
    var medIdList = new(MedicationsCreated)
    var loopErr error
    for _, theMed := range medList {
	 	medId, loopErr := SaveMedication(*dbh, theMed, patId)   	
		if loopErr != nil {
			w.WriteHeader(internalServerError) // internal server error
			log.Println("Error creating medications: " + err.Error())
			break	
		} else {
			medIdList.MedicationId = append(medIdList.MedicationId, strconv.Itoa(medId))
		}
    }
    if loopErr == nil {
		w.WriteHeader(http.StatusCreated)
		if err := json.NewEncoder(w).Encode(medIdList); err != nil {
			panic(err)
		}
    }
}

func LocationManager(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    vars := mux.Vars(r)
	var deviceId = vars["device_id"]
	if len(deviceId) > 0 {
		patLoc, err := GetPatientForDeviceLocation(*dbh, deviceId)
		if err != nil {
			 w.WriteHeader(internalServerError)
			 log.Println("Error getting patient for location: " + err.Error())
		} else {
			w.WriteHeader(http.StatusOK)
			if err := json.NewEncoder(w).Encode(patLoc); err != nil{
				panic(err)
			}
		}
	}
}
	
func PatientLocationManager(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	vars := mux.Vars(r)
	var patLocReq = new(PatientLocationRequest)
	patLocReq.Floor = vars["floor"]
	patLocReq.LatStr = vars["lat"]
	patLocReq.LongitudeStr = vars["long"]
	patLocReq.LocationErrorStr = vars["locErr"]
	patLoc, err := GetPatientForLocation(*dbh, *patLocReq)
	if err != nil {
		w.WriteHeader(internalServerError)
	} else {
		w.WriteHeader(http.StatusOK)
	    if err := json.NewEncoder(w).Encode(patLoc); err != nil {
	    	panic(err)
	    }
	}
}

func CreateCarePlan (w http.ResponseWriter, r *http.Request) {
	var meds MedicationsType
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
    	log.Println("Error reading Care Plan JSON: " + err.Error())
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
    	log.Println("Error closing request: " + err.Error())
        panic(err)
    }
    if err := json.Unmarshal(body, &meds); err != nil {
        w.WriteHeader(422) // unprocessable entity
	   if err := json.NewEncoder(w).Encode(err); err != nil {
	        panic(err)
	    }
    }
    // magic to save care plan here
}
// Nov 13, 2016
// This function needs to be deprecated soon.  The IPS is functioning and this no longer has value
func NextPatient(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	vars := mux.Vars(r)
	dwq, err := GetNextPatient(*dbh, vars["patientId"])
	if err != nil {
		w.WriteHeader(internalServerError)
	} else {
		w.WriteHeader(http.StatusOK)
	    if err := json.NewEncoder(w).Encode(dwq); err != nil {
	    	panic(err)
	    }	
	}
}

func HandleAddPatientToQueue(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	var patQueReq = new(PatientQueueRequest)
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
    	log.Println("Error reading AddPatiantToQue JSON: " + err.Error())
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
    	log.Println("Error closing request: " + err.Error())
        panic(err)
    }
    if err := json.Unmarshal(body, &patQueReq); err != nil {
        w.WriteHeader(422) // unprocessable entity
	   if err := json.NewEncoder(w).Encode(err); err != nil {
	        panic(err)
	    }
    } else {
		err = AddPatientToQueue(*dbh, *patQueReq)
		if(err != nil) {
			w.WriteHeader(internalServerError)
		}
    }
}

func HandleCreateObservation(w http.ResponseWriter, r *http.Request) {
	var obs ObservationType
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
    body, err := ioutil.ReadAll(io.LimitReader(r.Body, maxReadBytes))
    if err != nil {
    	log.Println("Error reading observation JSON: " + err.Error())
        panic(err)
    }
    if err := r.Body.Close(); err != nil {
    	log.Println("Error closing request: " + err.Error())
        panic(err)
    }
    if err := json.Unmarshal(body, &obs); err != nil {
        w.WriteHeader(422) // unprocessable entity
	   if err := json.NewEncoder(w).Encode(err); err != nil {
	        panic(err)
	    }
    }
    err = AddObservation(*dbh, obs)
    
    if err != nil {
		w.WriteHeader(internalServerError)
    } else {
    	w.WriteHeader(http.StatusCreated)
    }
}

func GetObservations(w http.ResponseWriter, r *http.Request) {
//	var obs ObservationDisplay
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	vars := mux.Vars(r)
	patientId, err := strconv.Atoi(vars["patient_id"])
	if err!=nil {
		log.Println("Unparseable patient ID.  All patient ID's are integers")
		panic(err)
	}
	obs, err := GetObservationsForPatientId(*dbh, patientId)
		if err != nil {
		w.WriteHeader(internalServerError)
	} else {
		w.WriteHeader(http.StatusOK)
	    if err := json.NewEncoder(w).Encode(obs); err != nil {
	    	panic(err)
	    }	
	}

}