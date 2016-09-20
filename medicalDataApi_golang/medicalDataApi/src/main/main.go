package main
// the kick off for the api
// Fred T. Dunaway
// August 25, 2016

import (
	"log"
    "net/http"
)

const mysqlTimeFormat = "2006-01-02 15:04:05"

func main() {

    router := NewRouter()

    log.Fatal(http.ListenAndServe(":8080", router))
}
