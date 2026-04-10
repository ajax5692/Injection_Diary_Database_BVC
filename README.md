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
Before running the synchronization, ensure you download the follwing softwares:  
1. OneDrive [(link)](https://www.microsoft.com/en-us/microsoft-365/onedrive/download)
2. Docker desktop [(link)](https://www.docker.com/products/docker-desktop/).  I have attached a screenshot for new users to figure out which docker desktop software should be downloaded.
<img src="https://github.com/ajax5692/Injection_Diary_Database_BVC/blob/docker/Python_SQL/whichDockerDesktopSoftware.png" width="600">

🚀 $\color{#f00}{\textsf{Getting Started}}$  
Please check this [manual](https://github.com/ajax5692/Injection_Diary_Database_BVC/blob/docker/Python_SQL/Run%20Manual.pdf) explaining step by step instructions for how to install and get things running.

### 🔍 Data Usage & Analytics  
Once the injection_diary.db file is updated, you can connect to it using:  
* DBeaver: Create a new SQLite connection and point it to the .db file for manual SQL queries and data editing.  
* Power BI: Use the "SQLite" or "ODBC" connector to build real-time injection tracking dashboards.  
* Python: Use pandas and sqlalchemy for advanced statistical modeling.

### 📅 Roadmap (Updates Coming Soon)  
* Visual Analytics: Integration of Matplotlib/Seaborn for automatic PDF report generation.  
* Project Tracking: Timeline views of injections per project approval number.


Maintained by: Abhrajyoti Chakrabarti, BrainVisionCenter
