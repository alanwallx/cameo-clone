Readme
--------------------------------------
Summary:
--------------------------------------
Note: see 5 min overview: videoinstarvid-runthrough-01.webm 

The project satisfies the distinctiveness and complexity requirements:
The project allows the user to request a short video from their favourite TV, sports or movie star saying hello or birthday greetings to them or someone the user nominates. The user can sign up, pick their preferred star, send a request to the star. Once the star has uploaded the video the user is emailed to tell then that the video is ready and they can link to it or download it. Each user has an profile page where they can view all their closed and pending orders with links to videos where applicable. 

Meanwhile someone who is considered a star can set up one or more "Star Profiles" and apply to be listed on the site. If they are listed, they get an email saying that there is a request for them to consider and respond to. Stars have a profile page where they can see all pending and closed requests, and offers a solution for them to upload the video. Why would you have two star profiles? If you are a singer you would have one star profile, using your real name, whereas if you were for example a comedian with several characters, for example Sasha Baron Cohen has Ali-G and Borat, so he can set up two star profiles to cater to different audiences.

There is also an admin area where administrators can consider the star's application and approve, reject, query or ban the star profile application, depending on the merits of the star. 

I felt the project was sufficiently complex for CS50 at this stage, so I have not implemented a payment system at this point. 

--------------------------------------
Detailed description of the project:
--------------------------------------

Personas:
Customer: someone requesting a video from a star
Star: the owner or one or more star profiles
Administrator

--Typical scenario--

User browses and registers:
Once the project is running, a user, Frank, as an unknow user arrives at the site. Frank can see all the stars on the home page and the price to book each star. He can hide a star he's not interested in by clicking hide on any star.  This satisfies the javascript requirement. Frank clicks on a star and looks at thier profile. He then decides to sign up. he clicks 'Sign Up' and enters his details. An account is created and he is invited to log in. Frank logs in with his new username and password and then is able to browse the board as a logged in user. 

User books a video:
Frank clicks on a star and views the star profile. He wants to book musician Lisa Hannigan to say hello to his friend who is a big fan of Lisa Hannigan. He fills out the form and tells Lisa that his friend's 30th birthday is coming up and that he is a big fan of Lisa. He then submits the order. A payment system could be built in at this stage but it was not necessary for the purposes of fulfilling the requirements of the project. 

The form is validated and if all fields are ok then Frank gets a confirmation message telling him the booking has been made and that he can expect an email or can keep track of his orders via his dashboard. 

Star receives the booking:
Lisa gets an email telling her that someone has booked a video. She logs into he dashboard and reads the request. When she is ready Lisa takes a video of herself and uploads it on the relevant page of her dashboard.

User receives the video:
Frank recieves an email alerting him that the video is ready. He logs in and goes to his dashboard where the video can be downloaded or the link copied and shared.

User applies to become a star:
Frank is impressed with the service and thinks he would like to be a star on the platform. He is a comedian on the local scene. He clicks through to the star dashboard  and fills out the enroll form, uploading a photo of himself and detailing for the administrators why he should be considered. Upon submitting the application he is told that his application is under consideration, which he can verify if he clicks through to the star dashboard. He can make amendments to the application at this stage, for example if he forgot to include a link to his instagram page.

Administrator considers the application:
An administrator, Adam, logs into the admin dashboard and can see all the star requests. There are several status options that can be applied to an application:
Pending = a new application that has not been modified by administators
Returned = an application that was returned to the user with a request for more information
Resubmitted = an application that has been resubmitted with the requested information
Suspended = an applicaiton that has been suspended for either breaking the rules or some other infraction, and will contain a message from the admin to explain the status change
Resubmitted after suspension = an application that has been submitted with notes or info from the applicant to persuade the admin to un-suspend the star profile.
Declined = an application that has been declined by the admin because it does not meet the requirements of the platform
Resubmitted after being declined = this application will give the applicant one last attempt to persuade the administrator to admit them to the site.
Approved = application that has been approved to go live on the website.  

Adam clicks through to the star profile and sees that Frank has not filled out enough information about why he should be considered, namely he has not included his follower numbers. Adam changes the status to Returned and adds a note to Frank asking him to resubmit with the follower numbers for his social media channels. 

User resubmits the application:
Frank gets an email saying the application needs attention and he logs in and views the application. The status is noe "Returned". Upon clicking through he can see the message from the administrator and proceeds to add the relevant detail before submitting again. 

Admin approves an application:
Adam, viewing his dashboard, sees that Frank's application has been resubmitted. Adam is happy with the applicaton now and he changes the status to Approved. This immediately puts Frank's profile on the home page and it is available to be booked by other users. Frank gets an email notifying him that the applicaiton has been approved. 

--------------------------------------
What’s contained in each file
--------------------------------------

instarvid/settings.py:
Contains extra lines to handle storage of video and image files
Extra code to sen email content to console output
Styles for form package Crispy Forms


instarvid/urls.py:
Contains code to handle medial files and testing of medial files


media/images and media/videos :
contains media files uploaded by users

stars/static/css/styley.css:
contains all the CSS styles for the application. I am also using Bootstrap

stars/static/js/js.js
contains all the Javascript for the application. 
• There is a function to copy the URL for the video
• There is a function to ignore a star from the home page
I also use jQuery in the project

stars/static/facicon.ico:
The favicon icon that appears in the browser next to the URL

start/static/logo.png:
The logo for the website

stars/templates/orders/index.html:
This is the template file to create the page where the customer can see their orders

stars/templates/orders/specific_order.html:
This page shows the customer the details of a specific order, and if the video has been uploaded it displays the video and allows the customer to download or grab a link to the video.

stars/templates/stars/admindashboard.html:
This page allows the admins to get an overview of all the star profiles, see the status of star profiles and click through to a starprofile that needs attention

stars/templates/stars/create.html:
This page allows a star to create a star profile. I use crispy forms to create the forms without having to write custom form templates. The star must pick a unique username which is compared to the database to see if it's unique. 

stars/templates/stars/edit.html:
This page allows stars to edit a star profile. It also tells them the reason for any recent change to their profile status

stars/templates/stars/index.html:
The homepage of the website displays all the stars with their price and some other details. You don't need to be logged in to view

stars/templates/stars/layout.html:
This page generates the navigation (which changes based on the user being logged out / an admin / a customer and also pulls in the jQuery, JavaScript, Bootstrap and CSS

stars/templates/stars/profile.html:
This admin only page is a star profile confirmation page including the star name, price, occupation, reason for status change etc.

stars/templates/stars/staradmin.html:
This is for administrators to change the status of an order and the owner gets emailed (although we only write the email to the console for the purposes of this application). Again using crispy forms to generate the form.

stars/templates/stars/stardashboard.html:
This page shows a star all their star profiles, the status of their profiles, their video requests and the status of their video requests.

stars/templates/stars/starpage.html:
This is the individual star profile that the customer sees, and it encourages them to book this star. It allows them to book the star and is reused as the confirmation page when a star is booked. 

stars/templates/stars/upload.html:
This page enables a star to upload their video to complete the order. The customer is notified that the video has gone up. 

stars/templates/users/login.html:
A simple login page allowing the user to sign in to their account

stars/templates/users/signup.html:
A simple signup page that allows users to create an account.

stars/admin.py:
Registers the models for the Django administrator page

stars/models.py:
This page contains all the models for the database:
• Video containe the name of the video and the location of the video
• Photo contains the title of the photo and the location of the photo
• Star contains the name, price, occution, owner, username, image, application letter, status (as a list of choices) and the reason for status change (for admin use).
• Order contains price, customer, star booked, whether the order is completed, the custom message, the recipient, and who the message is from (in case it's not the customer). 
• Ignored contains the stars that are being ignored by a customer

stars/urls.py:
contains the URLs of the pages required for the application

stars/views.py:
This page contains all the logic required for the site to work.
.
First we import all the required components
.
Then we define our forms:
Order form, Video upload form, Star creation, star edit by admin.
.
Next we handle our application logic:
• The home page reners all the star profiles
• The star page renders the star's details and the Order Form for the star
• The profile page renders the star profile for admin only areas to confirm changes
• The order renders the starpage. It creates an order by capturing and sanitising the data for the recipient, customer, custom message, the username, the message from field, the star requested, price. It creates an instance of the order in the Order table with the relevant details. An email is then sent to the star (we output to the console for the sake of this demo), informing them where they should upload their video. A confirmation is returned upon successful application. In the real world a payment system would be built in at this stage.
• The starcreate function creates a star profile with an initial status of 'pending', it checks if the username already exists
• Staredit allows stars to edit their star profile. The status is automatically updated, so for example if the status was 'declined' and they edit the profile, the new status will be "resub_declined" meaning resubmitted after being declined
• staradmin is for administrators to change the status of an order, the owner gets emailed. The administrator can change any part of the application. The administrator shoudl leave a comment for the applicant to explain their decision
• specific_order is the page where a customer can view a specific order, and if the order has been fulfilled (the video uploaded) they can download the video or get a link
• orders is where a customer can see all of their orders and the status of each order
• stardashboard allows the stars to see all their star profiles and the status of each profile. They can also see their video requests and the status of each request.
• upload allows the star to upload the requested video for a particular order. The customer gets an email to notify them that the video has been uploaded. If they have already uploaded a video the video is shown
• admindashboard displays all the star profiles and their status, with links to the profile so they can modify them
• signup allows a user to register an account
• login_view allows the user to log in to the application






--------------------------------------
How to run the application
--------------------------------------
Install Django and the dependencies in the requirements.txt file. Once you run the application you should be able to browse the stars and create a new profile, where you can then contact a star to request a video message. 
If the database is included, some useful usernames and passwords:

Sacha (star owner)
xxxdddiii

Aoibhinn (star owner)
aaabbbnnn

Lisa (star owner)
lisa

tony (admin)
777uuujjj

Brian (customer / Limmy)
444xxxiii

homer (Jazzy Jeff)
PPPiii333

claire (customer)
claire

alan (the video example)
alan


--------------------------------------
Any other additional information the staff should know about your project.
--------------------------------------
It was very hard to fit into 5 minutes what this application can do. As I worked on it it became obvious that the majority of the work is for administrators to approve and manage the star profies and the appeals process. If I was to flesh it out I would build on a payment system, an option for stars to report customers, refuse a request or ask the customer for more details. A category system would also be cool because as the site gets bigger some customers might be intersted in sports stars, others in actors etc. I hope I have included everything I need to to pass. The video is a bit scrappy because of the five minute limit. I had a whole script written that I couldn't use. Thanks for your time.