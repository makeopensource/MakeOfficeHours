package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

const (
	defaultServerURL = "http://localhost:8000"
)

// Response contains the UserID and ReaderCode that is being sent to the server
type Response struct {
	ID   string `json:"studentCode"`
	Code string `json:"readerId"`
}

func main() {
	// Initialize CLI arguments
	url := flag.String("url", defaultServerURL, "Remote Server URL")
	code := flag.String("code", "111111111", "Code for Office Hours location")
	flag.Parse()

	log.Println("Waiting for user input (card swipes)...")

	scanner := bufio.NewScanner(os.Stdin)

	// Read user input
	for scanner.Scan() {
		input := scanner.Text()
		if input == "quit" {
			return
		}

		log.Printf("Captured text: %s\n", input)

		// Handle POST in a goroutine
		go func(input string) {
			res := Response{
				ID:   input,
				Code: *code,
			}

			// Convert response struct to JSON
			resJSON := new(bytes.Buffer)
			err := json.NewEncoder(resJSON).Encode(res)
			if err != nil {
				log.Println("Error converting res struct to JSON:", err)
				return
			}

			log.Printf("Payload: %+v", res)

			// Send POST request
			resp, err := http.Post(*url, "application/json", resJSON)
			if err != nil {
				log.Println("HTTP Post error:", err)
				return
			}
			defer resp.Body.Close()

			// Read the response body
			responseBody, err := io.ReadAll(resp.Body)
			if err != nil {
				log.Println("Error reading response body:", err)
				return
			}

			// Log the server's response status and body
			log.Printf("Server Response Status: %d\n", resp.StatusCode)
			log.Printf("Server Response Body: %s\n", string(responseBody))

			if resp.StatusCode == http.StatusOK {
				log.Println("Data successfully sent to the server.")
			} else {
				log.Printf("Failed to send data, status code: %d\n", resp.StatusCode)
			}
		}(input)
	}

	// Check for errors in the scanner
	if err := scanner.Err(); err != nil {
		// PANIC! Error reading from Stdin
		panic(fmt.Sprintf("Error reading input from stdin: %v\n", err))
	}
}
