GNU GPL Licence V 2

This project lacks modules. So first expansion would be to break it down to models.

Unless you have the database setup it will not work. So create tables using the sql file. Change the mypass password to whatever is on your mysql database. They are on two places. It is a lame way to do that. Using database is costly for portability so the database should be either platform independent one, or xml file. Lets see which will be more efficient on next releases.


Plan for the project.
1. User adds a catagory
2. User addes entries for specific catagory.
   Entries consists of title, description, detail, tags(for search)
   Tag is future requirement. Simple regex search in title, description and details will do just fine.
3. The search result reconstructs the list based on rows matching search text.

Done till now.
1. The GUI dialog box is preety lame. The vbox did not expand well
2. The data is saved in database but still none is reselected to dialogbox for edit and delete.(It is a must in next release)
3. Data appears in listbox. Many SQL calls slows the application. So must be optimized for that.

