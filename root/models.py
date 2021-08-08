#from CSGM_APIs import Check_NVEligibility_url
from django.db import models 

class ChatTracker(models.Model): 
    chatid = models.CharField(max_length=5000,default="", blank=True) 
    init_message = models.CharField(max_length=5000,default="", blank=True,)
    variable_state = models.CharField(max_length=5000,default="", blank=True)
    ResidenceZip = models.CharField(max_length=100,default="", blank=True)
    ResidenceCity = models.CharField(max_length = 100, default = "", blank = True)
    ResidenceState = models.CharField(max_length  =100, default=True)   
    email = models.CharField(max_length=100,default="", blank=True)
    token = models.CharField(max_length = 40,default="d3a1b634-90a7-eb11-a963-005056a96ce9")
    #user define
    flowchart3_stucked_status = models.BooleanField(default=False)
    #user define for CoverateCheck API and te future
    #Tribal = models.BooleanField(default=False)
    #userconfiguration API 
    ReservationUserCode = models.CharField(max_length=100,default="", blank=True)
    ReservationClientCode = models.CharField(max_length=100,default="", blank=True)
    ReservationVendorCode = models.CharField(max_length=100,default="", blank=True)
    ReservationAgentCode = models.CharField(max_length=100,default="", blank=True)
    #state configuration API
    TribalEligible = models.CharField(max_length=100,default="", blank=True)
    FcraDisclosureText = models.CharField(max_length = 1000,default="",blank=True)
    FcraAdditionalDisclosureText = models.CharField(max_length = 1000,default="",blank=True)
    FcraAcknowledgement = models.CharField(max_length = 1000,default="",blank=True)
    EligibiltyPrograms = models.CharField(max_length = 100,default = "",blank = True)

    #startorder API
    OrderNumber = models.CharField(max_length = 100,default=0,blank=True)
    PackageId = models.CharField(max_length=100,default = "",blank=True)
    #user define
    TribalResident = models.BooleanField(default=False)
    #users input
    program = models.CharField(max_length=100,default="", blank=True)
    first_name = models.CharField(max_length=100,default="", blank=True)
    middle_name = models.CharField(max_length=100,default="", blank=True)
    last_name = models.CharField(max_length=100,default="", blank=True)
    second_last_name = models.CharField(max_length=100,default="", blank=True)
    suffix = models.CharField(max_length=100,default="", blank=True)
    date = models.CharField(max_length=100,default="", blank=True)
    last_four_social = models.CharField(max_length=100,default="", blank=True)
    residential_address = models.CharField(max_length=100,default="", blank=True)
    shipping_address = models.CharField(max_length=100,default="", blank=True)
    apt_unit1 = models.CharField(max_length=100,default="", blank=True)
    apt_unit2 = models.CharField(max_length=100,default="", blank=True)
    is_permanent = models.BooleanField(default=True)
    address_nature = models.CharField(max_length=100,default="", blank=True)
    form_filled = models.BooleanField(default=False)

    shipping_address = models.CharField(max_length=100,default="", blank=True)
    form_zip_code = models.CharField(max_length=100,default="", blank=True)
    #DisclosuresConfiguration
    ServicePlan = models.CharField(max_length = 30,default = "",blank = True)
    iehBool = models.BooleanField(default=False)
    benefit_code = models.CharField(max_length=10,default="")
    zap_acct = models.CharField(max_length = 10,default="")
    zap_name = models.CharField(max_length = 10,default="")
    sequence_count = models.CharField(max_length = 5, default = "0")
    islifeline_service = models.CharField(max_length=20,default="",blank=True)
    other_adult = models.CharField(max_length=20,default="",blank=True)
    share_liveing_expesses = models.CharField(max_length=20,default="",blank=True)
    #SubmitOrder
    PhoneNumber = models.CharField(max_length=10,default="",blank=True)
    PinCode = models.CharField(max_length=4,default="",blank=True)
    BestWayToReachYou =  models.CharField(max_length=10,default="",blank=True)
    #CheckNVEligibility
    ApplicationStatus = models.CharField(max_length = 50,default = "",blank = True)
    Check_NVEligibility_url = models.CharField(max_length = 1000,default="",blank=True)
    def __str__(self):
        return str(self.chatid)+"__"+str(self.ResidenceZip)

class Sequence(models.Model):
    """
    contains the sequence information
    """        
    sequence_id = models.CharField(max_length=18,primary_key=True)
    text = models.TextField()
    type = models.CharField(max_length = 40)

    def __str__(self):
        return self.text