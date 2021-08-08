import re,requests 
from root.models import ChatTracker
from root.CSGM_APIs import *
def INIT_MESSAGE_HANDLER(message):
    message = str(message).lower()
    possible_keywords = ['hello','hola','hi','hey','helo']
    for keyword in possible_keywords:
        if keyword in message:
            init =  'inithello'
            return init
    else: 
        init =  'irrelevent-int--force-zipcode'
        return init
def get_start(chatid, init_message):
    avaliable_choices = ['inithello','irrelevent-int--force-zipcode','zipcode','email']
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    if init_message in avaliable_choices:
        currentchat.init_message = init_message
        currentchat.save() 
        reply = ["Hello!👋 I am a bot and I am here to help. What is your Zip Code?","normal"]
        return reply  
    else:
        reply = ["Hello!👋 I am a bot and I am here to help. What is your Zip Code?","normal"]
        return reply 
def ZIPCODE_FINDER(chatid,message):
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    message = str(message).lower().split(' ')
    zipcode=''
    for keyword in message:  
        if len(keyword)==5 and str(keyword).isnumeric():
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={keyword}&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI"
            response = requests.get(url)
            if  response.json()['status']=='OK':
                currentchat.init_message = "Get_email"
                zipcode=keyword
                currentchat.ResidenceZip = zipcode
                currentchat.ResidenceCity = response.json()['results'][0]['address_components'][1]['short_name']
                currentchat.ResidenceState = response.json()['results'][0]['address_components'][2]['short_name']
                currentchat.save()
                return ["Great! That was a valid zip code! 🎉\nPlease enter your email address? (Ex: example@mail.com) 💬","normanl"]
    else:
        return  ["That Zip Code was not valid. Please enter a valid zip code.","normal"]

def EMAIL_FINDER(chatid,message):
    currentchats = ChatTracker.objects.filter(chatid=chatid)
    currentchat = currentchats.first()

    message = str(message).lower()
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", message)
   
    if len(email)>0 :
        email = email[0]
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        if status=='valid':
            print("-->email verified")
            currentchat.email = email
            currentchat.save()
            currentchat.init_message = "STARTFLOWCHART3"
            currentchat.save()
            return ["Thank You! This will just take a few seconds You are on your way to a FREE phone!📱","normal_autoPass"]
        else:
            return  ["That email address was not valid. Please enter a working email address. (Ex: example@mail.com)","normal"]
    elif len(email)==0:
        print("emial-->not verified")
        return  ["That email address was not valid. Please enter a working email address. (Ex: example@mail.com)","normal"]
     
def GET_FLOWCHAT_STATE(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'restart' in incoming_message:
        currentchat.flowchart3_stucked_status = False
        currentchat.ResidenceZip = ""
        currentchat.init_message = "init"
        currentchat.save()
        return ['Please enter a valid ZipCode.','normal']
    elif 'help' in incoming_message :
        currentchat.flowchart3_stucked_status = False
        currentchat.ResidenceZip = ""
        currentchat.init_message = "init"
        currentchat.save()
        return ['An agent will reach out shortly! Thank you for your patience.','normal']
       
def STARTFLOWCHAT4(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if currentchat.TribalEligible == True:
        reply = ["Do you reside on Federally-recognized Tribal lands?","normal_yes_no"]
        currentchat.init_message = "TribalResident"   
        currentchat.save()
        return reply
    else:
        currentchat.TribalResident = False
        currentchat.init_message = "Confirm_information"
        reply = ["Confirm your information again?","normal_autoPass"]
        currentchat.save() 
        return reply
def SET_TribalResident(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'yes' in incoming_message:
        currentchat.TribalResident = True
        currentchat.save() 
    elif 'no' in incoming_message:
        currentchat.TribalResident = False
        currentchat.save() 
    currentchat.init_message = "Confirm_information"
    currentchat.save() 
    return ["Confirm your information again?","normal_autoPass"]

def SET_ConfirmInfo(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "edit"
    currentchat.save()
    return ["Confirm your information again?",currentchat.first_name, currentchat.middle_name, currentchat.last_name,currentchat.suffix,currentchat.date,currentchat.last_four_social,currentchat.residential_address,currentchat.apt_unit1,currentchat.ResidenceCity,currentchat.ResidenceState,currentchat.ResidenceZip]

def EDIT_Info(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if 'yes' in incoming_message:
        reply = ["What would you like to edit?","FirstName", "MiddleName", "LastName","Suffix","Date Of Birth","Socical Security Number","ResidenceAddress","Apt","ResidenceCity","State","ZipCode"]
        currentchat.init_message = "edit_item"
        currentchat.save()
        return reply
    elif 'no' in incoming_message:
        result = NationalVerification(id)
        if  result['Status'] == "Success":
            if currentchat.ResidenceState!="CA":
                currentchat.init_message = "CGMChecks"
                currentchat.save()
                return ["CGM Checks...","normal_autoPass"]
            else:
                currentchat.init_message = "FCRATEXT"
                currentchat.save()
                return ["FCRADISCLOSURETEXT :"+currentchat.FcraDisclosureText+"  FCRAADDITIONALDISCLOSURETEXT:"+currentchat.FcraAdditionalDisclossureText+"  FCRAACKNOWLEDGEMENT : "+currentchat.FcraAcknowledgement+" - I agree : y/[n","normal"] 
        elif result['Status'] == "Failure":
            currentchat.init_message = "Confirm_information"
            currentchat.save()
            if "Invalid" in result['Message'] :
                return ["Your information did not pass out checks!","normal"]
            elif "Validation error" in result['Message'] :
                return ["Oh no! WE couldn't validate your information."+str(result['ValidationErrors']) +"Please correct the error","normal"]
        else:
            return ["Please Select the one of buttons","normal"] 
            
def EDIT_Info_item(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "save_item"
    currentchat.variable_state = incoming_message
    currentchat.save()
    if incoming_message=="DateOfBirth":
        return ["Please Enter the Date Of Birth again : MM-DD-YYYY","normal"]

    return ["Please Enter the "+ incoming_message + " again","normal"]

def SAVE_Info(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.init_message = "Confirm_information"
    currentchat.save()
    if currentchat.variable_state == "FirstName":
        currentchat.first_name = incoming_message  
        currentchat.save()
    elif currentchat.variable_state == "MiddleName":
        currentchat.middle_name = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "LastName":
        currentchat.last_name = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "Suffix":
        currentchat.suffix = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "DateOfBirth":
        currentchat.date = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "Socical Security Number":
        if len(incoming_message)==4 and str(incoming_message).isnumeric():
            currentchat.last_four_social = incoming_message
            currentchat.save()
    elif currentchat.variable_state == "ResidenceAddress":
        currentchat.residential_address = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "Apt":
        currentchat.apt_unit1 = incoming_message  
        currentchat.save()
    elif currentchat.variable_state == "ResidenceCity":
        currentchat.ResidenceCity = incoming_message 
        currentchat.save()
    elif currentchat.variable_state == "ZipCode":
        currentchat.ResidenceZip = incoming_message
        currentchat.save()
    elif currentchat.variable_state == "State":
        currentchat.ResidenceState = incoming_message
        currentchat.save()
    currentchat.variable_state = ""
    return["Continue","normal_autoPass"]

def FCRATEXT(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if "y" in incoming_message:
        currentchat.init_message = "CGMChecks"
        currentchat.save()
        return ["CGM Checks...","normal_autoPass"]    
            
def CGMChecks(id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()  
    response = FLOWCHAT5(id)
    print(response)
    if response=="error":
        currentchat.init_message="help"
        currentchat.save()
        return ["Oh no! Our System is having trouble wity your request","normal"]
    elif response=="No-Pass":
        currentchat.init_message = "End_chat"
        currentchat.save()
        return ["Sorry! We do not currently offer coverage in your area.","normal"]
    elif response == "Pass":
        if currentchat.ResidenceState!="CA":
            currentchat.init_message = "Lifeline"
            currentchat.save()
            return ["Let's start Lisfeline",'normal_autoPass']
        elif ConfirmState(id):
            currentchat.init_message = "Lifeline"
            currentchat.save()
            return ["Let's start Lisfeline",'normal_autoPass']
        else:
            currentchat.init_message = "ConfirmError"
            currentchat.save()
            return ["Oh no! Our system is having trouble with your request",'normal']

def Lifeline_state(response,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    if response['Status'] == "Success":
        currentchat.init_message = "lifeline_success"
        currentchat.save()
        plan = ["You quality for"]
        for i in range(0,len(response['LifelinePlans'])):
            mid=(str(response['LifelinePlans'][i]["Name"]))
            plan.append(mid)
        
        return [plan,"LifelinePlans","normal"]
    else:
        currentchat.init_message = "lifeline_failure"
        currentchat.save()
        return["Oh no! We could not find any plans that you qualify for.","normal_help"]              

def lifeline_success(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()
    currentchat.ServicePlan = incoming_message
    currentchat.save()
    if currentchat.ResidenceState=="CA":
        currentchat.init_message = "setLanguageEs"
        currentchat.save()
        return ["What language do you prefer to speak? 😊", "normal_language_ES"]
    else:
        currentchat.init_message = "check_status_lifeline"
        currentchat.save()  
        return ["Track ApplicationStatus...","normal_autoPass"] 

def setLanguageEs(id,incoming_message):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first() 
    if  incoming_message == "English" or incoming_message == "Spanish":
        currentchat.language  = incoming_message
        currentchat.init_message = "check_status_lifeline"
        currentchat.save()
        return ["Do you prefer statmdard pring, or LARGE PRINT ontifications?","Contact Access Wireless Customer Service directly if you would like to receive future communications from  the California LifeLine Administrator in Braille.","normal_check"]
    elif incoming_message== "more languages":
        currentchat.init_message = "setLanguageCk"
        currentchat.save()
        return ["What language do you prefer to speak? 😊","normal_language_CK"]  

def setLanguageCK(id,incoming_message):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first()        
    if  incoming_message == "Chinese" or incoming_message == "Korean":
        currentchat.language  = incoming_message
        currentchat.init_message = "check_status_lifeline"
        currentchat.save()
        return ["Do you prefer statmdard pring, or LARGE PRINT ontifications?","Contact Access Wireless Customer Service directly if you would like to receive future communications from  the California LifeLine Administrator in Braille.","normal_check"]
    elif incoming_message== "more languages":
        currentchat.init_message = "setLanguageJv"
        currentchat.save()
        return ["What language do you prefer to speak? 😊","normal_language_JV"]       

def setLanguageJv(id,incoming_message):
    currentchats = ChatTracker.objects.filter(chatid=id)
    currentchat = currentchats.first() 
    if  incoming_message == "Japanese" or incoming_message == "Vietnames":
        currentchat.language  = incoming_message
        currentchat.init_message = "check_status_lifeline"
        currentchat.save()
        return ["Do you prefer statmdard pring, or LARGE PRINT ontifications?","Contact Access Wireless Customer Service directly if you would like to receive future communications from  the California LifeLine Administrator in Braille.","normal_check"]        
def Check_Status_Lifeline(response,id):
    print(response)
    print(response.keys())
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    if "ApplicationStatus" in response.keys():
        if response['ApplicationStatus'] == "ApplicationPending":
            currentchat.init_message = "check_status_lifeline"
            currentchat.save()
            return["Your application is still being processed by the National verifier! Click here to check its status.","normal_check"]
        elif response['ApplicationStatus'] == "ApplicationNotComplete" or response['ApplicationStatus'] == "ApplicationNotFound":
            currentchat.init_message = "DisclosuresConfiguration"
            currentchat.save()
            return["DisclosuresConfiguration","normal_autoPass"]   
        else:  
            currentchat.init_message = "DuplicateSubscriber"
            currentchat.save()
            return["We noticed that you are already receiving a  Lifeline benefit from another provider. Would you like to transfer your service provider to Access Wireless? 😊","normal_yes_no"]        
    else:
            currentchat.init_message = "DisclosuresConfiguration"
            currentchat.save()
            return["DisclosuresConfiguration","normal_autoPass"] 

def DuplicateSubscriber(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    if "yes" in incoming_message:
        currentchat.init_message="DisclosuresConfiguration"
        currentchat.save()
        return ["Great! We're glad to have you 😍","normal_autoPass"]    
    elif "no" in incoming_message:
        currentchat.init_message="EndChat"
        currentchat.save()
        return["😥 We're sad to see you go!","normal"]
def Disclosure(id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    currentchat.init_message="iehBool"
    currentchat.save()
    return [f'http://localhost:8000/start/{id}','url']

def iehBool(id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    if currentchat.iehBool==True:
        currentchat.init_message = "lifelineService"
        currentchat.save()
        return ["Does your spouse or domestic partner live with you AND already receive LifeLine phone service? Select NO if you do not have a spouse or partner. Select NO if your spouse or partner does not live with you. Select NO if your spouse or partner does not receive lifeline phone service?","normal_yes_no"]   
    else:
        currentchat.init_message="submitorder"
        currentchat.save()
        return["SubmitOrdering...","normal_autoPass"]     
def lifelineService(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    if "yes" in incoming_message:
        currentchat.init_message="EndDisclosuresConfiguration"
        currentchat.save()
        return["I'm Sorry 😥 You do not qualify to apply for Lifeline because someone in your household already gets the benefit. Each household is allowed to get only ONE Lifeline.","normal"]      
    else:
        currentchat.islifeline_service="No"
        currentchat.init_message = "otherAdult"
        currentchat.save()
        options = ["Other than a spouse or partner, do other adults (people over the age of 18 or emancipated minors) live with you at your address? If so, are they your:","Parent","Child(+18)","Other Adult Relative","Adult Rommate","Other Adult","No Adult"]
        return[options,"otherAdult","normal"]

def otherAdult(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()

    if incoming_message=="Other Adult":
        currentchat.init_message = "before_share_living_expenses"
        currentchat.save()   
        return["Please specify:What is their relationship to you?","normal"]     
    elif incoming_message=="No Adult":
        currentchat.init_message = "submitorder"
        currentchat.save() 
        return["YES! You qualify to apply for Lifeline! 🎉😁🎉","normal_autoPass"]    
    else:
        currentchat.other_adult = incoming_message
        currentchat.init_message = "share_living_expenses"
        currentchat.save()  
        return["Do you share living expenses (bills, food, etc.) and share income (either your income, their income, or both incomes together) with the adult you listed above? 🏠💵","normal_yes_no"]     

def shareliving_expenses(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    if "yes" in incoming_message:
        currentchat.init_message = "EndDisclosuresConfiguration"
        currentchat.save()  
        return["I'm Sorry 😥 You do not qualify to apply for Lifeline because someone in your household already gets the benefit.Each household is allowed to get only ONE Lifeline.","normal"]
    elif "no" in incoming_message:
        currentchat.init_message = "submitorder"
        currentchat.save() 
        return["YES! You qualify to apply for Lifeline! 🎉😁🎉","normal_autoPass"]  
def beforeShare(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    currentchat.other_adult = incoming_message
    currentchat.init_message = "share_living_expenses"
    currentchat.save()  
    return["Do you share living expenses (bills, food, etc.) and share income (either your income, their income, or both incomes together) with the adult you listed above? 🏠💵","normal_yes_no"]
def getProgram(id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    print(currentchat.program)
    if currentchat.program == "135p":
        currentchat.init_message = "verifyIncome"
        currentchat.save()
        return ["To continue we'll need to verify some of your income information💲","normal_autoPass"]
    elif currentchat.program == "150p":
        currentchat.init_message = "verifyIncome"
        currentchat.save()
        return ["To continue we'll need to verify some of your income information💲","normal_autoPass"]
    else:
        options = ["what is the best way  to reay you ? Click one of the options below","Phone","Email","Mail"]
        currentchat.init_message = "BestWay"
        currentchat.save()
        return[options,"selectOption","normal"]

def moreIncome(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    if "yes" in incoming_message:
        return getProgram(id)
    else:
        options = ["what is the best way  to reach you ? Click one of the options below","Phone","Email","Mail"]
        currentchat.init_message = "BestWay"
        currentchat.save()
        return[options,"selectOption","normal"]   

def getBestway(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    print("getbestway")
    if incoming_message=="Phone":
        print("-->phone")
        currentchat.BestWayToReachYou = "phone"
        currentchat.init_message = "validPhoneNumber"
        currentchat.save()
        return ["What is your phone number? 📱 It can look like this: 5417901356","normal"]      
    else:
        print("-->email")
        currentchat.BestWayToReachYou = "email"
        currentchat.init_message = "makePinCode"
        currentchat.save()
        return ["Please make a four digit PIN for your application","normal"]  

def validPhoneNumber(number,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    if len(number)==10 and str(number).isnumeric():
        currentchat.PhoneNumber = number
        currentchat.init_message = "makePinCode"
        currentchat.save()
        return ["Please make a four digit PIN for your application","normal"]
    else:
        return["Verify all numbers and 10 digits long","normal"]      

def makePinCode(number,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    if len(number)==4 and str(number).isnumeric():
        currentchat.init_message = "runSubmitOrder"
        currentchat.PinCode = number
        currentchat.save()
        return ["SubmitOrder Call Checking","normal_autoPass"]       
    else:
        return["Verify all numbers and 4 digits long","normal"]      
def submitOrder(response,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    if response['Status'] == "Success":
        currentchat.init_message = "checkNvEligibility"
        currentchat.save()
        return ["Check NV Eligibility","normal_autoPass"]
    else:
        currentchat.init_message = "submit  Order_error"
        currentchat.save()
        return["Oh no! Your order failed: How would you like to proceed?","normal_restart_help_national"]   
def submitOrderError(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    if incoming_message=="restart":
         currentchat.init_message==''
         currentchat.ResidenceZip=''
         currentchat.email=''
         currentchat.flowchart3_stucked_status=False
         currentchat.save()
         return["Please restart!!","normal_autoPass"]
    elif incoming_message=="help":
         currentchat.init_message=='EndChat'
         currentchat.save()
         return["An agent will reach out shortly! Thank you for your patience.","normal"]
    elif incoming_message=="national Verfier":
         currentchat.init_message=='NationalVeriferQuestions'
         currentchat.save()
         return["NationalVeriferQuestions.","normal"]
def checkNvEligibility(response,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    currentchat.Check_NVEligibility_url = response['Action']['RedirectUrl']
    currentchat.save()
    if response['Status']=="Success":
        if currentchat.ApplicationStatus =="Complete":
            currentchat.init_message = "getLifelineform"
            currentchat.save()
            return ["GetLifelineForm",'normal_autoPass'] 
        currentchat.ApplicationStatus = response['ApplicationStatus']
        if response['ApplicationStatus'] in  ["PendingCertification","PendingResolution","PendingEligibility"]:
            currentchat.init_message = "CNEURL"
            currentchat.ApplicationStatus = "Complete"
            currentchat.save()
            message = ["We've filled out most of your application in the National Verifier with the information you provided.","To proceed, you'll need to confirm some of your information at the National Verifier's website.","Click below ⬇ When you've completed your application, you will be finished enrolling! You have 7 minutes before this link expires"]
            return [message,"CheckNVEligibility","normal_autoPass"]
        elif response['ApplicationStatus'] == "Complete":
            currentchat.init_message = "getLifelineform"
            currentchat.save()
            return ["GetLifelineForm",'normal_autoPass']    
        elif response['ApplicationStatus'] in ["PendingReview","InProgress"]:
            currentchat.init_message = "PendingNational"
            currentchat.save()
            return["Your Application is Pending National Verifier Review. Click here to check the status","normal_check"]
    else:
        currentchat.init_message = "nationalVerifierHelp"
        currentchat.save()
        return ["Oh no! Your request was reject by the National Verifier.","normal_help"]    
def PendingNational(id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    currentchat.init_message = "checkNvEligibility"
    currentchat.save()
    return ["Check NV Eligibility","normal_autoPass"]
def CNEURL(id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first()
    currentchat.init_message = "checkNvEligibilityAgain"
    url = currentchat.Check_NVEligibility_url
    currentchat.save()
    return  [url,"url"]

def CheckNVEligibilityAgain(incoming_message,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 

    if incoming_message=="yes":
        response = Check_NVEligibility_API(id)
        currentchat.Check_NVEligibility_url = response['Action']['RedirectUrl']
        currentchat.init_message = "checkNvEligibilityContinue"
        currentchat.save()
        return [currentchat.Check_NVEligibility_url,"url"]
    elif incoming_message =="no":
        currentchat.ApplicatonStatus = "Complete"
        currentchat.init_message = "checkNvEligibility"
        currentchat.save()
        return["Chekc NV Eligibility","normal_autoPass"]
    else:
        return["If the above link didn't work, click here(Yes) to make another!","normal_yes_no"] 
def getLifelineform(response,id):
    currentchats = ChatTracker.objects.filter(chatid=id)      
    currentchat = currentchats.first() 
    currentchat.init_message = "submitServiceType"
    currentchat.save()
    #if 'Status' in response.keys():
    if response == "Failure":
        return['submitServiceType','normal_autoPass']
    else:
        return["Here is a filled  out  copy  of your application","normal_autoPass"]    