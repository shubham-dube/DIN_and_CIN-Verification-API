from flask import Flask, jsonify, Response, make_response, request
import requests
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

@app.route("/api/v1/getCINdetails", methods=["POST"])
def getCINdetails():
    try:
        query = request.json.get("CIN")
        session = requests.Session()

        if(query==''):
            return jsonify({"error": "query cannot be empty"})

        params = {"q": query}

        response = session.get(
            "https://www.quickcompany.in/company/search/",
            params=params
        )

        htmlString = response.text
        cleaned_html_string = htmlString.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '')
        cleaned_html_string = html.unescape(cleaned_html_string)

        soup = BeautifulSoup(cleaned_html_string, 'html.parser')

        listDiv = soup.find('div', id="list_results")

        companyName = listDiv.find('h4').get_text()
        if "No Companies Found" in companyName:
            return jsonify({"error": companyName.replace('\"', '')})
        
        companyLink = listDiv.find('h4').find('a').get('href')

        try:
            buttons = listDiv.find_all('button')
            status = buttons[0].get_text()
            state = buttons[1].get_text()
        except Exception as e:
            if not status:
                status = ""
            if not state:
                state = ""

        response2 = session.get(f"https://www.quickcompany.in{companyLink}")
        
        htmlString = response2.text
        cleaned_html_string = htmlString.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '')
        cleaned_html_string = html.unescape(cleaned_html_string)

        soup = BeautifulSoup(cleaned_html_string, 'html.parser')

        directorsDiv = soup.find('div', id="directors")
        
        directorNamesHeading = directorsDiv.find_all('h5')
        designationSpan = directorsDiv.find_all('span')
        directors = []
        for i in range(len(directorNamesHeading)):
            directors.append(
                {
                    "name": directorNamesHeading[i].get_text(),
                    "designation": designationSpan[i].get_text()
                }
            )
        
        informationDiv = soup.find('div', id="information")
        tableRows = informationDiv.find_all('tr')

        data = {}

        for row in tableRows:
            key = row.find_all('td')[0].get_text()
            value = row.find_all('td')[1].get_text()
            data[key] = value
        
        CIN = data.get('CIN', '')
        RegNo = data.get('Registration Number', '')
        dateOfIncorporation = data.get('Date of Incorporation', '')
        RoC = data.get('RoC', '')
        companySubcategory = data.get('Company Sub-Category', '')
        listingStatus = data.get('Listing status', '')
        authorisedCapital = data.get('Authorised Capital', '')
        paidUpCapital = data.get('Paid Up Capital', '')
        dateOfLastAnnualGenMeet = data.get('Date of Last Annual General Meeting', '')
        dateOfLatestBalanceSheet = data.get('Date of Latest Balance Sheet', '')

        pastDirectorsDiv = soup.find('h4', id="past_directors").find_next_sibling('div')

        PdirectorNamesHeading = pastDirectorsDiv.find_all('h5')
        PdesignationSpan = pastDirectorsDiv.find_all('span')
        pastDirectors = []
        for i in range(len(PdirectorNamesHeading)):
            pastDirectors.append(
                {
                    "name": PdirectorNamesHeading[i].get_text(),
                    "designation": PdesignationSpan[i].get_text()
                }
            )

        CINdetail = {
            "companyName": companyName,
            "CIN": CIN,
            "status": status,
            "listingStatus": listingStatus,
            "state": state,
            "registrationNumber": RegNo,
            "Roc": RoC,
            "subCategory": companySubcategory,
            "capital": {
                "authorised": authorisedCapital,
                "paidUp": paidUpCapital
            },
            "dates": {
                "incorporation":dateOfIncorporation,
                "lastAnnualGeneralMeet": dateOfLastAnnualGenMeet,
                "latestBalanceSheet": dateOfLatestBalanceSheet
            },
            "directors": directors,
            "pastDirectors": pastDirectors
        }

        return jsonify(CINdetail)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching CIN Details"})

@app.route("/api/v1/getDINdetails", methods=["POST"])
def getDINdetails():
    try:
        DIN = request.json.get("DIN")
        session = requests.Session()

        postData = {
            "directorName": "",
            "din": DIN,
            "displayCaptcha": ""
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        response = session.post(
            "https://www.mca.gov.in/mcafoportal/showdirectorMasterData.do", data=postData, headers=headers
        )

        htmlString = response.text
        cleaned_html_string = htmlString.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '')
        cleaned_html_string = html.unescape(cleaned_html_string)

        soup = BeautifulSoup(cleaned_html_string, 'html.parser')
        masterDiv = soup.find('div', id = 'dirMasterData')
        directorDataTable = masterDiv.find('table', id="directorData")

        din = directorDataTable.find_all('tr')[0].find_all('td')[1].get_text()
        name = directorDataTable.find_all('tr')[1].find_all('td')[1].get_text()

        companyDataTable = masterDiv.find('table', id="companyData")
        companies = []
        tableRows = companyDataTable.find_all('tr')
        
        for i in range(1,len(tableRows)):
            tableData = tableRows[i].find_all('td')
            if(len(tableData)==1):
                break
            CIN = tableData[0].get_text()
            compName = tableData[1].get_text()
            beginDate = tableData[2].get_text()
            endDate = tableData[3].get_text()
            activeCompliance = tableData[4].get_text()
            company = {
                "CIN": CIN,
                "name": compName,
                "beginDate": beginDate,
                "endDate": endDate,
                "activeCompliance": activeCompliance
            }
            companies.append(company)

        llpDataTable = masterDiv.find('table', id="llpData")
        listLLP = []
        tableRows1 = llpDataTable.find_all('tr')

        for i in range(1,len(tableRows1)):
            tableData = tableRows1[i].find_all('td')
            if(len(tableData)==1):
                break
            LLPIN = tableData[0].get_text()
            llpName = tableData[1].get_text()
            beginDate = tableData[2].get_text()
            endDate = tableData[3].get_text()

            llp = {
                "LLPIN": LLPIN,
                "name": llpName,
                "beginDate": beginDate,
                "endDate": endDate
            }
            listLLP.append(llp)   
        
        DINdetails = {
            "name": name,
            "DIN": din,
            "companies": companies,
            "llpList": listLLP
        }

        return jsonify(DINdetails)

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching DIN Details"})
    

if __name__ == "__main__":
    app.run()