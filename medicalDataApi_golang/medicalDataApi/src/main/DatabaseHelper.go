package main
// a helper to deal wtih getting a database connection & submitting queries.
// Fred T. Dunaway
// August 25, 2016
import (
	"log"
	"fmt"
	"time"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)
type DatabaseConnectionPrameters struct {
	DatabaseName string	`json:"databaseName"`
	User string			`json:"user"`
	Password string		`json:"password"`
	IpAddress string	`json:"ipAddress"`
	Port string			`json:"port"`
	MaxOpenConns int	`json:"maxOpenConns"`
	ConnMaxLifetime int64	`json:"connMaxLifetime"`
}

var dbh *sql.DB

func NewDBH(dbConPram DatabaseConnectionPrameters) (*sql.DB, error) {
	connectStr := dbConPram.User + ":" + dbConPram.Password + "@tcp(" + dbConPram.IpAddress + ":" + dbConPram.Port + ")/" + dbConPram.DatabaseName
//	fmt.Println("opening with connection string: " + connectStr)
	dbh, err := sql.Open("mysql", connectStr)
	if err != nil {
		errStr := "Error connecting to mysql on: " + dbConPram.IpAddress + " with error: " + err.Error()
		fmt.Println(errStr)
		return dbh, err
	}
	if(dbh != nil) {
		dbh.SetMaxOpenConns(dbConPram.MaxOpenConns)
		var conMaxLife time.Duration = time.Duration(dbConPram.ConnMaxLifetime) * time.Millisecond
		dbh.SetConnMaxLifetime(conMaxLife)
		log.Print("database initialzed")
	}
	return dbh, nil
}

func DoSql(dbh sql.DB, query string, errorMessage string) (*sql.Rows, error) {
//	fmt.Println("attempting query")
		rows, err := dbh.Query(query)
		if err != nil {
			log.Println(errorMessage)
			log.Println("Error in query: " + query)
			log.Println("error message: " + err.Error())
			rows.Close()
		}
//		fmt.Println("About to return from DoSql")
		return rows, err
}

func DoExecSql(dbh sql.DB, query string, errorMessage string)  (error) {
	_, err := dbh.Exec(query)
	if err != nil {
		log.Println(errorMessage)
		log.Println("Error in query:" + query)
		log.Println("error message: " + err.Error())
	}
	return err
}

func GetLastInserId(dbh sql.DB) (int, error) {
	var id = -1
	err := dbh.QueryRow("select LAST_INSERT_ID()").Scan(&id)
	return id, err
}
