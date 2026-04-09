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
1. OneDrive: You must have the official Injection diary.xlsx synced to your local machine.
> [!IMPORTANT]
> Make sure there is a folder labelled as _'Documents - 2pteam folder'_ inside the _'OneDrive - Femtonics Kft'_ folder. If it does not exist, then visit _SharePoint -> 2pteam -> Documents_, and then click on the 'Add shortcut to OneDrive' ![](https://github.com/ajax5692/Injection_Diary_Database_BVC/blob/docker/Python_SQL/setting%20up%20the%20folder%20from%20onedrive.png) Make sure that the shortcut thus created has this name _'Documents - 2pteam'_ (rename if necessary). Go to this location _...\OneDrive - Femtonics Kft\Documents - 2pteam\Tables_ and check if the file _Injection diary.xlsx_ has a cloud logo next to it. If there is a cloud logo, then double click on the file to download a local copy of the same. Once the download is complete, the cloud logo would change to a circular white-green check mark.
2. Docker desktop [https://www.docker.com/products/docker-desktop/]

🚀 $\color{#f00}{\textsf{Getting Started}}$  
1. Sync the Data Source
Ensure the source Excel file is locally available on your system.
Example Path: C:\Users\YourUserName\OneDrive - Femtonics Kft\Documents - 2pteam\Tables\Injection diary.xlsx

2. Clone the Repository (either method can be followed)
   - Download this repository to your local machine:

      ```
      git clone https://github.com/ajax5692/Injection_Diary_Database_BVC.git
      cd Injection_Diary_Database_BVC/Python_SQL
      ```
   - Download from the github repo [https://github.com/ajax5692/Injection_Diary_Database_BVC/archive/refs/heads/docker.zip] or clone the repo $\color{#f00}{\textsf{(the docker branch!)}}$ using github desktop.

3. Install the docker desktop and run it. You may be prompted to update your Windows Subsystem for Linux. To do that, open Command Prompt on your computer and type in
```
wsl –update
```
  Once the update finish you can close the Command Prompt and restart Docker Desktop. You most likely will not be asked to restart your computer. Docker Desktop now should be properly working on your computer.  

4. In the docker desktop search for _ajax730/injection_diary_bvc_sync_ and download (or pull) it.
  
5. Run the Synchronization: Simply double-click the provided batch file _run_sync.bat_ that you will find inside the _...Injection_Diary_Database_BVC\Python_SQL_ folder. This script will:  
   - Activate the docker container.  
   - Parse the latest data from the excel sheet.  
   - Update injection_diary.db with fresh records.  

### 🔍 Data Usage & Analytics  
Once the injection_diary.db file is updated, you can connect to it using:  
* DBeaver: Create a new SQLite connection and point it to the .db file for manual SQL queries and data editing.  
* Power BI: Use the "SQLite" or "ODBC" connector to build real-time injection tracking dashboards.  
* Python: Use pandas and sqlalchemy for advanced statistical modeling.

### 📅 Roadmap (Updates Coming Soon)  
* Visual Analytics: Integration of Matplotlib/Seaborn for automatic PDF report generation.  
* Project Tracking: Timeline views of injections per project approval number.


Maintained by: Abhrajyoti Chakrabarti, BrainVisionCenter
