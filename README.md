Deployment details are contained in the deployment folder of the repository.

Deployment details are also listed below.

Project Overview
--------------------------------------------------------------------------------------------------------
The CFP Portal engine, is a system that aids fluid project proposal collection and distribution, so projects can be appropriately categorised and organised within an appropriate database. The system allows a company or reviewing committee to review projects with a RAG level and give feedback regarding the projects based on specific criteria. These projects can be accepted or rejected based on this feedback, which can be sent to universities to develop. 

We have developed two implementations, a SharePoint based one and a Django implementation. This repository contains the code for the Django based solution. 

Running Django implementation locally
--------------------------------------------------------------------------------------------------------
**Cloning repository** 
```
$ git clone https://github.com/AlexaIri/UCL-COMP0016-2020-Team-27.git
```
**Setting up django libraries** 
```
$ python -m pip install Django
$ pip install django-crispy-forms
$ pip install django-filter
$ pip install django-taggit
```

**Running the application** 
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Sharepoint Deployment
--------------------------------------------------------------------------------------------------------

Script to run for deployment:

```
1. $adminSiteUrl = "https://team29webapp-admin.sharepoint.com" (Admin puts in their own
Sharepoint value)

2. Connect-SPOService $adminSiteUrl (Needed for login)

3. $siteScriptFile = "C:\Users\hemil\Desktop\cfpportal.json" (Directory of the script)

4. $webTemplate = "64"

5. $siteScriptTitle = "CFP Portal"

6. $siteDesignTitle = "CFP Portal"

7. $siteDesignDescription = "Team 27 Sharepoint Deployment"

8. $siteScript = (Get-Content $siteScriptFile -Raw | Add-SPOSiteScript -Title $siteScriptTitle) | Select -First 1 Id

9. Add-SPOSiteDesign -SiteScripts $siteScript.Id -Title $siteDesignTitle -WebTemplate $webTemplate -Description $siteDesignDescription

10.  Using siteId generated by running step 9:
(This deletes the site design and this step must be run once the site is deployed)
Remove-SPOSiteDesign -Identity $siteDesignId
```
The site script file is contained in the google drive link below, as well as the relevant power automate flows and some videos guiding you through the set up. There are three flows exported as zips: the project proposal flow, the feedback flow and the approval flow. The videos will guide you to import these flows as well as set up the site. The site script will create the lists for you, however the styling of the site must be done by you afterwards.

You should watch the 'setting up the site' video first, and then the set up the flows.

https://drive.google.com/drive/folders/1qwu_olDBiciilCAbnHcX4YiU-SN6IpJV?usp=sharing

Link to duplicate form: https://forms.office.com/Pages/ShareFormPage.aspx?id=_oivH5ipW0yTySEKEdmlwuaS2kBwR75BhHpYlnK_ZSNUOTMzSEY2WVlMVTZNTk9WM0kwQzBMREU5Si4u&sharetoken=uxspDoRNmVON9e0RaLUW

-----------------------------------------------------------------------------------------------------------
Django Deployment
--------------------------------------------------------------------------------------------------------
In order to deploy the Django web portal properly, open two bash terminals (one for the local server and one for the remote) - the commands will be alternative. 

Set up a LINODE account (we used Linode for our cloud computing and web hosting service). 

The IP address of the REMOTE website can be found in the Network tab under the IP addresses or via the SSH Access.

We will use Ubuntu for the operating system needed to deploy the web portal.  
 The series of instructions and their explanations are provided step-by-step in the 
Django Deployment Manual.


Link to django depoloyment manual: https://drive.google.com/file/d/1HE7sEck8U8Ettj-MG44KTRZqdjaGRs6M/view?usp=sharing

