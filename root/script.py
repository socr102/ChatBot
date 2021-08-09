from root.analyzer import *
import os,django  
from root.CSGM_APIs import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

from root.models import ChatTracker


chatid = "O4U5YHR1ESL"
message = "Hello, how are u ?"
message = "THIS IS my zip code 40100"
message = "THIS IS my zip code 40100 mashood@gmail.com"


def CLEAR_ENTITY(currentchat):
    currentchat.ResidenceZip=''
    currentchat.email=''
    currentchat.flowchart3_stucked_status=False
    currentchat.save()


def generateReply(chatid,incoming_message): 

    ischatidexist = ChatTracker.objects.filter(chatid=chatid).exists()
    if ischatidexist:pass
    else:ChatTracker(chatid=chatid).save()

    currentchat = ChatTracker.objects.get(chatid=chatid)
    avaliable_choices = ['inithello','irrelevent-int--force-zipcode','zipcode','email']

    if currentchat.init_message=='':
        init_message = INIT_MESSAGE_HANDLER(incoming_message) 
        return get_start(chatid,init_message)
    elif currentchat.init_message !='':
        if currentchat.ResidenceZip=='':
            return   ZIPCODE_FINDER(chatid,incoming_message)
        elif currentchat.init_message =="Get_email":
           return  EMAIL_FINDER(chatid,incoming_message)  
        elif currentchat.flowchart3_stucked_status is True:
            incoming_message = incoming_message.lower()
            return GET_FLOWCHAT_STATE(incoming_message,chatid)
        elif currentchat.init_message=='STARTFLOWCHART3':
            check = CheckAvailability_API(currentchat.ResidenceZip,currentchat.email)
            if check:
                userConfiguration = UserConfiguration_API(chatid)
                if userConfiguration:
                    currentchat.ReservationUserCode = userConfiguration['ReservationUserCode']
                    currentchat.ReservationAgentCode = userConfiguration['ReservationAgentCode']
                    currentchat.ReservationClientCode = userConfiguration['ReservationClientCode']
                    currentchat.ReservationVendorCode = userConfiguration['ReservationVendorCode']
                    currentchat.save()
                    stateConfiguration = StateConfiguration_API(chatid)                  
                    if stateConfiguration:
                        if currentchat.ResidenceState == "CA":
                            currentchat.TribalEligible = stateConfiguration['TribalEligible']
                            currentchat.FcraDisclosureText = stateConfiguration['FcraDisclosureText']
                            currentchat.FcraAdditionalDisclosureText = stateConfiguration['FcraAdditionalDisclosureText']
                            currentchat.FcraAcknowledgement = stateConfiguration['FcraAcknowledgement']
                            currentchat.EligibiltyPrograms = stateConfiguration['EligibiltyPrograms'][0]['Code']
                            currentchat.save()
                        else:
                            currentchat.TribalEligible = stateConfiguration['TribalEligible']
                            currentchat.EligibiltyPrograms = stateConfiguration['EligibiltyPrograms'][0]['Code']
                            currentchat.save()
                        startOrder = StartOrder_API(chatid)
                        if startOrder:
                                currentchat.OrderNumber = startOrder['OrderNumber']
                                currentchat.PackageId = startOrder['PackageId']
                                currentchat.save()
                                currentchat.init_message = "STARTFLOWCHART4"
                                currentchat.save()


                                return [f'http://3.84.239.72:8000/submit_info/{chatid}','url']
                        
                currentchat.flowchart3_stucked_status=True
                currentchat.save()
                return ["Oh no! Our system is having trouble with your application","normal_restart_help"]
            else:
                CLEAR_ENTITY(currentchat)
                return [f'Sorry! We currently do not offer any service plans for the ZIP CODE {currentchat.ResidenceZip} area. Please try with other ZipCode. : Enter zip code again!','normal']
            
        elif currentchat.init_message == 'STARTFLOWCHART4':
            return STARTFLOWCHAT4(chatid)
        elif currentchat.init_message == "TribalResident":
            return SET_TribalResident(incoming_message,chatid) 
        elif currentchat.init_message == "Confirm_information":   
            return SET_ConfirmInfo(chatid)
        elif currentchat.init_message == "edit":
            return EDIT_Info(incoming_message,chatid)      
        elif currentchat.init_message == "edit_item":
            return EDIT_Info_item(incoming_message,chatid)
        elif currentchat.init_message == "save_item":
            return SAVE_Info(incoming_message,chatid)
        elif currentchat.init_message == "FCRATEXT":
            return FCRATEXT(incoming_message,chatid)
        #start the flowchat5            
        elif currentchat.init_message == "CGMChecks":
            return CGMChecks(chatid)
        elif currentchat.init_message == "ConfirmError": 
           if "help" in incoming_message:
                reply = ["An agent will  reach out  shortly!","normal"]
                return reply 
        elif currentchat.init_message == "help":
            if "help" in incoming_message:
                reply = ["An agent will  reach out  shortly!","normal"]
                return reply  
        elif currentchat.init_message == "Lifeline":
            response = Lifeline_API(chatid)
            return Lifeline_state(response,chatid)      
        elif currentchat.init_message=="lifeline_success":
            return lifeline_success(incoming_message,chatid)
        elif currentchat.init_message == "setLanguageEs":
            return setLanguageEs(chatid,incoming_message)
        elif currentchat.init_message == "setLanguageCk":
            return setLanguageCK(chatid,incoming_message)
        elif currentchat.init_message == "setLanguageJv":
            return setLanguageJv(chatid,incoming_message)
        elif currentchat.init_message == "lifeline_failure":
            currentchat.init_message = "agent_help"
            currentchat.save()
            return ["An agent will reach out shortly! Thank you for your patience.","normal_help"]  
        elif  currentchat.init_message == "check_status_lifeline":
                if currentchat.ResidenceState=="CA":
                    response = CheckNladEbbApplicationStatus_API(chatid) 
                    return Check_Status_Lifeline(response,chatid)          
                else:
                    response = CheckNVApplicationStatus_API(chatid)
                    return Check_Status_Lifeline(response,chatid)         
        elif currentchat.init_message=="DisclosuresConfiguration":
            return Disclosure(chatid)
        elif currentchat.init_message=="iehBool":
            return iehBool(chatid)
        elif  currentchat.init_message=="DuplicateSubscriber":
            return DuplicateSubscriber(incoming_message,chatid)
        elif currentchat.init_message == "lifelineService":
            return lifelineService(incoming_message,chatid)                 
        elif currentchat.init_message=="otherAdult":
            return otherAdult(incoming_message,chatid)
        elif currentchat.init_message=="share_living_expenses":
            return shareliving_expenses(incoming_message,chatid)   
        elif currentchat.init_message=="before_share_living_expenses":
            return beforeShare(incoming_message,chatid)
        elif currentchat.init_message=="submitorder":
            return getProgram(chatid) 
        elif currentchat.init_message == "verifyIncome":
            currentchat.init_message = "uploadIncome"
            currentchat.save()
            return ["what dollar amount is on your income proof?","normal_autoPass"]
        elif currentchat.init_message ==  "uploadIncome":
            currentchat.init_message = "moreIncome"
            currentchat.save()
            return ["Please upload your proof of income?","normal"]
        elif currentchat.init_message == "moreIncome":
            if  str(incoming_message).isnumeric():
                currentchat.Income = int(incoming_message)
                currentchat.init_message = "moreIncomeCheck"
                currentchat.save()
                return ["Do you have more income information to provide?","normal_yes_no"]
            else:
                return ["Please Input the correct Income","normal"]    
        elif currentchat.init_message == "moreIncomeCheck":
            return moreIncome(incoming_message,chatid)
        elif currentchat.init_message == "BestWay":
            return getBestway(incoming_message,chatid)    
        elif currentchat.init_message == "validPhoneNumber":
            return validPhoneNumber(incoming_message,chatid)
        elif currentchat.init_message=="makePinCode":
            return makePinCode(incoming_message,chatid)
        elif currentchat.init_message=="runSubmitOrder":
            response = SubmitOrder_API(chatid)  
            return submitOrder(response,chatid) 
        elif currentchat.init_message=="checkNvEligibility":
            response = Check_NVEligibility_API(chatid)
            return checkNvEligibility(response,chatid)
        elif currentchat.init_message=="Order_error":
            return submitOrderError(incoming_message,chatid)        
        elif currentchat.init_message == "CNEURL":
            return CNEURL(chatid)
        elif currentchat.init_message == "checkNvEligibilityContinue":
            if incoming_message=="yes":
                currentchat.init_message = "checkNvEligibility"
                currentchat.save()
                return ["Check NV Eligibility","normal_autoPass"]
                
            return["Continue Application","normal_yes"]    
        elif currentchat.init_message=="PendingNational":
            return PendingNational(chatid)   
        elif currentchat.init_message=="nationalVerifierHelp":
            currentchat.init_message = "EndChat"
            currentchat.save()
            return ["An agent will reach out shortly! Thank you for your patience.","normal"]      
        elif currentchat.init_message == "checkNvEligibilityAgain":
            return CheckNVEligibilityAgain(incoming_message,chatid) 
        elif currentchat.init_message == "getLifelineform":
            response = GetLifelineFormcall_API(chatid)
            return getLifelineform(response,chatid)  
        elif currentchat.init_message == "submitServiceType":
            response1 = SubmitServiceType_API(chatid)
            if response1['Status'] == "Success":
                response2 = SubmitServiceStatus_API(chatid)
                if response2['Status'] == "Success":
                    currentchat.init_message = "VeryfyCheckNVEligibility"
                    currentchat.save()
                    return["VeryfyCheckNVEligibility","normal_autoPass"]
            currentchat.init_message = "submitService"
            currentchat.save()        
            return ["Oh no! We are having trouble processing your application","normal_help"]  
        elif currentchat.init_message == "submitService":
            currentchat.init_message = "EndChat"
            currentchat.save()
            if incoming_message=='help':
                return ["An agent will reach out shortly!Thank you for you","normal"]  
        elif  currentchat.init_message == "VeryfyCheckNVEligibility":
            response = Check_NVEligibility_API(chatid) 
           # if response['Status']=="Success":
            if currentchat.ApplicationStatus=="Complete":
                #currentchat.ApplicationStatus = response['ApplicationStatus']
                currentchat.save()
                if currentchat.ApplicationStatus=='Complete':
                    currentchat.init_message = "EndSuccess"
                    currentchat.save()
                    return["EndSuccess...","normal_autoPass"] 
                else:
                    currentchat.init_message = "checknvEligibilityfail"
                    currentchat.save()
                    return ["Oh no! Your application was not completed in the National Verifier","normal_help" ]    
            else:
                    currentchat.init_message = "checknvEligibilityfail"
                    currentchat.save()
                    return ["Oh no!Your request was rejected by the National Verifier.","normal_help" ]     
        elif currentchat.init_message == "checknvEligibilityfail":
            currentchat.init_message = "EndChat"
            currentchat.save()
            if incoming_message=='help':
                if incoming_message=='help':
                    return ["An agent will reach out shortly!Thank you for you","normal"] 
        elif currentchat.init_message == "EndSuccess" :
            currentchat.init_message = "EndChatBefore"
            currentchat.save()
            return ["Congratulations! Your application is complete!Thank you for choosing Access Wireless.Your order number is: " + str(currentchat.OrderNumber) + " We will contact you when your applications has been finalized.","normal_autoPass"] 
        elif currentchat.init_message == "EndChatBefore" :
            currentchat.init_message = "EndChat"
            currentchat.save()
            return ["Get your friends and family FREE phone and service by sharing this link:http://m.me/accesswirelesslifeline","normal"]               
# return reply

if __name__ == '__main__':
     generateReply(chatid,message)