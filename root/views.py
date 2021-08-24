from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import ChatTracker,Sequence
from .script import generateReply
import  requests
import json

@csrf_exempt
def index(request):
    if request.method == 'POST':
        chatid = request.POST['chatid']
        message = request.POST['message']

        reply = generateReply(chatid, message)
        return JsonResponse({"message": reply})

@csrf_exempt
def get_info(request,id,token,PackageId,ResidneceState,TribalResident,EligibiltyPrograms):
    if request.method=='GET':
        item = ChatTracker.objects.get(chatid=id)
        #save the token, packageid, residencestate,trivalresident,eligibiltyprograms into the id
        item.token = token
        item.PackageId = PackageId,
        item.ResidenceState = ResidenceState
        item.TribalResident = TribalResident
        item.EligibiltyPrograms = EligibiltyPrograms
        item.save()

        data = {
            "program" : item.program,
            "first_name" : item.first_name,
            "middle_name" : item.middle_name,
            "last_name" : item.last_name,
            "second_last_name" : item.second_last_name,
            "suffix" : item.suffix,
            "date" : item.date,
            "last_four_social" : item.last_four_social,
            "residential_address" : item.residential_address,
            "shipping_address" : item.shipping_address,
            "apt_unit1" : item.apt_unit1,
            "apt_unit2" : item.apt_unit2,
            "address_nature": item.address_nature
        }
        return JsonResponse({"message": data})

@csrf_exempt
def get_ieh(request,id):
    if request.method=='GET':
        item = ChatTracker.objects.get(chatid = id)

        return JsonResponse({"ieh":item.iehBool})

@csrf_exempt
def submit_info(request, id):
        items = ChatTracker.objects.filter(chatid=id)
        if len(items) == 0:
            ChatTracker(chatid=id).save()

        #return HttpResponse("<h1>Invalid User ID</h1>")
    
        item = items.first()
        if request.method == 'GET':
            if item.form_filled:
                return HttpResponse("<h1>Submitted :) </h1>")
            else:
                return render(request, 'root/index.html', {'id': id})
        if request.method == 'POST':
            program_value = request.POST['program_value']
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            last_name = request.POST['last_name']
            second_last_name = request.POST['second_last_name']
            suffix = request.POST['suffix']
            toggleaddress = 'toggleaddress' in request.POST.keys()
            apt_unit1 = request.POST['apt_unit1']
            apt_unit2 = request.POST['apt_unit2']
            address_nature = request.POST['address_nature']
            shipping_address = request.POST['shipping_address']
            residence_address = request.POST['residence_address']
            zipcode = request.POST['zipcode']
            last_four_social = request.POST['last_four_social']
            month = request.POST['month']
            day = request.POST['day']
            year = request.POST['year']
            date = month+"-"+day+"-"+year

            item.program = program_value
            item.first_name = first_name
            item.last_name = last_name
            item.middle_name = middle_name
            item.second_last_name = second_last_name
            item.suffix = suffix
            item.last_four_social = last_four_social
            item.address_nature = address_nature
            item.date = date
            if toggleaddress is False:
                item.apt_unit1 = apt_unit1
                item.residential_address = residence_address
            else:
                item.apt_unit2 = apt_unit2
                item.shipping_address = shipping_address
                item.form_zip_code = zipcode

            item.form_filled = True
            item.save()


            return HttpResponse("<h1>Submitted :) </h1>")

@csrf_exempt
@xframe_options_exempt
def submit_form(request):
    """
    Send request to Zapier and clear database
    """
    if request.method == "POST":
        user_id = request.POST['user_id']  # Save User ID
        user = ChatTracker.objects.get(chatid=user_id)  # Find user by ID
        url = "https://hooks.zapier.com/hooks/catch/" + str(user.zap_acct) + "/" + str(user.zap_name) + "/"  # Create Zapier URL
        payload = {
            "user_id": str(request.POST['user_id']),
            "ieh": user.iehBool
        }
        response = requests.post(url,data=payload)  # Make Request

        for index in range(0, int(user.sequence_count)):  # Count all sequences in database
            sequence = Sequence.objects.get(sequence_id=str(user_id)+str(index))
            sequence.delete()  # Clear

        #user.delete()  # Clear User

        return render(request, "root/thanks.html")
@csrf_exempt
@xframe_options_exempt
def disclosure(request, user_id):
    """
    Render the disclosures HTML page
    """
    user = ChatTracker.objects.get(chatid=user_id)  # Get user by ID

    payload = {  # Form request data
        'Token': user.token,
        'PackageID': user.PackageId,
        'ResidenceState': user.ResidenceState,
        'TribalResident': user.TribalResident,
        'EligibilityProgram': user.EligibiltyPrograms
    }
    response = requests.post(
        "https://lifeline.cgmllc.net/api/v2/disclosuresconfiguration",headers={"Content-Type": "application/x-www-form-urlencoded"},data=payload)
    response_json = response.json()
    sequence_count = 0
    sequence_list = []
    for key in response_json['DisclosureItems']:
        sequence_count += 1
        sequence = Sequence(sequence_id=str(user_id)+str(key['Sequence']))  # Create record
        sequence.save()  # Save record

        sequence.type = key['Type']  # Update record fields
        sequence.text = key['Message']
        sequence.save()  # Save record

        sequence_list.append(sequence)  # Compile all sequences

    user.sequence_count = sequence_count
    #user.ieh = str(response_json['CaptureIehForm']).lower()  # Update User fields
    user.iehBool = str(response_json['CaptureIehForm'])  # Update User fields
    user.save()

    context = {
        "sequences": sequence_list,
        "user_id": user_id
    }

    return render(request, "root/start.html", context)


@csrf_exempt
def post_entry(request):
    """
    Receive a POST request and create a new record for the User model using the request data
    """
    if request.method == 'POST':
        user_id = request.POST['user_id']  # Get Data
        token = request.POST['token']
        package_id = request.POST['package_id']
        state = request.POST['state']
        benefit_code = request.POST['benefit_code']
        tribal = request.POST['tribal']
        zap_acct = request.POST['zapAcct']
        zap_name = request.POST['zapName']

        user = ChatTracker(chatid=user_id)  # Create record
        user.save()  # Save record

        user.token = token  # Update record fields
        user.PackageId = package_id
        user.ResidenceState = state
        user.TribalResident = tribal
        user.benefit_code = benefit_code
        user.zap_acct = zap_acct
        user.zap_name = zap_name
        user.save()  # Save record

        return HttpResponse({'Status': 200})  # Return success response
    else:
        return HttpResponse({'Status': 403})  # Return forbidden response
