from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import smtplib



from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from EncryptDecrypt.read_email_user import read_email1, getconnection, \
    disconnect, downloaddata, writetoDict


# Create your views here.
def home(request):
    return render(request,"login.html",{})

def viewlogin(request):
    return render(request,"login.html",{})
def viewRegister(request):
    return render(request,"index.html",{})
def viewSentMail(request):
    mails=dict()
    datalist=list()
    conn=getconnection(request.session["username"], request.session["password"])
    ret = read_email1(conn,'[Gmail]/Sent Mail')
    for mailsdata in ret:
        mails["subject"]=mailsdata[0]
        mails["from"]=mailsdata[1]
        mails["mailtext"]=" ".join(mailsdata[3])
        if mailsdata[4]:
            mails["attachment"]=mailsdata[4]
        else:
            mails["attachment"]="None"
        datalist.append(mails.copy())  
    return render(request,"sentMail.html",{"mails":datalist,"user":request.session['user']})
def viewTrash(request):
    mails=dict()
    datalist=list()
    conn=getconnection(request.session["username"], request.session["password"])
    ret = read_email1(conn,'[Gmail]/Trash')
    for mailsdata in ret:
        mails["subject"]=mailsdata[0]
        mails["from"]=mailsdata[1]
        mails["mailtext"]=" ".join(mailsdata[3])
        if mailsdata[4]:
            mails["attachment"]=mailsdata[4]
        else:
            mails["attachment"]="None"
        datalist.append(mails.copy()) 
    return render(request,"trash.html",{"mails":datalist,"user":request.session['user']})

@csrf_exempt
def register(request):
 
    p=User.objects.create_user(email=request.POST.get('Email'),password=request.POST.get('pass', ''),username=request.POST.get('user', ''),is_active=1)
    p.save()
    return render(request,"login.html",{})

def downloader(request,file=None):
    if file=="None":
        return HttpResponse('sorry nothing to download')
        
    conn=getconnection(request.session["username"], request.session["password"])
    data=downloaddata(conn,file)
    return HttpResponse('File Downloaded to local folder and the message decoded as {}'.format(data))
  
def sendmail(request):
    to=request.POST.get('to')
    sender=request.POST.get('subject')
    message=request.POST.get('final_span')
    writetoDict(message)
    print to,sender,message
    recipients = [to] 
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = sender
    msg['From'] = request.session["username"]
    msg['Reply-to'] = request.session["username"]
    from enc import encrypt
    encrypt(10,message)
    
    msg.preamble = 'Multipart massage.\n'
     
    part = MIMEText("Hi, please find the attached file")
    msg.attach(part)
     
    part = MIMEApplication(open(str("new_songs.mid"),"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=str(len(message)))
    msg.attach(part)
     

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(request.session["username"],request.session["password"])
     
    server.sendmail(msg['From'], emaillist , msg.as_string())

    return HttpResponse('mail send with attachment')

def login(request):

    mails=dict()
    datalist=list()
    user=request.POST.get('username', '')
    Password=request.POST.get('password', '')
    request.session['user']=user
    data=User.objects.filter(username=user)
    for user in data:
        gmail_user=user.email
    import time
    request.session["username"]=gmail_user
    
    request.session["password"]=Password
    datatime=time.strftime("%H:%M:%S")
    conn=getconnection(gmail_user, Password)
    
    ret = read_email1(conn,'INBOX')
  
    for mailsdata in ret:
        mails["subject"]=mailsdata[0]
        mails["from"]=mailsdata[1]
        mails["mailtext"]=" ".join(mailsdata[3])
        if mailsdata[4]:
            mails["attachment"]=mailsdata[4]
        else:
            mails["attachment"]="None"
        datalist.append(mails.copy())   
    seo_specialist = authenticate(username=user, password=Password)
    if seo_specialist:
        print seo_specialist
        django_login(request,seo_specialist)
       
        return render(request,"inbox.html",{"mails":datalist,"user":user,"time":datatime})
    return render(request,"index.html",{})


def inbox(request):
    mails=dict()
    datalist=list()
    conn=getconnection(request.session["username"], request.session["password"])
    ret = read_email1(conn,'INBOX')
    for mailsdata in ret:
        mails["subject"]=mailsdata[0]
        mails["from"]=mailsdata[1]
        mails["mailtext"]=" ".join(mailsdata[3])
        if mailsdata[4]:
            mails["attachment"]=mailsdata[4]
        else:
            mails["attachment"]="None"
        
        datalist.append(mails.copy())   
    return render(request,"inbox.html",{"mails":datalist,"user":request.session['user']})


def viewCompose(request):
    return render(request,"compose.html",{})
def logout(request):
    
    
    conn=getconnection(request.session["username"], request.session["password"])
    disconnect(conn)
    django_logout(request)
    return render(request,"login.html",{})



