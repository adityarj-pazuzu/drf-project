import requests

# Replace these values with your actual endpoint URLs
BASE_URL = 'http://localhost:8000'
LOGIN_URL = BASE_URL + '/token/'
BLOGS_URL = BASE_URL + '/api/blogs/'

# Replace these values with your test user credentials
USERNAME = 'admin'
PASSWORD = 'admin'

# Function to authenticate and get JWT token
def get_token():
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }

    response = requests.post(LOGIN_URL, data=login_data)
    response_data = response.json()
    return response_data.get('access')

# Function to perform API requests with JWT token
def perform_request(url, method='GET', data=None):
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)

    return response

# Test cases

# Test Case 1: Get Blog List (Unauthenticated)
response = perform_request(BLOGS_URL)
print(f'Test Case 1 - Get Blog List (Unauthenticated): Status Code: {response.status_code}, Response: {response.json()}')

# Test Case 2: Authenticate and Get JWT Token
token = get_token()
print(f'Test Case 2 - Authenticate and Get JWT Token: Token: {token}')

# Test Case 3: Get Blog List (Authenticated)
response = perform_request(BLOGS_URL)
print(f'Test Case 3 - Get Blog List (Authenticated): Status Code: {response.status_code}, Response: {response.json()}')

# Test Case 4: Create Blog (Authenticated)
blog_data = {'title': 'New Test Blog', 'content': 'This is a new test blog content.'}
response = perform_request(BLOGS_URL, method='POST', data=blog_data)
print(f'Test Case 4 - Create Blog (Authenticated): Status Code: {response.status_code}, Response: {response.json()}')

# Test Case 5: Update Blog (Authenticated)
updated_blog_data = {'title': 'Updated Test Blog', 'content': 'This is an updated test blog content.'}
response = perform_request(BLOGS_URL + '1/', method='PUT', data=updated_blog_data)
print(f'Test Case 5 - Update Blog (Authenticated): Status Code: {response.status_code}, Response: {response.json()}')

# Test Case 6: Delete Blog (Authenticated)
response = perform_request(BLOGS_URL + '1/', method='DELETE')
print(f'Test Case 6 - Delete Blog (Authenticated): Status Code: {response.status_code}')

# Test Case 7: Search Blog by Title (Unauthenticated)
response = perform_request(BLOGS_URL + '?title=Test')
print(f'Test Case 7 - Search Blog by Title (Unauthenticated): Status Code: {response.status_code}, Response: {response.json()}')

# Test Case 8: Search Blog by Author (Unauthenticated)
response = perform_request(BLOGS_URL + '?author=1')
print(f'Test Case 8 - Search Blog by Author (Unauthenticated): Status Code: {response.status_code}, Response: {response.json()}')
