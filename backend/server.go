package main

import (
	"fmt"

	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"strconv"
)

type Restaurant struct {
	Name string `json:"name"`
	Kana string `json:"kana"`
	URL  string `json:"url"`
}

type Query struct {
	Station  string
	Genre    string
	Subgenre string
}

// DBConfig は DB 接続情報
type DBConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	SSLMode  string
}

var dbConfig DBConfig

func init() {
	err := godotenv.Load("../.env")

 
	if err != nil {
		fmt.Printf("読み込み出来ませんでした: %v", err)
	}
	port, err := strconv.Atoi(os.Getenv("DB_PORT"))
	if err != nil {
		log.Fatalf("invalid DB_PORT: %v", err)
	}
	dbConfig = DBConfig{
		Host:     os.Getenv("DB_HOST"),
		Port:     port,
		User:     os.Getenv("DB_USER"),
		Password: os.Getenv("DB_PASS"),
		DBName:   os.Getenv("DB_NAME"),
		SSLMode:  os.Getenv("DB_SSLMODE"),
	}
}

func main() {

	http.HandleFunc("/search", searchHandler)
	http.HandleFunc("/", rootHandler)

	fmt.Println("Server Start Up........")
	server := http.Server{
		Addr:    ":8080",
		Handler: nil,
	}
	log.Fatal(server.ListenAndServe())
}
