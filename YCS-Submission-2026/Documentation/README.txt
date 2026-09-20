CIVICEYE AI
YCS 2026 — AI-Powered Civic Issue Reporting Platform
Sri Lanka

============================================================
1. PROJECT OVERVIEW
============================================================

CivicEye AI is an AI-assisted civic issue reporting and
monitoring web application developed as a competition
prototype for YCS 2026.

The platform is designed to help citizens report common
public issues such as road damage, garbage, water leaks,
and faulty street lights through a structured digital
workflow.

Citizens can submit issue information including an image,
issue type, description, and location. The system then
performs AI-assisted analysis using programmed rules and
keyword matching to support issue categorization, priority
assessment, and authority recommendation.

The platform also demonstrates duplicate detection,
citizen notifications, report tracking, resolution
verification, and an administrator dashboard.

CivicEye AI is a prototype and is not currently connected
to an official Municipal Council, government authority,
emergency service, or production government database.


============================================================
2. PROBLEM
============================================================

Public issues such as damaged roads, garbage accumulation,
water leaks, and faulty street lights require an organized
way for citizens to report them and for responsible
authorities to monitor them.

Traditional reporting processes may involve difficulties
such as:

* Unclear reporting channels
* Incomplete complaint information
* Difficulty identifying the relevant authority
* Repeated or duplicate complaints
* Limited visibility of complaint progress
* Difficulty identifying higher-priority issues
* Language barriers for some citizens

CivicEye AI addresses these challenges through a structured
digital reporting workflow that combines citizen input,
AI-assisted analysis, location information, priority
assessment, authority recommendation, duplicate detection,
notifications, and report tracking.


============================================================
3. PROPOSED SOLUTION
============================================================

CivicEye AI provides a single web-based platform where
citizens can create and monitor civic issue reports.

The general workflow is:

Citizen
   ↓
Create Report
   ↓
Upload Image + Enter Issue Details
   ↓
AI-Assisted Analysis
   ↓
Issue Categorization
   ↓
Priority Assessment
   ↓
Authority Recommendation
   ↓
Report Tracking
   ↓
Notifications
   ↓
Resolution Verification

The system is designed to make the reporting process more
structured while providing administrators with a dashboard
for monitoring submitted reports.


============================================================
4. MAIN FEATURES
============================================================

4.1 AI-Assisted Issue Categorization

The system analyzes the submitted issue information using
programmed rules and keyword matching to determine the
likely issue category.

Supported example categories include:

* Road Damage
* Garbage
* Water Leak
* Faulty Street Light


4.2 Image-Based Reporting

Citizens can upload an image related to the reported issue.
The image provides supporting visual information for the
submitted complaint.

The current prototype does not use a trained computer-vision
model for image classification.


4.3 Location Support

Citizens can enter or capture the location associated with
the reported issue.

Browser geolocation functionality depends on browser support
and user permission.


4.4 Priority Assessment

The system provides an AI-assisted priority assessment based
on programmed rules and issue information.

This is intended to demonstrate how reports could be
prioritized in a future production system.


4.5 Authority Recommendation

Based on the issue category, the system can recommend a
relevant authority for the reported issue.

This recommendation is part of the prototype workflow and
does not directly submit complaints to government authorities.


4.6 Multilingual Interaction

The platform is designed to support English, Tamil, and
Sinhala user interaction.

Voice recognition functionality depends on browser support
and user permissions.


4.7 Duplicate Detection

The backend checks submitted reports for potentially matching
existing reports using relevant report information such as
issue type and location.

This helps demonstrate how repeated complaints could be
identified.


4.8 Citizen Notifications

Citizens can receive notifications related to report activity
and status changes.


4.9 Admin Alerts

The administrator interface supports monitoring of relevant
report activity.


4.10 Report Tracking

Citizens can view submitted reports and monitor their current
status.


4.11 Resolution Verification

The prototype provides a citizen-facing resolution
verification interaction after an issue is marked as solved.


4.12 Administrator Dashboard

Administrators can review submitted reports and update their
status.

Example status flow:

Pending
   ↓
Processing
   ↓
Solved


============================================================
5. USER WORKFLOW
============================================================

Citizen Workflow

1. Open CivicEye AI.
2. Login as a citizen.
3. Open the Citizen Portal.
4. Select Report New Issue.
5. Upload an issue image.
6. Select the issue type.
7. Enter a description.
8. Enter or capture the location.
9. Submit the complaint.
10. View the AI-assisted analysis result.
11. Open the Citizen Dashboard.
12. Check the submitted report and notification.

Admin Workflow

1. Open Admin Login.
2. Open the Admin Dashboard.
3. Review submitted reports.
4. Open a report.
5. Review the report information.
6. Change the status from Pending to Processing.
7. Change the status from Processing to Solved.
8. Verify the updated status and generated notifications.


============================================================
6. TECHNOLOGIES USED
============================================================

Frontend:

* HTML5
* CSS3
* JavaScript

Backend:

* Node.js
* Express.js
* CORS
* Multer
* dotenv

Development and Deployment:

* Visual Studio Code
* Git / GitHub
* Vercel
* Railway

Browser-based capabilities:

* Geolocation API
* Web Speech / Voice Recognition support where available


============================================================
7. SYSTEM ARCHITECTURE
============================================================

The CivicEye AI prototype follows a frontend-backend
architecture.

Citizen / Admin
       ↓
Web Frontend
       ↓
JavaScript
       ↓
HTTP API
       ↓
Node.js + Express Backend
       ↓
Report Processing
       ↓
Duplicate Detection
       ↓
Notifications / Admin Alerts

The frontend communicates with the backend through HTTP
API requests.

The backend handles report processing, duplicate detection,
status management, notifications, and related application
logic.


============================================================
8. PROJECT STRUCTURE
============================================================

Main frontend pages include:

index.html
login.html
citizen.html
admin.html
report.html
ai-processing.html
track.html
profile.html
settings.html
notifications.html
privacy.html

Supporting frontend files include:

script.js
style.css
images/

Backend files contain the Node.js and Express server,
configuration, and supporting backend logic.


============================================================
9. DEPLOYMENT
============================================================

Frontend:

The frontend can be deployed as a web application using
Vercel.

Backend:

The backend is deployed using Railway.

The frontend communicates with the deployed backend through
the configured backend API URL.

The backend uses the environment variable PORT when provided.

When deployed on Railway, the platform-provided port is used.


============================================================
10. TESTING WORKFLOW
============================================================

Citizen Report Test

1. Open CivicEye AI.
2. Select Citizen Login.
3. Open the Citizen Portal.
4. Select Report New Issue.
5. Upload an issue image.
6. Select the issue type.
7. Enter a description.
8. Enter or capture the location.
9. Submit the complaint.
10. View the AI-assisted analysis result.
11. Open the Citizen Dashboard.
12. Check the submitted report and notification.


Duplicate Detection Test

1. Submit a report with a specific issue type and location.
2. Submit another report using the same issue type and location.
3. The backend checks for an existing matching report.
4. The second submission is identified as a duplicate.


Admin Test

1. Open Admin Login.
2. Open the Admin Dashboard.
3. Review submitted reports.
4. Open a report.
5. Change the status from Pending to Processing.
6. Change the status from Processing to Solved.
7. Verify the updated status and generated notifications.


============================================================
11. IMPORTANT PROTOTYPE LIMITATIONS
============================================================

CivicEye AI is a competition prototype and has several
limitations.

Rule-Based AI

The current AI-assisted analysis uses programmed rules and
keyword matching.

It does not currently use a trained machine-learning model
or external AI API.

Confidence Display

The current prototype displays a predefined confidence value
for demonstration purposes. It should not be interpreted as
a statistically calibrated machine-learning confidence score.

Data Storage

Reports and notifications are currently stored in server
memory.

Therefore, the prototype does not provide permanent database
storage.

Authentication

The current login system is designed for prototype
demonstration and does not provide production-grade
authentication.

Resolution Verification

The citizen resolution verification interface is currently
a frontend prototype interaction and is not stored through
a dedicated backend verification service.

Browser Features

Voice recognition and geolocation depend on browser support
and user permissions.


============================================================
12. FUTURE IMPROVEMENTS
============================================================

Future versions of CivicEye AI could include:

* Trained machine-learning models
* Computer vision for image-based issue classification
* Permanent cloud database
* Secure user authentication
* Role-based access control
* Per-citizen report access
* Real-time authority communication
* Advanced GIS mapping
* Persistent resolution verification
* Advanced analytics and reporting
* Mobile application support
* Integration with relevant government authorities


============================================================
13. PROJECT OBJECTIVE
============================================================

The objective of CivicEye AI is to demonstrate how web
technologies and AI-assisted decision logic can support more
structured civic issue reporting and monitoring.

The project focuses on:

* Simplifying citizen reporting
* Organizing complaint information
* Supporting issue prioritization
* Reducing repeated complaints
* Recommending relevant authorities
* Improving complaint visibility
* Supporting multilingual interaction


============================================================
14. CONCLUSION
============================================================

CivicEye AI demonstrates a prototype workflow for digital
civic issue reporting and monitoring.

By combining a citizen-facing web interface, a Node.js
backend, rule-based AI-assisted analysis, duplicate detection,
authority recommendation, notifications, and an administrator
dashboard, the project provides a foundation for a future
intelligent civic management platform.

The current implementation is intentionally presented as a
prototype, with future scope for machine learning, persistent
databases, secure authentication, advanced mapping, and
direct authority integration.


CivicEye AI · YCS 2026 · Sri Lanka