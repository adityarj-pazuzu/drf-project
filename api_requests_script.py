"""Simple script to test the API functions"""
import requests

# Replace these values with your actual endpoint URLs
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = "http://localhost:8000/token/"
BLOGS_URL = BASE_URL + "/blogs/"  # Updated endpoint
BLOGS_BY_DATE_URL = BASE_URL + "/blogs/by_date/"
BLOGS_BY_DATE_RANGE_URL = BASE_URL + "/blogs/by_date_range/"
BLOGS_CREATED_AFTER_DATE_URL = BASE_URL + "/blogs/created_after_date/"
BLOGS_CREATED_BEFORE_DATE_URL = BASE_URL + "/blogs/created_before_date/"

# Replace these values with your test user credentials
USERNAME = "admin"
PASSWORD = "admin"


def get_token():
    """
    # Function to authenticate and get JWT token
    """
    login_data = {"username": USERNAME, "password": PASSWORD}

    res = requests.post(LOGIN_URL, data=login_data, timeout=15)
    response_data = res.json()
    return response_data.get("access")


def perform_request(url, method="GET", data=None):
    """
    Function to perform API requests with JWT token
    """
    res = None
    headers = {"Authorization": f"Bearer {get_token()}"}

    if method == "GET":
        res = requests.get(url, headers=headers, timeout=30)
    elif method == "POST":
        res = requests.post(url, headers=headers, json=data, timeout=30)
    elif method == "PUT":
        res = requests.put(url, headers=headers, json=data, timeout=30)
    elif method == "DELETE":
        res = requests.delete(url, headers=headers, timeout=30)

    return res


# Test cases

# Test Case 1: Get Blog List (Unauthenticated)
response = perform_request(BLOGS_URL)
print(
    f"Test Case 1 - Get Blog List (Unauthenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 2: Authenticate and Get JWT Token
token = get_token()
print(f"Test Case 2 - Authenticate and Get JWT Token: Token: {token}")

# Test Case 3: Get Blog List (Authenticated)
response = perform_request(BLOGS_URL)
print(
    f"Test Case 3 - Get Blog List (Authenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 4: Create Blog (Authenticated)
blog_data = {"title": "New Test Blog", "content": "This is a new test blog content."}
response = perform_request(BLOGS_URL, method="POST", data=blog_data)
print(
    f"Test Case 4 - Create Blog (Authenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 5: Update Blog (Authenticated)
ID_TO_UPDATE = str(response.json()["id"])
updated_blog_data = {
    "title": "Updated Test Blog",
    "content": "This is an updated test blog content.",
}
response = perform_request(
    BLOGS_URL + ID_TO_UPDATE + "/", method="PUT", data=updated_blog_data
)
print(
    f"Test Case 5 - Update Blog (Authenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 6: Delete Blog (Authenticated)
response = perform_request(BLOGS_URL + ID_TO_UPDATE + "/", method="DELETE")
print(f"Test Case 6 - Delete Blog (Authenticated): Status Code: {response.status_code}")

# Test Case 7: Search Blog by Title (Unauthenticated)
response = perform_request(BLOGS_URL + "?title=Test")
print(
    f"Test Case 7 - Search Blog by Title (Unauthenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 8: Search Blog by Author (Unauthenticated)
response = perform_request(BLOGS_URL + "?author=1")
print(
    f"Test Case 8 - Search Blog by Author (Unauthenticated): Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 9: Get Blogs by Date
response = perform_request(BLOGS_BY_DATE_URL + "?date=2024-02-05")
print(
    f"Test Case 9 - Get Blogs by Date: Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 10: Get Blogs by Date Range
response = perform_request(
    BLOGS_BY_DATE_RANGE_URL + "?start_date=2024-02-01&end_date=2024-02-05"
)
print(
    f"Test Case 10 - Get Blogs by Date Range: Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 11: Get Blogs Created After Date
response = perform_request(BLOGS_CREATED_AFTER_DATE_URL + "?date=2024-02-01")
print(
    f"Test Case 11 - Get Blogs Created After Date: Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)

# Test Case 12: Get Blogs Created Before Date
response = perform_request(BLOGS_CREATED_BEFORE_DATE_URL + "?date=2024-02-06")
print(
    f"Test Case 12 - Get Blogs Created Before Date: Status Code: {response.status_code}, "
    f"Response: {response.json()}"
)
