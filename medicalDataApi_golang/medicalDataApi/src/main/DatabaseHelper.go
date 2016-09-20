package main
// a helper to deal wtih getting a database connection & submitting queries.
// Fred T. Dunaway
// August 25, 2016
import (
	"log"
	"fmt"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)
type DatabaseConnectionPrameters struct {
	databaseName string
	user string
	password string
	ipAddress string
	port string	
}

func NewDBH(dbConPram DatabaseConnectionPrameters) (*sql.DB, error) {
	connectStr := dbConPram.user + ":" + dbConPram.password + "@tcp(" + dbConPram.ipAddress + ":" + dbConPram.port + ")/" + dbConPram.databaseName
//	fmt.Println("opening with connection string: " + connectStr)
	dbh, err := sql.Open("mysql", connectStr)
	if err != nil {
		errStr := "Error connecting to mysql on: " + dbConPram.ipAddress + " with error: " + err.Error()
		fmt.Println(errStr)
		return nil, err
	}
	if(dbh != nil) {
		log.Print("database initialzed")
	}
	return dbh, nil
}

func DoSql(dbh sql.DB, query string) (*sql.Rows, error) {
//	fmt.Println("attempting query")
		rows, err := dbh.Query(query)
		if err != nil {
			log.Println("Error in query")
		}
//		fmt.Println("About to return from DoSql")
		return rows, err
}

func DoUpdateSql(dbh sql.DB, query string)  (error) {
	_, err := dbh.Exec(query)
	return err
}

func GetLastInserId(dbh sql.DB) (int, error) {
	var id = -1
	err := dbh.QueryRow("select LAST_INSERT_ID()").Scan(&id)
	return id, err
}
