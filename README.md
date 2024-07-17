# DIN & CIN Verification API

This API fetches Director Data with Director Identification Number (DIN) and also Corporate Information with its Identification Number (CIN).

## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [Endpoints](#EndPoints)
- [Support](#Support)
- [Contribution](#Contribution)

## Features
- Sends DIN or TIN based on what needs
- Return its details in a structured JSON format.
- Easy to integrate in any of your application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shubham-dube/DIN_and_CIN-Verification-API.git
   cd DIN_and_CIN-Verification-API
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate # On Linux use `source venv/bin/activate`
   
3. Install the dependencies:
   ```bash
   pip install flask requests bs4 html

4. Run the Application:
   ```bash
   python app.py
 *The API will be available at http://127.0.0.1:5000.*
 
## Usage
- Show the Input Field of what user needs (DIN data or CIN data) to the user.
- Send the entered Data to the given endpoint request body.
- You will get all the details related to that entered data in the JSON format.
  
## EndPoints

### Fetching CIN Details

**Endpoint:** `/api/v1/getCINdetails`

**Method:** `POST`

**Description:** `This Endpoint takes the CIN in a request body and returns the detail of that Company.`

**Request Body:**
```json
{
    "CIN": "U45201DL2002PTC114224"
}
```
**Response**
```json
{
    "CIN": "U45201DL2002PTC114224",
    "Roc": "",
    "capital": {
        "authorised": "100,000",
        "paidUp": " 100,000"
    },
    "companyName": "Rapti Construction And Projects Private Limited",
    "dates": {
        "incorporation": "14 February 2002",
        "lastAnnualGeneralMeet": "30 September 2013",
        "latestBalanceSheet": "31 March 2013"
    },
    "directors": [
        {
            "designation": "Director/Designated Partner",
            "name": "Manoj Kumar Sharma"
        },
        {
            "designation": "Director/Designated Partner",
            "name": "Kusum Sharma"
        },
        {
            "designation": "Director/Designated Partner",
            "name": "Lalita Sharma"
        },
        {
            "designation": "Director/Designated Partner",
            "name": "Ravi Shankar Sharma"
        }
    ],
    "listingStatus": "Unlisted",
    "pastDirectors": [],
    "registrationNumber": "114224",
    "state": "Delhi",
    "status": "Strike Off",
    "subCategory": "Non-govt company"
}
```
**Status Codes**
- 200 OK : `Details Recieved`


### Fetching DIN Details

**Endpoint:** `/api/v1/getDINdetails`

**Method:** `POST`

**Description:** `This Endpoint takes the DIN in a request body and returns the detail of that Director from a Govt. Website`

**Request Body:**
```json
{
    "DIN": "00591863"
}
```
**Response**
```json
{
    "DIN": "00591863",
    "companies": [
        {
            "CIN": "U45201DL2002PTC114224",
            "activeCompliance": "",
            "beginDate": "14/02/2002",
            "endDate": "-",
            "name": "RAPTI CONSTRUCTION AND PROJECTS PRIVATE LIMITED"
        },
        {
            "CIN": "U45201DL2005PTC139704",
            "activeCompliance": "",
            "beginDate": "16/08/2010",
            "endDate": "-",
            "name": "NCR PULSE REAL ESTATES (INDIA) PRIVATE LIMITED"
        },
        {
            "CIN": "U68200UP2023PTC192378",
            "activeCompliance": "ACTIVE compliant",
            "beginDate": "10/11/2023",
            "endDate": "-",
            "name": "VIDASTU DEVELOPERS PRIVATE LIMITED"
        }
    ],
    "llpList": [],
    "name": "RAVI SHANKAR SHARMA"
}
```
**Status Codes**
- 200 OK : `Details Recieved`

## Support
For Support Contact me at itzshubhamofficial@gmail.com
or Mobile Number : `+917687877772`

## Contribution

We welcome contributions to improve this project. Here are some ways you can contribute:

1. **Report Bugs:** If you find any bugs, please report them by opening an issue on GitHub.
2. **Feature Requests:** If you have ideas for new features, feel free to suggest them by opening an issue.
3. **Code Contributions:** 
    - Fork the repository.
    - Create a new branch (`git checkout -b feature-branch`).
    - Make your changes.
    - Commit your changes (`git commit -m 'Add some feature'`).
    - Push to the branch (`git push origin feature-branch`).
    - Open a pull request.

4. **Documentation:** Improve the documentation to help others understand and use the project.
5. **Testing:** Write tests to improve code coverage and ensure stability.

Please make sure your contributions adhere to our coding guidelines and standards.
