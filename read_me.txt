note:
I used flask, SQLAlchemy and sqllite.

Running instructions:

	-run the python file- A database will be created, And http requests can be sent (I have attached examples in a separate postman file)

2)details for each request:

	post: 
		/newMessage: הוספת הודעה חדשה 
	get:
		/all/<sender>:    שלח <sender> מחזיר את כל ההודעות שהמשתמש   
		
		/all_unread/<sender>:   שלח <sender> מחזיר את כל ההודעות שלא נקראו שהמשתמש 
	
		/one_msg/<user>: <user> מחזיר הודעה ראשונה שקיימת עבור המשתמש 

	delete:
		/delete_owner/<user>:      <user> מוחק הודעה ראשונה שקיימת ונשלחה ע"י המשתמש

			