import subprocess
import sys
import os

def run_pipeline(make, model):
    print(f" STARTING PIPELINE FOR: {make} {model}")
    
    # 1. Run Scraper
    print("\n[1/2] Scraping data...")
    try:
        subprocess.run([sys.executable, "scrapper.py", make, model], check=True)
    except subprocess.CalledProcessError:
        print(" Scraping failed. Stopping pipeline.")
        return

    # 2. Run DB Populator
    # The scraper creates a file named "makemodel.csv" (e.g., daciasandero.csv)
    csv_filename = f"{make}{model}.csv"
    
    print(f"\n[2/2] Uploading {csv_filename} to Database...")
    try:
        subprocess.run([sys.executable, "populate_db.py", csv_filename], check=True)
    except subprocess.CalledProcessError:
        print(" Database upload failed.")
        return

    print("\n PIPELINE COMPLETE! Data is live.")

if __name__ == "__main__":
    # You can change these values or add input() to ask the user
    target_make = "dacia"
    target_model = "sandero"
    
    if len(sys.argv) > 2:
        target_make = sys.argv[1]
        target_model = sys.argv[2]

    run_pipeline(target_make, target_model)
