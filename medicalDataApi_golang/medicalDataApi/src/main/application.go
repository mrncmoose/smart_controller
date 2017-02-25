package main
// the kick off for the api
// Fred T. Dunaway
// August 25, 2016

import (
	"log"
    "net/http"
//    "database/sql"
)

const mysqlTimeFormat = "2006-01-02 15:04:05"
//var dbh *sql.DB		// our global database handler pointer.

func main() {

    router := NewRouter()

    log.Fatal(http.ListenAndServe(":8080", router))
}
