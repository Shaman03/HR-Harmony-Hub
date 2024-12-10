# TeamProject
PIP INSTALL 
PIP NSTALL IOS 
PIP INSTALL FLASK 
Install Flask

To use Flask, first, you need to install it:
Copy code 
pip install flask

Python file (app.py) for backend logic.
HTML templates (e.g., home.html) stored in a templates folder for frontend design.

Running the App
Run the Flask app with:

Copy code
python app.py
Open your browser and navigate to http://127.0.0.1:5000/ to see the home page
PYTHON DOWNLOAD FOR VSCODE TO GET APP.PY FILE 

SQLITE BUILT INTO VSCODE USED TO STORE DATA AND USED HASH TO SECURE PASSWORD 

How to run application within the terminal type python app.py access HTTP link 
click follow link 
browser will apear firstly with home page top right corner has three bars we click that will give choice to register if you are already a user you will log in or register if new 
username email and password 
home page payroll , leave management and employee directory 

SQLite is a small database that keeps information on your computer as a file. Small apps like our HR app are ideal for it. It has the ability to keep user information in your case, such as names, emails, and employment applications.

Simple to assemble: No server is required. It operates straight from a file. (built in to vs code )
Python-friendly: Python's built-in sqlite can be used. 

to keep the password secure we used hashing to convert the password into a scrambled, secure format example will be shown in  the database thats connected to the app (ENCRYPT THE PASSWORD SO NOT READABLE JUST USING HASH FOR THIS)
 IMPORTANT: Hashing is a one-way method of data jumble. The hash cannot be reversed to reveal the original password, even if someone manages to get into the database.

 Hashing and sqlite is important and i used it to keep the web secure as we are collecting personal data such as the user name email and password ect. 
 Hashing protects sensitive data like passwords.
SQLite efficiently stores and retrieves user data.
This make the HR app secure and functional 
