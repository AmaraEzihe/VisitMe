from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Staff,Visitors,VisitorPhoto,VisitorQRCode
from datetime import date
import time
from django.template.loader import render_to_string
from visitme.utility.visitorid import visitoridgen
from visitme.utility.visitationdurationgenerator import durationgenerator,format_timedifference
from visitme.utility.qrcodegenerator import generate_qrcode
import base64
from datetime import datetime, date
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  

# Create your views here.
def landing(request):
    return render(request, 'visitme/Landing.html')

def CheckIn(request):
    staff = Staff.objects.all()
    
    if request.method == 'POST':
     try:
      FirstName =  request.POST.get('first_name') 
      LastName =  request.POST.get('last_name') 
      EmailAddress =  request.POST.get('email') 
      Phoneno =  request.POST.get('phone_number') 
      Occupation =  request.POST.get('occupation') 
      Address =  request.POST.get('address') 
      WhoToSee =  request.POST.get('who_to_see') 
      Reason =  request.POST.get('reason') 
      if Phoneno.isdigit == True or len(Phoneno) == 11:
              Phoneno = '+234'+Phoneno[1:]
              if Phoneno and FirstName and LastName and WhoToSee and Reason:
                 firstName = FirstName.strip().capitalize()
                 lastName = LastName.strip().capitalize()
                 consent = 'Y'
                 fullname = firstName +" "+lastName
                 
                 
                 CheckIntime = time.strftime("%H:%M", time.localtime())
                 CheckIndate = date.today()
                 
                 vid = visitoridgen()

                 visitor = Visitors(
                           VisitorNo=vid,
                           FirstName = firstName,
                           LastName = lastName,
                           FullName = fullname,
                           EmailAddress = EmailAddress,
                           Phoneno = Phoneno,
                           Occupation = Occupation,
                           Address = Address,
                           WhoToSee = WhoToSee,
                           ReasonForVisit = Reason,
                           Consent = consent,
                           CheckinTime = CheckIntime,
                           CheckinDate = CheckIndate 
                       )
                 visitor.save()
                 messages.success(request, "Record Saved Successfully")
                 return redirect('checkindets',visit_id=visitor.id)
              else:
                  messages.warning(request, "Provide data for the inputs marked red") 
      else: 
              messages.error(request, "Invalid Phonenumber") 
      
     except Exception as e:
        print(e)
        messages.error(request, "An Error Occured while saving records")

    return render(request, 'visitme/CheckinForm.html',{"staffs":staff})

def CheckInDetails(request,visit_id):
    try:
        visitid = Visitors.objects.get(id=visit_id)
        return render(request, 'visitme/CheckinDetails.html', {'visit': visitid})
    except Visitors.DoesNotExist:
       return render(request, 'visitme/404page.html')

def VisitorsPass(request,visitor_id):
    try:
      visitinfo = Visitors.objects.get(id=visitor_id)
      visitphoto = VisitorPhoto.objects.filter(visitorid=visitinfo.id).first()
      photo_base64 = None

      #getting the visitor's image to add to the front end
      if visitphoto and visitphoto.photo:
          photo_base64 = base64.b64encode(visitphoto.photo).decode('utf-8')
      #print(visitinfo.CheckinDate,visitinfo.EmailAddress,visitinfo.FullName)
      checkindate = str(visitinfo.CheckinDate)
      checkintime = str(visitinfo.CheckinTime)

      #data to be put in the qrcode
      qrdata = "VISITOR "+visitinfo.VisitorNo +" INFORMATION\nVISITOR NAME: "+visitinfo.FullName+"\nVISITOR PHONENUMBER: "+visitinfo.Phoneno +"\nVISITOR EMAIL: "+visitinfo.EmailAddress+"\nVISITOR OCCUPATION: "+visitinfo.Occupation+"\nVISITOR WHO-TO-SEE: "+visitinfo.WhoToSee+"\nVISITOR REASON-FOR-VISIT: "+visitinfo.ReasonForVisit+"\nVISITOR CHECKINDATE: "+checkindate+"\nVISITOR CHECKINTIME: "+checkintime

      #put the data in the qrcode and generate it
      qr_blob = generate_qrcode(qrdata)
  
      visitor = get_object_or_404(Visitors, id=visitor_id)
      VisitorQRCode.objects.create(visitor=visitor, qrcode=qr_blob)
  
      #qrcode to be added to frontend
      base64_img = base64.b64encode(qr_blob).decode('utf-8')

      return render(request, 'visitme/VisitorPass.html',{"visit":visitinfo,"visitphoto": visitphoto,"photo_base64": photo_base64,"qrcode":base64_img})
    except Visitors.DoesNotExist:
       return render(request, 'visitme/404page.html')


def PageNotFound(request):
    return render(request, 'visitme/404page.html')

def PhotoPage(request,visitor_id): 
   #basically checking if the id exists or not
   try:
       visitor = get_object_or_404(Visitors, id=visitor_id)
       return render(request, 'visitme/image.html', {"visitor": visitor})
   except Exception as e:
       return render(request, 'visitme/404page.html')

@csrf_exempt
def Visitor_Photo(request,visitor_id):
     if request.method == "POST":
      try:
        data = json.loads(request.body)
        image_data = data.get("image")

        # Remove the "data:image/png;base64," prefix
        format, imgstr = image_data.split(';base64,') 
        image_bytes = base64.b64decode(imgstr)

        #CHECK IF THERE IS ALREADY AN IMAGE FOR THAT VISITOR
        if VisitorPhoto.objects.filter(visitorid=visitor_id).exists():
            messages.error(request, "Error Occurred: Photo already exists for this visitor.")
            return JsonResponse({"status": "error", "message": "Photo already exists"})
        else: 
           #when there is no image for that visitor, it creates one
           visitor = get_object_or_404(Visitors, id=visitor_id)
           # Save to DB
           VisitorPhoto.objects.create(visitorid=visitor,photo=image_bytes)
   
           return JsonResponse({"status": "success", "redirect_url": f"/visitorspass/{visitor.id}"})
      except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def SendMail(request,visitor_id):
    visitinfo = Visitors.objects.get(id=visitor_id)
    if visitinfo.VisitationDuration is None:
       subject = 'Your Visitme Details 🎉'
       #fall back message incase html template fails
       message = f'Hi {visitinfo.FullName}, thanks for joining our platform!'
       #Html template that will be sent to user
       try:
         html_message = render_to_string(
             'visitme/EmailTemplate.html',
             {'visitor': visitinfo}
         )  
       except:
           messages.error(request, "An error occured")
       try:
           send_mail(
               subject=subject,
               message=message,  # Plain text fallback
               from_email=settings.DEFAULT_FROM_EMAIL,
               recipient_list=[visitinfo.EmailAddress],
               html_message=html_message,  
               fail_silently=False,
           )
           message = f"Email sent to {visitinfo.EmailAddress}"
           messages.success(request, message)
           return redirect('landing')
       except Exception as e:
           print(e)
           message2 = f"Email failed to send at this time"
           messages.error(request, message2)
           return redirect('landing')  
    else:
        error = f"{visitinfo.FullName} has already been checked out"
        messages.error(request,error )
        return redirect('landing')


def CheckOut(request):
     if request.method == 'POST':
         try:
             Vid =  request.POST.get('visitor_id') 
             visitor = Visitors.objects.get(VisitorNo = Vid)
             if visitor:
                 if visitor.VisitationDuration is None:
                   return redirect('checkoutdetails',visitor_id=visitor.id)
                 else:
                   error = f"{visitor.FullName} has already been checked out"
                   messages.error(request,error )
                   return redirect('landing')
             else:
                 messages.error(request, "Visitor does not exist") 
         except Exception as e:
             print(e)
             messages.error(request, "Visitor does not exist")
     return render(request,'visitme/CheckOut.html')

def CheckOutDetails(request, visitor_id):
    visitor = get_object_or_404(Visitors, id=visitor_id)

    # Prevent double checkout
    if visitor.VisitationDuration:
        messages.error(request, f"{visitor.FullName} has already been checked out")
        return redirect("landing")

    # Calculate duration
    checkin_str = f"{visitor.CheckinDate} {visitor.CheckinTime}"
    checkout_time = datetime.now()
    duration = format_timedifference(durationgenerator(checkin_str, checkout_time))

    # Save checkout info
    visitor.CheckoutTime = checkout_time
    visitor.VisitationDuration = duration
    visitor.save()

    # Prepare email
    subject = "Thank You for Visiting 🎉"
    plain_message = f"Hi {visitor.FullName}, thanks for joining our platform!"
    html_message = render_to_string("visitme/EmailTemplate2.html", {"visitor": visitor})

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[visitor.EmailAddress],
            html_message=html_message,
            fail_silently=False,
        )
        messages.success(request, f"Email sent to {visitor.EmailAddress}")
    except Exception as e:
        print(f"Email error: {e}")
        messages.error(request, "Email failed to send at this time")

    return render(request, "visitme/CheckOutDetails.html", {"visit": visitor})
