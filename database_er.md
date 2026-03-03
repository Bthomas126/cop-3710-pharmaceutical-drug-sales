# ER Diagram

![ER_Diagram](ER_DIRAGRAM.png)



Relational Schema
MANUFACTURER

MfrID (PK)

Name

Country

DRUG_CATEGORY

Drug_Code (PK)

Description

MfrID (FK → MANUFACTURER.MfrID)

DRUG_DETAILS

Drug_Code (PK, FK → DRUG_CATEGORY.Drug_Code)

Notes

FDA_Approval_Date

TIME_PERIOD

Date (PK)

Year

Month

Weekday

Hour

SALES

Drug_Code (PK, FK → DRUG_CATEGORY.Drug_Code)

Date (PK, FK → TIME_PERIOD.Date)

Units_Sold

DRUG_RECALL

Drug_Code (PK, FK → DRUG_CATEGORY.Drug_Code)

Recall_No (PK)

Recall_Date

Reason

Notes
