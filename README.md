# Injection Diary Database System  

An automated pipeline for synchronizing a local SQLite relational database with a cloud-based Microsoft Excel "Injection Diary." This system allows for structured data management, replacing flat Excel files with a robust SQL backend suitable for Python analytics, DBeaver exploration, and Power BI dashboards.

> [!WARNING]
> PLEASE MAKE SURE YOU ARE $\color{#f00}{\textsf{DOWNLOADING THE BRANCH LABELLED AS 'docker'}}$ AND NOT THE 'main' BRANCH!!

### 📊 Database Architecture
The system transforms flat Excel data into a normalized relational database consisting of five core tables:

* animals: The central hub (ID, sex, arrival data).  
* owners: Research staff and animal owners.  
* projects: Project names and official approval numbers.  
* injections: Specific surgical data, vectors used, and quantities.  
* housing_and_status: Current location (box number) and animal state.  


### 🛠 Prerequisites
Before running the synchronization, ensure your environment meets the following requirements:  
1. OneDrive / SharePoint: You must have the official Injection diary.xlsx synced to your local machine.  
2. Python 3.10+: Ensure Python is installed and added to your system PATH.  
3. Virtual Environment: It is recommended to use the provided my_venv setup to manage dependencies.  

🚀 $\color{#f00}{\textsf{Getting Started}}$  
1. Sync the Data Source
Ensure the source Excel file is locally available on your system.
Example Path: C:\Users\YourUserName\OneDrive - Femtonics Kft\Documents - 2pteam\Tables\Injection diary.xlsx

2. Clone the Repository
Download this repository to your local machine:

```
Bash
git clone https://github.com/YourUsername/Injection_Diary_Database_BVC.git
cd Injection_Diary_Database_BVC/Python_SQL
```

3. Configure the File Path
Open update_DB.py and update the excel_path variable with your specific Windows username:
```
Python
excel_path = r"C:\Users\YOUR.NAME\OneDrive - Femtonics Kft\Documents - 2pteam\Tables\Injection diary.xlsx"
```  
4. Run the Synchronization
Simply double-click the provided batch file:
run_sync.bat

This script will:  
1. Activate the Python virtual environment.  
2. Parse the latest data from the Excel sheet.  
3. Update injection_diary.db with fresh records.  

### 🔍 Data Usage & Analytics  
Once the injection_diary.db file is updated, you can connect to it using:  
* DBeaver: Create a new SQLite connection and point it to the .db file for manual SQL queries and data editing.  
* Power BI: Use the "SQLite" or "ODBC" connector to build real-time injection tracking dashboards.  
* Python: Use pandas and sqlalchemy for advanced statistical modeling.

### 📅 Roadmap (Updates Coming Soon)  
* Docker based container so that the user does not need to install separate softwares or libraries. It will be a ready to use package once the docker image is downloaded.  
* Visual Analytics: Integration of Matplotlib/Seaborn for automatic PDF report generation.  
* Project Tracking: Timeline views of injections per project approval number.

> [!NOTE]
> 🛠 Troubleshooting  
* FileNotFoundError: Double-check the path in update_DB.py. Use the "Copy as Path" feature in Windows Explorer to ensure the username and folder names are exact.  
* UNIQUE constraint failed: The database prevents duplicate animal IDs. Ensure the Excel sheet does not have duplicate entries for the same animal number.  
* ModuleNotFoundError: Run pip install -r requirements.txt within your virtual environment to ensure all libraries (pandas, sqlalchemy, openpyxl) are present.

Maintained by: [Abhrajyoti Chakrabarti, BrainVisionCenter]
