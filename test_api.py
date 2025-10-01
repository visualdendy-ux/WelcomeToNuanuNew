#!/usr/bin/env python3
"""
Test script for NUANU WiFi Login Portal API
Run this to verify all endpoints work correctly
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your Railway URL for production testing
TEST_EMAIL = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_result(success, message):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")

def test_home_page():
    """Test if home page loads"""
    print_header("Test 1: Home Page")
    try:
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200
        print_result(success, f"Home page status: {response.status_code}")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_admin_page():
    """Test if admin page loads"""
    print_header("Test 2: Admin Page")
    try:
        response = requests.get(f"{BASE_URL}/admin")
        success = response.status_code == 200
        print_result(success, f"Admin page status: {response.status_code}")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_save_user():
    """Test saving user data"""
    print_header("Test 3: Save User Data")
    try:
        data = {
            "email": TEST_EMAIL,
            "questions": "Test question from API test",
            "role": "Solopreneur"
        }
        response = requests.post(
            f"{BASE_URL}/api/save-user",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        success = response.status_code == 200 and result.get("success") == True
        print_result(success, f"Save user response: {json.dumps(result, indent=2)}")
        return success, result.get("data", {}).get("id")
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False, None

def test_get_users():
    """Test getting all users"""
    print_header("Test 4: Get All Users")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        result = response.json()
        success = response.status_code == 200 and result.get("success") == True
        count = result.get("count", 0)
        print_result(success, f"Retrieved {count} users")
        if success and count > 0:
            print(f"Sample user: {json.dumps(result['data'][0], indent=2)}")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_get_stats():
    """Test getting statistics"""
    print_header("Test 5: Get Statistics")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        result = response.json()
        success = response.status_code == 200 and result.get("success") == True
        if success:
            stats = result.get("stats", {})
            print_result(success, f"Statistics retrieved:")
            print(f"  - Total users: {stats.get('total', 0)}")
            print(f"  - Last 24 hours: {stats.get('last24hours', 0)}")
            print(f"  - Roles: {len(stats.get('byRole', []))}")
            for role_stat in stats.get('byRole', [])[:3]:
                print(f"    • {role_stat['role']}: {role_stat['count']}")
        else:
            print_result(success, f"Failed to get statistics")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_delete_user(user_id):
    """Test deleting a user"""
    print_header("Test 6: Delete User")
    if not user_id:
        print_result(False, "No user ID provided, skipping delete test")
        return False
    
    try:
        response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        result = response.json()
        success = response.status_code == 200 and result.get("success") == True
        print_result(success, f"Delete user response: {json.dumps(result, indent=2)}")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_database_connection():
    """Test database connection by checking if we can save and retrieve data"""
    print_header("Test 7: Database Connection")
    try:
        # Save a test user
        data = {
            "email": f"db-test-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "questions": "Database connection test",
            "role": "Student"
        }
        save_response = requests.post(
            f"{BASE_URL}/api/save-user",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        save_result = save_response.json()
        
        if not save_result.get("success"):
            print_result(False, "Failed to save test user")
            return False
        
        user_id = save_result.get("data", {}).get("id")
        
        # Retrieve users to verify
        get_response = requests.get(f"{BASE_URL}/api/users")
        get_result = get_response.json()
        
        if not get_result.get("success"):
            print_result(False, "Failed to retrieve users")
            return False
        
        # Check if our test user exists
        users = get_result.get("data", [])
        found = any(u.get("id") == user_id for u in users)
        
        # Clean up
        if user_id:
            requests.delete(f"{BASE_URL}/api/users/{user_id}")
        
        print_result(found, "Database connection and data persistence verified")
        return found
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 " + "="*58)
    print("  NUANU WiFi Login Portal - API Test Suite")
    print("="*60)
    print(f"Testing URL: {BASE_URL}")
    print(f"Test Email: {TEST_EMAIL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    user_id = None
    
    # Run tests
    results.append(("Home Page", test_home_page()))
    results.append(("Admin Page", test_admin_page()))
    
    save_success, user_id = test_save_user()
    results.append(("Save User", save_success))
    
    results.append(("Get Users", test_get_users()))
    results.append(("Get Statistics", test_get_stats()))
    results.append(("Delete User", test_delete_user(user_id)))
    results.append(("Database Connection", test_database_connection()))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        exit(1)
