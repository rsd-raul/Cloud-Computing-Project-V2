# Cloud-Computing-Project w. Python v2

Description:

    This project objective is to design a simple application or service using Google App Engine and it's Datastore
    system, in this case implemented with the recommended Blobstore service.
    Another important feature is to construct the website dynamically using only Python and GAE, and not only that
    but also referencing static files such as CSS ones to directly apply styling to the webpage.

    As this is a education-oriented project, code will be explained for better comprehension.

Libraries & SDK:

    Google App Engine SDK.

Setup to access the code and run on localhost:

    Download and install the Google App Engine SDK.

    Select file > open on PyCharm and find the project.

    Hit run and open "localhost:8080" on your browser.

Menus & actions:

    - Upload file feature that stores files in the GAE datastore.
        The filename, format and a timestamp should be recorded. 3.5%
    - Download file feature to retrieve a file from the datastore and save to local disk.

    - Main page where a list of all uploaded files
        - Timestamp and filename is displayed for each item stored.
        - Clicking on a checkbox (a file at a time) and pressing “download” will offer the file to download.
        - Upload feature available on the same page.