from django.db import models

# Create your models here.
# class Visitors(models.Model):
#     Visitornumber = models.CharField(max_length=20)

class Staff(models.Model):
    Fullname = models.CharField(max_length=100)
    Designation = models.CharField(max_length=20, null=True,blank=True)

    def __str__(self):
        return self.Fullname
    
class Visitors(models.Model):
    CONSENT_CHECKER = {
        "Y": "Yes",
        "N": "No",
    }
    VisitorNo = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    FullName = models.CharField(max_length=100)
    EmailAddress = models.CharField(max_length=50,null=True,blank=True)
    Phoneno = models.CharField(max_length=100)
    Occupation = models.CharField(max_length=50,null=True,blank=True)
    Address = models.CharField(max_length=120,null=True,blank=True)
    WhoToSee = models.CharField(max_length=100)
    ReasonForVisit = models.TextField()
    Consent = models.CharField(max_length=1, choices=CONSENT_CHECKER)
    CheckinTime = models.TimeField()
    CheckinDate = models.DateField()
    CheckoutTime = models.DateTimeField(null=True)
    VisitationDuration = models.CharField(null=True)

    def __str__(self):
        return self.VisitorNo

class VisitorPhoto(models.Model):
    visitorid = models.ForeignKey(Visitors,on_delete=models.CASCADE,null=True, blank=True)
    photo = models.BinaryField()  # stores image as blob
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at
    
class VisitorQRCode(models.Model):
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE)
    qrcode = models.BinaryField()  # stores QR as blob
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at