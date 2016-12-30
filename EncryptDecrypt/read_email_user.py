

def main():
    pass

if __name__ == '__main__':
    main()


import sys
from datetime import datetime, timedelta
import os
import re
import imaplib
import email


# # Read only emails from last 3 days
no_days_query = 5

server = "imap.gmail.com"
port_num = 993
import sys
 
dictfile = "D:\Django Projects\MusicalCryptography\EncryptDecrypt\words"
 
def get_words(text):
    """ Return a list of dict words """
    return text.split()
     
def writetoDict(word):
    with open(dictfile,"a") as f:
        f.write(word) 
def get_possible_words(words,jword):
    """ Return a list of possible solutions """
    possible_words = []
    jword_length = len(jword)
    for word in words:
        jumbled_word = jword
        if len(word) == jword_length:
            letters = list(word)
            for letter in letters:
                if jumbled_word.find(letter) != -1:
                    jumbled_word = jumbled_word.replace(letter,'',1)
            if not jumbled_word:
                possible_words.append(word)
    return possible_words       
             
def getconnection(username,password):
    conn = imaplib.IMAP4_SSL(server, port_num)
    conn.login(username, password)
    return conn
def disconnect(conn):
    conn.logout()
    
def downloaddata(conn,filenameto):
    totals=list()
    conn.select()

    #Check status for 'OK'
    status, all_folders = conn.list()

#     folder_to_search = 'INBOX'


    #Check status for 'OK'
    status, select_info = conn.select('INBOX')

    if status == 'OK':
        today = datetime.today()
        cutoff = today - timedelta(days=no_days_query)
        search_key =" after:" + cutoff.strftime('%Y/%m/%d')
        status, message_ids = conn.search(None, 'X-GM-RAW', search_key)
        for ids in message_ids[0].split():
            status, data = conn.fetch(ids, '(RFC822)')

            email_msg = email.message_from_string(data[0][1])
            
            for part in email_msg.walk():
                if part.get_content_maintype() == 'multipart': continue
                if part.get('Content-Disposition') is None: continue

    
            #save the attachment in the program directory
                filename = part.get_filename()
                if filenameto==filename:
                    fp = open(filename, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    from enc import decrypt
                    print filename
                    message=decrypt(10,filename,int(filename))
                    print message
                    words = get_words(file(dictfile).read())
                    jumbled_word = message
                    words = get_possible_words(words,jumbled_word)
                    print "possible words :"
                    print '\n'.join(words)
                    print '%s saved!' % filename
                    return ''.join(words)
                

    
        
def getAttachment(conn,fromdata):
    attachmentlist=list()
    totals=list()
    today = datetime.today()
    cutoff = today - timedelta(days=no_days_query)
    search_key =fromdata+" after:" + cutoff.strftime('%Y/%m/%d')
    status, message_ids = conn.search(None, 'X-GM-RAW', search_key)
    for ids in message_ids[0].split():
        status, data = conn.fetch(ids, '(RFC822)')

        email_msg = email.message_from_string(data[0][1])
            
        for part in email_msg.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            attachmentlist.append(part.get_filename())
    
#             #save the attachment in the program directory
#                 filename = part.get_filename()
#                 fp = open(filename, 'wb')
#                 fp.write(part.get_payload(decode=True))
#                 fp.close()
#                 print '%s saved!' % filename
    return attachmentlist


def getMails(email_msg):
    mails=list()
    for part in email_msg.walk():
        if part.get_content_type() == 'text/plain':
            email_content = part.get_payload(decode=True) # prints the raw text
            mails.append(email_content)
    return mails
            #TODO :
            #process_email() #Delete, Mark as Spam, Forward it
            #TODO :
            #print email_content
    
def read_email1(conn,folder_to_search):
    newdata=None
    Total=list()
    fromdata=list()
    conn.select()

    #Check status for 'OK'
    status, all_folders = conn.list()

#     folder_to_search = 'INBOX'


    #Check status for 'OK'
    status, select_info = conn.select(folder_to_search)

    if status == 'OK':
        today = datetime.today()
        cutoff = today - timedelta(days=no_days_query)

#         from_email = 'projects.fleming@gmail.com'
        #from_email = 'contact@sapnaedu.in'

        search_key =  " after:" + cutoff.strftime('%Y/%m/%d')

        status, message_ids = conn.search(None, 'X-GM-RAW', search_key)


        for id in message_ids[0].split():
            status, data = conn.fetch(id, '(RFC822)')

            email_msg = email.message_from_string(data[0][1])
            

            #Print all the Attributes of email message like Subject,
##            print email_msg.keys()

            subject = email_msg['Subject']
            sender_email =  email_msg['From']
            sent_to_email =  email_msg['To']
            attachment=getAttachment(conn,subject)
            mails=getMails(email_msg)
#             fromdata.append(subject)
            Total.append([subject,sender_email,sent_to_email,mails," ".join(attachment)])
            
              

    else:
        print "Error"
    return Total
    ## Search for relevant messages
    ## see http://tools.ietf.org/html/rfc3501#section-6.4.5










