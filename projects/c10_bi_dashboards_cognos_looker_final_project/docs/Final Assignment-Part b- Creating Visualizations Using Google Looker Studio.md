![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0130EN-SkillsNetwork/images/SN_web_lightmode.png)

# Hands-on Lab: Creating Visualizations Using Google Looker Studio

**Estimated time needed:** 1hr 15 mins

In this lab, you will create some visualizations and add them to a dashboard using Google Looker Studio.

## Software Used in this Lab

The hands-on lab will use the free version of Google's Looker Studio

## Dataset Used

The dataset used in this lab comes from the **IBM Accelerator Catalog** and can be downloaded from [here](https://accelerator.ca.analytics.ibm.com/bi/?utm_source=skills_network&utm_content=in_lab_content_link&utm_id=Lab-IBMSkillsNetwork-DV0130EN-Coursera&perspective=authoring&pathRef=.public_folders%2FIBM%2BAccelerator%2BCatalog%2FContent%2FDAT00142&id=i22898C2A4DD748F79E0FC2BD017F4FE8&objRef=i22898C2A4DD748F79E0FC2BD017F4FE8&action=run&format=HTML&cmPropStr=%7B%22id%22%3A%22i22898C2A4DD748F79E0FC2BD017F4FE8%22%2C%22type%22%3A%22reportView%22%2C%22defaultName%22%3A%22DAT00142%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D "here") .

The Terms of use for such are located at [https://developer.ibm.com/terms/ibm-developer-terms-of-use/](https://developer.ibm.com/terms/ibm-developer-terms-of-use/).

We are using a modified subset of that dataset for the lab, so to follow the lab instructions successfully, please use the dataset provided with the lab, rather than the dataset from the original source.

## Assignment Scenario

As a regional manager for a chain of car dealerships you need to build out a dashboard to allow you to understand your sales and service departments.

## Accessing the Dataset for the Google Looker Lab of the Final Assignment

---

You need to download this dataset (all files) and **import** them into your Google Drive.

- Upload all these files in your drive. Use the _Google Sheets_ connector in Looker Studio to connect with these Excel worksheets to add data into your report
    
- In case it doesn't show the files while adding, then, open a blank Google Sheet in your drive.
    
- Click on **Import** from the **File** menu, and then select the relevant file from your drive.
    

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_1.png)

- Then you can use the _Google Sheets_ connector in Looker Studio to connect with these Excel worksheets to add data into your report. Select the data sheets one by one and add them to your report or create a data source.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_4.png)

---

Alternatively you can use the **CSV** versions of these files, which can be downloaded from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/labs/v2/Looker_Dataset.zip "here").

## Guidelines for the Submission

Use the course videos and hands-on lab on _Creating Visualizations and Dashboards with Google Looker Studio_ to help you complete the following tasks:

Create report with two pages as follows:

- One page with 5 different visuals to develop a **Sales** Dashboard. Rename page one as **Sales**. You may display the charts on this page as below:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_7.png)

  

- One page with 4 different charts to represent a **Service** dashboard- rename this page to **Service**. You may display the charts on this page as below:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_8.png)

  

Capture the following KPI metrics as visualizations:

TASK 1: On the **Sales** dashboard, capture the following KPI metrics:

- In the first small rectangle **(Panel 1)**, capture **Profit** (formatted to 1 decimal place in millions of US dollars)
- In the second small rectangle **(Panel 2)**, capture **Quantity sold**
- In the third small rectangle **(Panel 3)**, capture **Quantity sold by model** (as a **bar chart**)
- In the fourth small rectangle **(Panel 4)**, capture **Average quantity sold**

  

TASK 2: On the **Sales** dashboard in the large rectangle **(Panel 5)**, display _Profit_ by _Dealer ID_ as a **column chart**, sorted in ascending order.

  

TASK 3: On the **Service** dashboard, capture the following KPI metrics as visualizations:

- In the top left area **(Panel 1)**, capture the number of recalls per model of car (as a **column chart**).
- In the top right area **(Panel 2)**, capture the customer sentiment by comparing positive, neutral, and negative reviews (as a **treemap**).
- In the bottom left area **(Panel 3)**, capture the quantity of cars sold per month compared to the profit (as a **combo chart** from line section).
- In the bottom right area **(Panel 4)**, capture the number of recalls by model and affected system (as a **pivot table with a heatmap**). This will help us understand if there are any outliers for a given model or a specific system.

---

NOTE: Include suitable chart titles and labels for x and y axis.

---

Task 4: To export your dashboard as a PDF, follow instructions below:

- On the top right corner of your report editor, click on the small triangle of the **Share** button. Then select **Download report**.
    
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_5.png)
    
      
    
- On the pop up window _Download as PDF_, click on the _All pages_ radio button. Choose from additional options and then click on _download_.
    
    ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_6.png)
    
      
    
- Save the PDF file on your local machine to any location you like (preferably your **Downloads** folder) for later upload and submission to the coursera platform.
    
- Your report may look like this:
    

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_9.png)

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0130EN-Coursera/images/fa_10.png)

## Author(s)

- [Dr. Pooja](https://www.linkedin.com/in/p-b28802262)

### © IBM Corporation. All rights reserved.