package main

import (
  
    _ "github.com/lib/pq"
  
    "fmt"
    "html/template"
    "log"
    "net/http"
     
    "encoding/json"
     "database/sql"
    "math/rand/v2"
     
     
       
)


func queryRestaurants(p Query) (*Restaurant, error) {
    dsn := 
        fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
            dbConfig.Host, dbConfig.Port, dbConfig.User, dbConfig.Password, dbConfig.DBName, dbConfig.SSLMode,
        )
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }
    defer db.Close()

    // 動的 WHERE 組み立て
    args := []interface{}{p.Station}
    where := "WHERE station = $1"
    idx := 2
    if p.Genre != "" {
        where += fmt.Sprintf(" AND genre = $%d", idx)
        args = append(args, p.Genre)
        idx++
    }
    if p.Subgenre != "" {
        where += fmt.Sprintf(" AND subgenre = $%d", idx)
        args = append(args, p.Subgenre)
        idx++
    }

    query := fmt.Sprintf(`
        SELECT name, kana, url
          FROM restaurant
        %s
    `, where)

    rows, err := db.Query(query, args...)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var res []Restaurant
    for rows.Next() {
        var r Restaurant
        if err := rows.Scan(&r.Name, &r.Kana, &r.URL); err != nil {
            return nil, err
        }
        res = append(res, r)
    }
    if err := rows.Err(); err != nil {
        return nil, err
    }
     

    var ind = rand.N(len(res))
    return &res[ind], nil
}

 

 
func rootHandler(w http.ResponseWriter, r *http.Request) {
	html, err := template.ParseFiles("../frontend/index.html")
        if err != nil {
                log.Fatal(err)
        }
        if err := html.Execute(w, nil); err != nil {
                log.Fatal(err)
        }

         
}

func searchHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var params Query
    if err := json.NewDecoder(r.Body).Decode(&params); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }
    if params.Station == "" {
        http.Error(w, "Station is required", http.StatusBadRequest)
        return
    }

    results, err := queryRestaurants(params)
    if err != nil {
        log.Println("DB query error:", err)
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    if err := json.NewEncoder(w).Encode(results); err != nil {
        log.Println("JSON encode error:", err)
    }
}

 
// func DatabaseQuery(DB_USER string, DB_PASS string, station string , genre string , subgenre string){
//     dsn := fmt.Sprintf(
//         "host=localhost port=5432 user=%s password=%s dbname=app sslmode=disable",
//         DB_USER, DB_PASS,
//     )    
//     db, err := sql.Open("postgres", dsn)
//     if err != nil {
//         log.Fatal(err)
//     }
//     defer db.Close()

//     if err := db.Ping(); err != nil {
//         log.Fatal("DB ping error:", err)
//     }

//      // --- 動的に WHERE 句を組み立てる ---
//     args := []interface{}{station}      // 第1引数は必ず station
//     where := "WHERE station = $1"       // プレースホルダは $1 から始まる

//     idx := 2
//     if genre != "" {
//         where += fmt.Sprintf(" AND genre = $%d", idx)
//         args = append(args, genre)
//         idx++
//     }
//     if subgenre != "" {
//         where += fmt.Sprintf(" AND subgenre = $%d", idx)
//         args = append(args, subgenre)
//         idx++
//     }

//     query := fmt.Sprintf(`
//         SELECT name, kana, url
//           FROM restaurant
//         %s
//     `, where)

//     // --- 実行 ---
//     rows, err := db.Query(query, args...)
//     if err != nil {
//         log.Fatal("Query error:", err)
//     }
//     defer rows.Close()

//     for rows.Next() {
//         var name, kana, url  string
//         if err := rows.Scan(&name, &kana, &url); err != nil {
//             log.Fatal("Scan error:", err)
//         }
//         log.Println(name, kana, url)
//     }
//     if err := rows.Err(); err != nil {
//         log.Fatal("Rows iteration error:", err)
//     }
// }
// func DatabaseSummary(DB_USER string, DB_PASS string){
//     dsn := fmt.Sprintf(
//         "host=localhost port=5432 user=%s password=%s dbname=app sslmode=disable",
//         DB_USER, DB_PASS,
//     )    

//     db, err := sql.Open("postgres", dsn)
//     if err != nil {
//         log.Fatal(err)
//     }
//     defer db.Close()

//     if err := db.Ping(); err != nil {
//         log.Fatal("DB ping error:", err)
//     }

//     rows, err := db.Query("SELECT id, name FROM restaurant")
//     if err != nil {
//         log.Fatal(err)
//     }
//     defer rows.Close()

//     for rows.Next() {
//         var id, name string
//         if err := rows.Scan(&id, &name); err != nil {
//             log.Fatal("Scan error:", err)
//         }
//         log.Println(id, name)
//     }
//     if err := rows.Err(); err != nil {
//         log.Fatal("Rows iteration error:", err)
//     }
// }

// func main() {
//     user,pass,err:= loadEnv()
//     if err != nil {
// 		fmt.Printf("読み込み出来ませんでした: %v", err)
// 	} 
//     fmt.Printf(user,pass)
//     DatabaseSummary(user,pass)
//     DatabaseQuery(user,pass,"赤羽","は","")

// }
 