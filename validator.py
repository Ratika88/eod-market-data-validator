import csv
import json
from datetime import datetime

def run_eod_validation():
    input_file = "market_data.csv"
    log_file = "critical_alerts.log"
    
    print(f"[{datetime.now()}] Starting Automated End-of-Day Data Integrity Scan...")
    
    flagged_incidents = []
    
    try:
        with open(input_file, mode='r') as file:
            reader = csv.DictReader(file)
            
            for line_no, row in enumerate(reader, start=2):
                ticker = row.get('Ticker', 'UNKNOWN')
                price_str = row.get('Price', '').strip()
                volume_str = row.get('Volume', '').strip()
                
                # Anomaly 1: Missing critical data field
                if not price_str or not volume_str:
                    flagged_incidents.append({
                        "Line": line_no, "Ticker": ticker, "Type": "DATA_MISSING",
                        "Details": f"Null value encountered in critical metrics field."
                    })
                    continue
                
                try:
                    price = float(price_str)
                    volume = int(volume_str)
                    
                    # Anomaly 2: Bad business logic boundaries (Negative Pricing)
                    if price <= 0:
                        flagged_incidents.append({
                            "Line": line_no, "Ticker": ticker, "Type": "NEGATIVE_PRICE_FAILURE",
                            "Details": f"Invalid trading boundary check. Value parsed: {price}"
                        })
                        
                    # Anomaly 3: Data Integrity check (Extreme Price spikes)
                    if ticker == "SHOP" and price > 500:
                        flagged_incidents.append({
                            "Line": line_no, "Ticker": ticker, "Type": "PRICE_VARIANCE_SPIKE",
                            "Details": f"Suspicious market variance detected. Price value: {price}"
                        })
                        
                except ValueError:
                    flagged_incidents.append({
                        "Line": line_no, "Ticker": ticker, "Type": "DATA_CORRUPTION",
                        "Details": f"Failed to parse numeric string format into floating points."
                    })

        # Process and write the alerts to an enterprise log file
        if flagged_incidents:
            with open(log_file, mode='w') as log:
                log.write(f"=== CRITICAL SLA SEVERITY-1 PRODUCTION ALERTS ({datetime.now()}) ===\n")
                for incident in flagged_incidents:
                    # Write traditional log text line
                    log.write(f"[{incident['Type']}] Line {incident['Line']} (Asset: {incident['Ticker']}): {incident['Details']}\n")
                    
                    # Also print a mock JSON payload that would feed a modern downstream API (like ServiceNow or Jira)
                    print(f"--> Mock JSON Payload Routed to ServiceNow: {json.dumps(incident)}")
            
            print(f"\n[{datetime.now()}] Scan complete. {len(flagged_incidents)} critical systemic risks written to '{log_file}'.")
        else:
            print(f"\n[{datetime.now()}] Scan complete. All records passed strict data validation schemas.")
            
    except FileNotFoundError:
        print(f"[FATAL_SEV1] Input feed '{input_file}' not found. Aborting processing loop.")

if __name__ == "__main__":
    run_eod_validation()
