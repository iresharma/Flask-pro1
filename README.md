# The Social Media Project 

My first flask (python FrameWork) project



## Implements 
  - Regitration
  - Email verification
  - Login
  - Profile Page
  - SMS Verification*
  
  
## In process
  - [x] Regitration
  - [x] Email verification
  - [x] Login
  - [x] Profile Page
  - [x] SMS verifiction
  - [ ] Database
  - [ ] Post
  - [ ] Edit/Delete/like/comment post


### Help
  - Image Upload not working
  
  
  
## About SMS Verification
  chaces are sms verfication may not work for you because I have put in my credentials up here and hence TWilio has blocked my Account.
  
  to make the SMS verification work go to https://www.twilio.com/sms
  
   - register
   - Get a twilio number 
   - Get a account SID and Auth Token
              
  Then perform the following changes in the sendSMS(uu) function of my code
     
     ``` def sendSMS(uu):
              l = open('DATA/credential.json', 'r')   --- comment this
              j = eval(l.read())                      --- comment this
              l.close()                               --- comment this

              k = open('DATA/temp.json', 'r')
              b = eval(k.read())
              k.close()

              a = open('DATA/contentSMS.txt', 'r')

              client = Client(j['twiAccSid'], j['twiAccToken'])  --- replace j['twiAccSid'],j['twiAccToken'] with <SID>, <Auth token>

              b[uu]['OTP'] = random.choice(range(100000,1000000))

              k = open('DATA/temp.json', 'w')
              json.dump(b,k)
              k.close()

              meassage = client.messages.create(
                                                  from_ ='+12512946865',
                                                  to = b[uu]['tel'],
                                                    body = '\n' + str(b[uu]['OTP']) +'\n\n Thank you'
                                          ) ```

``` Author @iresharma ``` 
