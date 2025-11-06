# Criminal Record Management System

## Project Overview

The Criminal Record Management System is a web-based application built using Python (Streamlit) and MySQL.

It helps manage and organize criminal records, cases, officers, and crime data through a centralized interface.

The system provides role-based access, data visualization, and automated backup of deleted records using JSON and stored procedures.

## Key functionalities include:

Managing records for criminals, cases, crimes, officers, victims, and stations.

Linking multiple entities (e.g., cases ↔ officers, crimes ↔ criminals).

Dashboard analytics and search reports.

Automatic JSON logging and record restoration for deleted data.

## Tech Stack

Frontend: Streamlit (Python)

Backend: MySQL

Visualization: Plotly, Pandas

Automation: MySQL Triggers, Stored Procedures

Programming Language: Python 3.x

Version Control: Git + GitHub

## Normalization

The database follows Third Normal Form (3NF) to ensure data consistency and reduce redundancy.

| Normalization Rule | Implementation                                              |
| ------------------ | ----------------------------------------------------------- |
| 1NF                | Each column holds atomic (single) values.                   |
| 2NF                | All non-key attributes depend fully on the primary key.     |
| 3NF                | No transitive dependencies; derived data is not duplicated. |


This ensures efficient data organization and scalability.

## Workflow Summary

Admin/Officer logs into the Streamlit application.

Navigates through modules using the sidebar.

Admins can add, update, and delete records; officers have limited access.

When a record is deleted, a MySQL trigger logs the deleted row in JSON format.

The "Deleted Log" page displays these logs.

Admins can restore records using stored procedures.

Dashboard and reports dynamically reflect data changes.
