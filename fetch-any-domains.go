// The following code is heavily generated with help from Copilot
package main

import (
	"context"
	"encoding/csv"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/google/certificate-transparency-go/client"
	"github.com/google/certificate-transparency-go/jsonclient"
)

func main() {
	// Multiple CT log URLs
	logURLs := []string{
		"https://oak.ct.letsencrypt.org/2026h1/",
		"https://ct.googleapis.com/logs/us1/argon2026h1/",
		"https://ct.cloudflare.com/logs/nimbus2026/",
		"https://elephant2026h1.ct.sectigo.com/",
		"https://ct.googleapis.com/logs/eu1/xenon2026h1/",
		"https://tiger2026h1.ct.sectigo.com/",
		"https://wyvern.ct.digicert.com/2026h1/",
		"https://sphinx.ct.digicert.com/2026h1/",
	}

	// Prepare output file for intermittent saving
	outputFile := "found_any_domains.csv"
	file, err := os.OpenFile(outputFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		log.Fatalf("Failed to open file: %v", err)
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()

	seen := make(map[string]bool) // Track already saved domains
	var mu sync.Mutex             // Protect shared resources

	// Rate limiter: 1 request every 500ms (adjust as needed)
	rateLimit := time.NewTicker(500 * time.Millisecond)
	defer rateLimit.Stop()

	var wg sync.WaitGroup
	for _, logURL := range logURLs {
		wg.Add(1)
		go func(url string) {
			defer wg.Done()
			processLog(url, writer, seen, &mu, rateLimit)
		}(logURL)
	}

	wg.Wait()
	fmt.Println("All logs processed.")
}

func processLog(logURL string, writer *csv.Writer, seen map[string]bool, mu *sync.Mutex, rateLimit *time.Ticker) {
	fmt.Printf("Processing log: %s\n", logURL)

	cli, err := client.New(logURL, &http.Client{}, jsonclient.Options{})
	if err != nil {
		log.Printf("Failed to create client for %s: %v", logURL, err)
		return
	}

	sth, err := cli.GetSTH(context.Background())
	if err != nil {
		log.Printf("Failed to get STH for %s: %v", logURL, err)
		return
	}

	const batchSize int64 = 1000
	for start := int64(0); start < int64(sth.TreeSize); start += batchSize {
		end := start + batchSize - 1
		if end >= int64(sth.TreeSize) {
			end = int64(sth.TreeSize) - 1
		}

		// Wait for rate limiter before making request
		<-rateLimit.C

		entries, err := cli.GetEntries(context.Background(), start, end)
		if err != nil {
			log.Printf("Failed to get entries %d-%d: %v", start, end, err)
			continue
		}

		for _, entry := range entries {
			if entry.X509Cert != nil {
				for _, name := range entry.X509Cert.DNSNames {
					mu.Lock()
					if !seen[name] {
						fmt.Printf("Found domain: %s\n", name)
						seen[name] = true
						if err := writer.Write([]string{name}); err != nil {
							log.Printf("Failed to write domain %s: %v", name, err)
						}
						writer.Flush()
					}
					mu.Unlock()
				}
			}
		}
	}
}
