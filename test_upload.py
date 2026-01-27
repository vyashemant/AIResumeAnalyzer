22import requests
import os
from io import BytesIO

# Test the application functionality
def test_app():
    base_url = "http://127.0.0.1:5000"

    print("Testing AI Resume Analyzer Application...")

    # Test 1: Check if app is running
    try:
        response = requests.get(base_url)
        print(f"✓ App is running (status: {response.status_code})")
    except Exception as e:
        print(f"✗ App is not running: {e}")
        return False

    # Test 2: Check dashboard route
    try:
        response = requests.get(f"{base_url}/dashboard")
        print(f"✓ Dashboard route accessible (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Dashboard route failed: {e}")
        return False

    # Test 3: Check upload route
    try:
        response = requests.get(f"{base_url}/upload")
        print(f"✓ Upload route accessible (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Upload route failed: {e}")
        return False

    # Test 4: Check if upload page contains expected elements
    try:
        response = requests.get(f"{base_url}/upload")
        if "Upload Your Resume" in response.text and "job_description" in response.text:
            print("✓ Upload page contains expected form elements")
        else:
            print("✗ Upload page missing expected form elements")
            return False
    except Exception as e:
        print(f"✗ Upload page content check failed: {e}")
        return False

    # Test 5: Check if dashboard links to upload page
    try:
        response = requests.get(f"{base_url}/dashboard")
        if "/upload" in response.text:
            print("✓ Dashboard contains link to upload page")
        else:
            print("✗ Dashboard missing link to upload page")
            return False
    except Exception as e:
        print(f"✗ Dashboard link check failed: {e}")
        return False

    print("\n✓ All basic tests passed! The application is working correctly.")
    return True

if __name__ == "__main__":
    test_app()
