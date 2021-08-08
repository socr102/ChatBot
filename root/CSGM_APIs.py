import requests
from requests.api import request
from root.models import ChatTracker

check_avaliability_url = 'https://lifeline.cgmllc.net/api/v2/checkavailability'
user_confituration_url = 'https://lifeline.cgmllc.net/api/v2/userconfiguration'
state_configuration_url = 'https://lifeline.cgmllc.net/api/v2/stateconfiguration'
start_order_url = 'https://lifeline.cgmllc.net/api/v2/startorder'
validate_name_address = ' https://lifeline.cgmllc.net/api/v2/validatenameaddress'
check_duplicate_customer ='https://lifeline.cgmllc.net/api/v2/checkduplicatecustomer'
coverage_check =  'https://lifeline.cgmllc.net/api/v2/coveragecheck'
confirm_state = 'https://lifeline.cgmllc.net/api/v2/confirmstateeligibility'
life_line_url = "https://lifeline.cgmllc.net/api/v2/lifelineplans"
Check_NVApplication_Status_url = "https://lifeline.cgmllc.net/api/v2/CheckNVApplicationstatus"
Check_NladEbbApplication_Status_url = "https://lifeline.cgmllc.net/api/v2/CheckNladEbbApplicationstatus"
submit_order_url = "https://lifeline.cgmllc.net/api/v2/submitorder"
Check_NVEligibility_url = "https://lifeline.cgmllc.net/api/v2/checknveligibility"
get_lifeline_url = "http://lifeline.cgmllc.net/api/v2/getlifelineform"
submit_service_type_url = "https://lifeline.cgmllc.net/api/v2/submitservicetype"
submit_service_status_url = "https://lifeline.cgmllc.net/api/v2/servicetypestatus"

token='d3a1b634-90a7-eb11-a963-005056a96ce9'

def CheckAvailability_API(zipcode,email):
    res = requests.post(check_avaliability_url, data={'Token':token,'ZipCode':zipcode,'Email':email}).json()
    if res['Status']=='Success':
        return res
    else:  
        return None

def UserConfiguration_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    res = requests.post(user_confituration_url,data={'Token':token}).json()
    if res['Status']=='Success':
        return res
    else:
        return None

def StateConfiguration_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    res = requests.post(state_configuration_url,data={'Token':token,'state':currentchat.ResidenceState}).json()
    if res['Status']=='Success':
        return res
    else:
        return None

def StartOrder_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()

    data = {
        'Token':token,
        'State':currentchat.ResidenceState,
        'AppVersion':'89.0.4389.72',
        'Platform':'WebApp',
        'SerialNumber':'www.zapier.com',
        'SaleTypeid':3
        }
    res = requests.post(start_order_url,data=data).json()
    
    if res['Status']=='Success':
        return res
    else:
        return None



   
def NationalVerification(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        'FirstName': currentchat.first_name,
        'LastName': currentchat.last_name,
        'DateOfBirth': currentchat.date,
        'SocialSecurityNo': currentchat.last_four_social,
        'StateEligibilityCode': currentchat.EligibiltyPrograms,
        'ResidenceAddress01': currentchat.residential_address,
        'ResidenceCity': currentchat.ResidenceCity,
        'ResidenceState': currentchat.ResidenceState,
        'ResidenceZip': currentchat.ResidenceZip,
        'PackageID': currentchat.PackageId,
        'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9',
        'VendorCode' : currentchat.ReservationVendorCode,
        'ClientCode' : currentchat.ReservationClientCode,
        'UserCode' : currentchat.ReservationUserCode,
        }
    res = requests.post(validate_name_address,data=data).json()
    return  res  
#Flowchat5
def Check_dulicate_customer(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {   
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": currentchat.PackageId,
        "FirstName": currentchat.first_name,
        "LastName": currentchat.last_name,
        "DateOfBirth": currentchat.date,
        "Ssn": currentchat.last_four_social,
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip
    }   
    res = requests.post(check_duplicate_customer,data=data).json()
    if res['Status'] == "Success":
        return res
    else:
        return None    
def Coverage_check(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": currentchat.PackageId,
        "Tribal": currentchat.TribalResident,
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip
        }
    res = requests.post(coverage_check,data=data).json()
    if res['TribalFail'] == True or res['TribalMismatch'] == True or res['TribalProgramMismatch'] ==True:
        currentchat.TribalResident = False
    if  res['TribalFail'] == False and res['TribalMismatch'] == False and res['TribalProgramMismatch'] ==False:
        if  "TribalVerified" in res.keys():
            if res['TribalVerified'] == True:
                currentchat.TribalResident = False

    if res['Status'] == "Success":
        return res
    else:
        return None   

def ConfirmState(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": currentchat.PackageId,
        "FirstName": currentchat.first_name,
        "LastName":currentchat.last_name,
        "DateOfBirth":currentchat.date,
        "SocialsecurityNo":currentchat.last_four_social,
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip,
        "TribalResident":currentchat.TribalResident,
        "Program":currentchat.program
    }
    res = requests.post(confirm_state,data=data).json()
    if res['Status'] == "Success":
        return res
    else:
        return None    

def FLOWCHAT5(id):
    if Check_dulicate_customer(id):
        response = Coverage_check(id)
        if response:
            if response['Coverage'] == True:
                reply = "Pass"
                return reply
            else:
                reply = "No-Pass"  
                return reply  
    reply = "error"    
    return reply

def Lifeline_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID" : currentchat.PackageId,
        "State" : currentchat.ResidenceState,
        "Zip" : currentchat.ResidenceZip,
        "Tribal" : currentchat.TribalResident
    }
    res = requests.post(life_line_url,data=data).json()
    return res
def CheckNladEbbApplicationStatus_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID" : currentchat.PackageId,
        "SSN" : currentchat.last_four_social,
        "FirstName" : currentchat.first_name,
        "LastName" : currentchat.last_name,
        "DOB" : currentchat.date,
        "PrimaryAddress1" :currentchat.residential_address,
        "PrimaryCity" : currentchat.ResidenceCity,
        "PrimaryState": currentchat.ResidenceState,
        "PrimaryZip" : currentchat.ResidenceZip,
        "Tribal" : currentchat.TribalResident,
    }
    res = requests.post(Check_NladEbbApplication_Status_url,data = data).json()
    return res
def CheckNVApplicationStatus_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID" : currentchat.PackageId,
        "SSN" : currentchat.last_four_social,
        "FirstName" : currentchat.first_name,
        "LastName" : currentchat.last_name,
        "DOB" : currentchat.date,
        "PrimaryAddress1" :currentchat.residential_address,
        "PrimaryCity" : currentchat.ResidenceCity,
        "PrimaryState": currentchat.ResidenceState,
        "PrimaryZip" : currentchat.ResidenceZip,
        "Tribal" : currentchat.TribalResident,
    }
    res = requests.post(Check_NVApplication_Status_url,data = data).json()
    return   res  

def SubmitOrder_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        "Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
        "PackageID": currentchat.PackageId,
        "EligibilityProgram": currentchat.EligibiltyPrograms,
        "FirstName": currentchat.first_name,
        "LastName": currentchat.last_name,
        "NameSuffix": currentchat.suffix,
        "DateOfBirth": currentchat.date,
        "Ssn": currentchat.last_four_social,
        "ResidenceAddress01": currentchat.residential_address,
        "ResidenceCity": currentchat.ResidenceCity,
        "ResidenceState": currentchat.ResidenceState,
        "ResidenceZip": currentchat.ResidenceZip,
        "BestWayToReachYou": currentchat.BestWayToReachYou,
        "PhoneNumber": currentchat.PhoneNumber,
        "Email": currentchat.email,
    }
    res = requests.post(submit_order_url,data = data).json()
    return res
def Check_NVEligibility_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        'Token':"d3a1b634-90a7-eb11-a963-005056a96ce9",
        'PackageID': currentchat.PackageId,
    }
    res = requests.post(Check_NVEligibility_url,data = data).json()
    return res
def GetLifelineFormcall_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
        'Token':"d3a1b634-90a7-eb11-a963-005056a96ce9",
        'PackageID': currentchat.PackageId,
    }
    #res = requests.post(get_lifeline_url,data = data).json()
    return "Failure"

def SubmitServiceType_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
    'Token' : "d3a1b634-90a7-eb11-a963-005056a96ce9",
    'PackageID' : currentchat.PackageId,
    'ServicePlan' : currentchat.ServicePlan
    }
    res = requests.post(submit_service_type_url,data = data).json()
    return res

def SubmitServiceStatus_API(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    data = {
    'Token' : "d3a1b634-90a7-eb11-a963-005056a96ce9",
    'PackageID' : currentchat.PackageId,
    }
    res = requests.post(submit_service_status_url,data = data).json()
    return res
if __name__ == '__main__':
    email='denea1288@gmail.com'
    email='denea128822@gmail.com'
    zipcode=30314