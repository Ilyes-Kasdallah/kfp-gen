#!/usr/bin/env python3
"""
Script to run SonarQube analysis on Python/KFP files
"""
import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if required tools are installed"""
    try:
        subprocess.run(['sonar-scanner', '-v'], capture_output=True, check=True)
        print("✓ SonarScanner is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ SonarScanner not found. Please install it first.")
        return False
    
    if not Path('sonar-project.properties').exists():
        print("✗ sonar-project.properties not found")
        return False
    else:
        print("✓ sonar-project.properties found")
    
    return True

def run_pylint_analysis():
    """Run pylint analysis for additional insights"""
    print("Running pylint analysis...")
    try:
        # Find all Python files
        python_files = list(Path('/home/ilyes101/Documents/pfe-project/kfp-gen/generate-kfp/kube-linter/sec_gen/kfp_eval_samples_enhanced').rglob('*.py')) + list(Path('.').rglob('*.kfp'))
        
        if python_files:
            files_str = ' '.join(str(f) for f in python_files[:50])  # Limit to avoid command line length issues
            subprocess.run(f'pylint {files_str} > pylint-report.txt 2>&1', shell=True)
            print("✓ Pylint analysis completed")
        else:
            print("No Python files found")
    except Exception as e:
        print(f"Pylint analysis failed: {e}")

def run_sonar_analysis():
    """Run SonarQube analysis"""
    print("Starting SonarQube analysis...")
    try:
        result = subprocess.run(['sonar-scanner'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ SonarQube analysis completed successfully")
            print("Check results at: http://localhost:9000")
        else:
            print("✗ SonarQube analysis failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running SonarQube analysis: {e}")
        return False
    
    return True

def main():
    print("=== SonarQube Analysis for Python/KFP Files ===\n")
    
    if not check_prerequisites():
        sys.exit(1)
    
    # Optional: Run pylint for additional analysis
    run_pylint_analysis()
    
    # Run SonarQube analysis
    if run_sonar_analysis():
        print("\n=== Analysis Complete ===")
        print("View results at: http://localhost:9000")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()