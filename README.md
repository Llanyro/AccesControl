# AccesControl
Manages acces of users to the system with sql and cookies<br>
Signin and login returns 2 parameters<br>
- If the action is computed ok
- The cookie that is generated for the user

This repo requieres ``` sqlite3 ```

```python
session = AccessController("users.db", True)
```
How to Login or register
```python
result, cookie = session.signin("Llanyro", "Password")
print("Signin:", (result, cookie))
print("Login:", session.login("Llanyro", "Password"))
```
How to check if is logged
```python
print(session.is_logged(cookie))
```
How to log out
```pyhton
print(session.logout(cookie))
```
You can print all database
```python
session.print_cookies()
session.printDB()
```