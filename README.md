# IsraFlight_Project
**מערכת לניהול חברת תעופה, המאפשרת ניהול טיסות, מטוסים, הזמנות ולקוחות. המערכת מיועדת הן למנהלי החברה והן ללקוחות**

## Architecture
### Backend (ASP.NET Core Web API)
**Development in the Visual Studio environment**
- Controllers: HTTP ניהול בקשות
- Models: ייצוג ישויות נתונים
- DbContext: ניהול התקשורת עם מסד הנתונים


### Fronted (PySide6 )
**Development in the Visual Studio Code environment**
 - Models: ייצוג מבני נתונים
 - Views: ממשקי משתמש גרפיים
 - Controllers: ניהול לוגיקת הביזנס והתקשורת בין Views ל-Models

### Database (SQL Server - Somee.com)
  - Use of cloud services for data storage

## Functionality
### Admin interface
- ניהול מלא של טיסות: הוספה, עדכון, מחיקה
- ניהול צי מטוסים: הוספת מטוסים חדשים, עדכון פרטים
- צפייה בסטטיסטיקות

### A frequent flyer interface

- רישום למשתמשים חדשים
- חיפוש והזמנת טיסות
- צפייה בהיסטוריית הזמנות
- הדפסת כרטיסי טיסה ב-PDF
  
## Service in FastAPI
**Development in the PyCharm environment**
Development of a service based on machine learning in FastAPI for predicting flight delays.

## Explanation of the running of the project
1. Run the **backend** in the Visual Studio environment
2. Run the **Predicting_flight_delays** file in the PyCharm environment
3. Run **Fronted** in the Visual Studio Code environment



