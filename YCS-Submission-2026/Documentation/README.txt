CivicEye AI

AI-Powered Public Issue Reporting & Monitoring Web Application

YCS 2026 – Young Computer Scientist Competition

National-Level School ICT Championship – Sri Lanka

⸻

1. Project Overview

CivicEye AI is an AI-powered web application designed to help citizens report and monitor public issues in their communities.

The system allows users to submit an image, select the type of public issue, provide a description, and specify the location.

The submitted report is analysed and presented with useful information such as issue priority, recommended authority, and duplicate complaint status.

The project aims to use modern web technologies and AI-assisted analysis to make public issue reporting more organized, accessible, and efficient.

⸻

2. Problems Addressed

Citizens may encounter public issues such as:
	•	Road damage
	•	Garbage problems
	•	Water leakage
	•	Street-light issues
	•	Other local public problems

Traditional reporting methods can make it difficult to organize complaints, identify repeated reports, and determine which authority should handle an issue.

CivicEye AI provides a centralized digital approach for reporting and monitoring public issues.

⸻

3. Main Features

Image-Based Reporting

Users can upload an image showing the public issue.

Issue Description

Users can provide a written description of the reported problem.

Location Capture

Users can enter a location manually or use the device’s current location.

AI-Assisted Analysis

The system processes the submitted report and provides an AI analysis result.

Priority Detection

Reports are assigned a priority level such as:
	•	Normal
	•	Medium
	•	High
	•	Emergency

Authority Recommendation

The system recommends a relevant authority based on the reported issue.

Examples:
	•	Water Leakage → Water Supply Authority
	•	Garbage Problem → Local Municipal Authority
	•	Road Damage → Road Development / Local Authority
	•	Street Light Issue → Local Authority / Electricity Provider

Duplicate Complaint Detection

The system checks whether a report with the same issue type and location has already been submitted.

Admin Dashboard

Administrators can view submitted reports, images, descriptions, locations, status, and submission time.

Multilingual Voice Input

The reporting interface provides voice-input options for:
	•	English
	•	Tamil
	•	Sinhala

⸻

4. Technology Used

Frontend
	•	HTML5
	•	CSS3
	•	JavaScript

Backend
	•	Node.js
	•	Express.js
	•	Multer
	•	CORS
	•	dotenv

Deployment
	•	Frontend: Web-based interface
	•	Backend: Railway

⸻

5. Project Structure

Frontend

Important files include:
	•	index.html – Home page
	•	report.html – Public issue reporting page
	•	ai-processing.html – AI analysis result page
	•	admin.html – Administrative dashboard
	•	login.html – Login interface
	•	citizen.html – Citizen dashboard
	•	script.js – JavaScript functionality
	•	style.css – Styling and responsive design

Backend

Important files include:
	•	server.js – Main backend server
	•	package.json – Project dependencies
	•	package-lock.json – Dependency lock file

⸻

6. How to Test the Project

Step 1 – Open the Reporting Page

Open:

report.html

Step 2 – Create a Report
	1.	Upload an image.
	2.	Select an issue type.
	3.	Enter a description.
	4.	Enter a location or use the current-location feature.
	5.	Click Submit Report.

Step 3 – View AI Analysis

The system opens:

ai-processing.html

The result displays:
	•	Issue
	•	AI Confidence
	•	Location
	•	Description
	•	Priority
	•	Recommended Authority
	•	Duplicate Complaint
	•	Status

Step 4 – Test Duplicate Detection

Submit the same issue type using the same location again.

The second submission should be identified as:

Duplicate Complaint: Yes

Step 5 – View the Admin Dashboard

Open:

admin.html

The administrator can view submitted reports and their details.

⸻

7. Backend API

The application backend provides the following main endpoints:

Health Check

GET /

Used to verify that the CivicEye AI backend is running.

Submit Report

POST /upload

Receives the uploaded image and report information and returns the analysed report.

Get Reports

GET /reports

Returns submitted reports for the Admin Dashboard.

Delete Report

DELETE /reports/:id

Removes a selected report from the backend.

⸻

8. Requirements

To run the project locally, the following are recommended:
	•	Modern web browser
	•	Node.js
	•	Internet connection for the deployed backend
	•	JavaScript enabled

Install the backend dependencies using:

npm install

Start the backend using:

node server.js

⸻

9. Important Notes for Judges

The project is designed as a web application.

For the easiest demonstration:
	1.	Open the reporting interface.
	2.	Create a sample public-issue report.
	3.	View the AI analysis result.
	4.	Open the Admin Dashboard to view the submitted report.

For duplicate detection, submit the same issue type and location more than once.

The project has been designed to support both desktop and mobile screen sizes.

⸻

10. Project Objective

The main objective of CivicEye AI is to demonstrate how AI-assisted software can improve the way citizens report public issues and how such reports can be organized for administrative monitoring.

The project focuses on:
	•	Citizen participation
	•	Intelligent report analysis
	•	Public issue prioritization
	•	Duplicate complaint identification
	•	Authority recommendation
	•	Digital administration

⸻

11. Future Improvements

Possible future developments include:
	•	Advanced computer-vision-based issue detection
	•	Real-time authority notifications
	•	Interactive geographic issue maps
	•	Improved multilingual AI support
	•	Cloud database integration
	•	Real-time report status updates
	•	Advanced analytics and prediction
	•	Integration with relevant public-service authorities

⸻

12. Conclusion

CivicEye AI demonstrates a practical application of AI and web technologies to address real-world public-service problems.

By combining citizen reporting, image uploads, location information, AI-assisted analysis, priority detection, duplicate detection, authority recommendation, and administrative monitoring, the system provides a foundation for a smarter and more organized public issue reporting process.

⸻

Project Information

Project Name: CivicEye AI

Competition: Young Computer Scientist (YCS) 2026

Project Type: AI-Powered Web Application

Country: Sri Lanka 🇱🇰

