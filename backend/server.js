const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

const upload = multer({
    dest: "uploads/"
});

app.use(
    "/uploads",
    express.static(
        path.join(__dirname, "uploads")
    )
);

let reports = [];
let notifications = [];
let adminAlerts = [];

// ==========================================
// HOME / HEALTH CHECK
// ==========================================

app.get("/", (req, res) => {

    res.json({
        message:
            "CivicEye AI Backend is running 🚀"
    });

});

// ==========================================
// AUTHORITY RECOMMENDATION
// ==========================================

function recommendAuthority(issue) {

    const issueText =
        String(issue || "")
            .toLowerCase()
            .trim();

    if (issueText.includes("water")) {
        return "Water Supply Authority";
    }

    if (issueText.includes("garbage")) {
        return "Local Municipal Authority";
    }

    if (issueText.includes("road")) {
        return "Road Development / Local Authority";
    }

    if (
        issueText.includes("street light") ||
        issueText.includes("streetlight")
    ) {
        return "Local Authority / Electricity Provider";
    }

    return "Relevant Local Authority";
}

// ==========================================
// PRIORITY DETECTION
// ==========================================

function determinePriority(
    issue,
    description
) {

    const text =
        (
            String(issue || "") +
            " " +
            String(description || "")
        ).toLowerCase();

    const emergencyKeywords = [
        "flood",
        "flooding",
        "fire",
        "dangerous",
        "electric shock",
        "electrical hazard",
        "collapsed",
        "accident",
        "blocked emergency",
        "life threatening"
    ];

    const highKeywords = [
        "large pothole",
        "major pothole",
        "severe damage",
        "broken pipe",
        "burst pipe",
        "heavy leak",
        "dangerous road"
    ];

    if (
        emergencyKeywords.some(
            keyword =>
                text.includes(keyword)
        )
    ) {
        return "Emergency";
    }

    if (
        highKeywords.some(
            keyword =>
                text.includes(keyword)
        )
    ) {
        return "High";
    }

    if (
        String(issue || "")
            .toLowerCase()
            .trim() === "road damage"
    ) {
        return "High";
    }

    if (
        String(issue || "")
            .toLowerCase()
            .trim() === "water leakage"
    ) {
        return "High";
    }

    if (
        String(issue || "")
            .toLowerCase()
            .trim() === "street light issue"
    ) {
        return "Medium";
    }

    return "Normal";
}

// ==========================================
// DUPLICATE COMPLAINT DETECTION
// ==========================================

function checkDuplicate(
    issue,
    location
) {

    const normalizedIssue =
        String(issue || "")
            .toLowerCase()
            .trim();

    const normalizedLocation =
        String(location || "")
            .toLowerCase()
            .trim();

    const duplicate =
        reports.find(report => {

            const oldIssue =
                String(report.issue || "")
                    .toLowerCase()
                    .trim();

            const oldLocation =
                String(report.location || "")
                    .toLowerCase()
                    .trim();

            return (
                oldIssue === normalizedIssue &&
                oldLocation === normalizedLocation
            );

        });

    if (duplicate) {

        return {

            isDuplicate: true,

            duplicateReportId:
                duplicate.id

        };

    }

    return {

        isDuplicate: false,

        duplicateReportId: null

    };

}

// ==========================================
// CITIZEN NOTIFICATIONS
// ==========================================

function createNotification(
    reportId,
    type,
    title,
    message,
    citizenEmail = null
) {

    const notification = {

        id:
            Date.now() +
            Math.floor(
                Math.random() * 1000
            ),

        reportId,

        citizenEmail,

        type,

        title,

        message,

        read: false,

        createdAt:
            new Date().toISOString()

    };

    notifications.push(
        notification
    );

    console.log(
        "🔔 Citizen notification created:",
        notification
    );

    return notification;

}

// ==========================================
// ADMIN ALERTS
// ==========================================

function createAdminAlert(
    reportId,
    type,
    title,
    message
) {

    const alert = {

        id:
            Date.now() +
            Math.floor(
                Math.random() * 1000
            ),

        reportId,

        type,

        title,

        message,

        read: false,

        createdAt:
            new Date().toISOString()

    };

    adminAlerts.push(
        alert
    );

    console.log(
        "🔔 Admin alert created:",
        alert
    );

    return alert;

}

// ==========================================
// UPLOAD / CREATE REPORT
// ==========================================

app.post(
    "/upload",
    upload.single("image"),
    (req, res) => {

        try {

            // ----------------------------------
            // IMAGE CHECK
            // ----------------------------------

            if (!req.file) {

                return res.status(400).json({

                    success: false,

                    message:
                        "No image uploaded"

                });

            }

            // ----------------------------------
            // REPORT DATA
            // ----------------------------------
            // Supports both:
            // issueType  -> current report.html
            // issue      -> older frontend
            // ----------------------------------

            const issue =
                String(
                    req.body.issueType ||
                    req.body.issue ||
                    "Other"
                ).trim();

            const description =
                String(
                    req.body.description ||
                    ""
                ).trim();

            const location =
                String(
                    req.body.location ||
                    "Unknown"
                ).trim();

            // ----------------------------------
            // CITIZEN EMAIL
            // ----------------------------------

            const citizenEmail =
                String(
                    req.body.citizenEmail ||
                    req.body.email ||
                    req.body.userEmail ||
                    ""
                )
                    .trim()
                    .toLowerCase() ||
                null;

            // ==================================
            // AI PROCESSING
            // ==================================

            console.log("");
            console.log(
                "=========================================="
            );
            console.log(
                "🤖 AI PROCESSING STARTED"
            );
            console.log(
                "=========================================="
            );

            console.log(
                `Issue: ${issue}`
            );

            console.log(
                `Location: ${location}`
            );

            console.log(
                `Citizen: ${citizenEmail || "Not provided"}`
            );

            // ----------------------------------
            // PRIORITY
            // ----------------------------------

            const priority =
                determinePriority(
                    issue,
                    description
                );

            // ----------------------------------
            // AUTHORITY
            // ----------------------------------

            const authority =
                recommendAuthority(
                    issue
                );

            // ----------------------------------
            // DUPLICATE DETECTION
            // ----------------------------------

            const duplicateResult =
                checkDuplicate(
                    issue,
                    location
                );

            // ==================================
            // DUPLICATE COMPLAINT
            // ==================================

            if (
                duplicateResult.isDuplicate
            ) {

                console.log("");
                console.log(
                    "⚠️ DUPLICATE COMPLAINT DETECTED"
                );

                console.log(
                    `🔗 Existing complaint ID: ${duplicateResult.duplicateReportId}`
                );

                // --------------------------------
                // CREATE AI RESULT OBJECT
                // --------------------------------
                // This object is NOT saved into
                // reports[].
                //
                // It is returned to the AI
                // processing page so the citizen
                // can see the analysis result.
                // --------------------------------

                const duplicateReport = {

                    id:
                        Date.now(),

                    issue,

                    confidence:
                        "94%",

                    location,

                    description,

                    status:
                        "Submitted",

                    priority,

                    authority,

                    isDuplicate:
                        true,

                    duplicate:
                        true,

                    duplicateReportId:
                        duplicateResult.duplicateReportId,

                    citizenEmail,

                    image:
                        req.file.filename,

                    createdAt:
                        new Date().toISOString(),

                    solvedAt:
                        null

                };

                // --------------------------------
                // CITIZEN DUPLICATE NOTIFICATION
                // --------------------------------

                const duplicateNotification =
                    createNotification(

                        duplicateResult.duplicateReportId,

                        "duplicate",

                        "⚠️ Duplicate Complaint Detected",

                        `Your ${issue} complaint appears to be a duplicate of an existing complaint at ${location}. The existing complaint is already registered.`,

                        citizenEmail

                    );

                // --------------------------------
                // ADMIN DUPLICATE ALERT
                // --------------------------------

                const duplicateAdminAlert =
                    createAdminAlert(

                        duplicateResult.duplicateReportId,

                        "duplicate",

                        "⚠️ Duplicate Complaint Attempt",

                        `A citizen attempted to submit a duplicate ${issue} complaint from ${location}. Existing complaint ID: ${duplicateResult.duplicateReportId}.`

                    );

                console.log(
                    "🔔 Duplicate citizen notification created"
                );

                console.log(
                    "🔔 Duplicate admin alert created"
                );

                console.log(
                    "ℹ️ Duplicate complaint was NOT added as a new report"
                );

                console.log(
                    "=========================================="
                );

                // ==================================
                // IMPORTANT DUPLICATE RESPONSE
                // ==================================
                //
                // accepted: true
                // -> The complaint request was
                //    successfully processed by AI.
                //
                // adminSubmitted: false
                // -> It is NOT created as a new
                //    admin report because it is
                //    already registered.
                //
                // The citizen still continues to
                // ai-processing.html.
                // ==================================

                return res.status(200).json({

                    success: true,

                    message:
                        "AI analysis completed. Duplicate complaint detected.",

                    duplicate: true,

                    isDuplicate: true,

                    accepted: true,

                    adminSubmitted: false,

                    existingReportId:
                        duplicateResult.duplicateReportId,

                    notification:
                        duplicateNotification,

                    adminAlert:
                        duplicateAdminAlert,

                    report:
                        duplicateReport

                });

            }

            // ==================================
            // NORMAL / NON-DUPLICATE REPORT
            // ==================================

            const report = {

                id:
                    Date.now(),

                issue,

                confidence:
                    "94%",

                location,

                description,

                status:
                    "Pending",

                priority,

                authority,

                isDuplicate:
                    false,

                duplicate:
                    false,

                duplicateReportId:
                    null,

                citizenEmail,

                image:
                    req.file.filename,

                createdAt:
                    new Date().toISOString(),

                solvedAt:
                    null

            };

            // ==================================
            // SAVE NORMAL REPORT
            // ==================================

            reports.push(
                report
            );

            console.log("");
            console.log(
                `✅ AI accepted new report: ${report.id}`
            );

            // ==================================
            // NORMAL CITIZEN NOTIFICATION
            // ==================================
            // IMPORTANT:
            // This notification is ONLY created
            // for a normal new complaint.
            // ==================================

            createNotification(

                report.id,

                "report_submitted",

                "📢 Report Submitted",

                `Your ${issue} report has been submitted successfully and is now pending review.`,

                citizenEmail

            );

            // ==================================
            // NORMAL ADMIN ALERT
            // ==================================
            // IMPORTANT:
            // This is ONLY created for a new
            // non-duplicate complaint.
            // ==================================

            createAdminAlert(

                report.id,

                "new_report",

                "📢 New Citizen Report",

                `A new ${issue} report has been submitted from ${location}.`

            );

            console.log(
                "=========================================="
            );

            return res.status(200).json({

                success: true,

                message:
                    "Report analysed successfully 🚀",

                duplicate: false,

                isDuplicate: false,

                accepted: true,

                adminSubmitted: true,

                report

            });

        } catch (error) {

            console.error(
                "❌ Upload error:",
                error
            );

            return res.status(500).json({

                success: false,

                message:
                    "Server error while uploading image"

            });

        }

    }
);

// ==========================================
// GET ALL REPORTS
// ==========================================

app.get(
    "/reports",
    (req, res) => {

        cleanupOldSolvedReports();

        res.status(200).json(
            reports
        );

    }
);

// ==========================================
// GET SINGLE REPORT
// ==========================================

app.get(
    "/reports/:id",
    (req, res) => {

        cleanupOldSolvedReports();

        const reportId =
            Number(
                req.params.id
            );

        const report =
            reports.find(
                item =>
                    item.id ===
                    reportId
            );

        if (!report) {

            return res.status(404).json({

                message:
                    "Report not found"

            });

        }

        res.status(200).json(
            report
        );

    }
);

// ==========================================
// UPDATE REPORT STATUS
// ==========================================

app.patch(
    "/reports/:id/status",
    (req, res) => {

        try {

            const reportId =
                Number(
                    req.params.id
                );

            const newStatus =
                String(
                    req.body.status || ""
                ).trim();

            const allowedStatuses = [
                "Pending",
                "Processing",
                "Solved"
            ];

            if (
                !allowedStatuses.includes(
                    newStatus
                )
            ) {

                return res.status(400).json({

                    message:
                        "Invalid report status"

                });

            }

            const report =
                reports.find(
                    item =>
                        item.id ===
                        reportId
                );

            if (!report) {

                return res.status(404).json({

                    message:
                        "Report not found"

                });

            }

            // ==================================
            // DUPLICATE SAFETY CHECK
            // ==================================
            // Duplicate analysis objects are not
            // saved inside reports[], so normally
            // this will never block a real report.
            // ==================================

            if (
                report.isDuplicate === true
            ) {

                return res.status(403).json({

                    message:
                        "Duplicate complaints cannot be processed as new reports"

                });

            }

            const oldStatus =
                report.status;

            report.status =
                newStatus;

            // ==================================
            // SOLVED TIME
            // ==================================

            if (
                newStatus === "Solved" &&
                oldStatus !== "Solved"
            ) {

                report.solvedAt =
                    new Date().toISOString();

            }

            // ==================================
            // RESET SOLVED TIME
            // ==================================

            if (
                newStatus !== "Solved"
            ) {

                report.solvedAt =
                    null;

            }

            console.log(
                `Report ${reportId} status updated from ${oldStatus} to ${newStatus}`
            );

            // ==================================
            // PROCESSING NOTIFICATION
            // ==================================

            if (
                newStatus === "Processing" &&
                oldStatus !== "Processing"
            ) {

                createNotification(

                    report.id,

                    "status_update",

                    "🔵 Report Processing",

                    `Your ${report.issue} report is now being processed by the relevant authority.`,

                    report.citizenEmail

                );

            }

            // ==================================
            // SOLVED NOTIFICATION
            // ==================================

            if (
                newStatus === "Solved" &&
                oldStatus !== "Solved"
            ) {

                createNotification(

                    report.id,

                    "status_update",

                    "🟢 Issue Solved",

                    `Your ${report.issue} report has been marked as solved.`,

                    report.citizenEmail

                );

                createAdminAlert(

                    report.id,

                    "resolved",

                    "🟢 Report Solved",

                    `Report ${report.id} has been marked as solved.`

                );

            }

            return res.status(200).json({

                message:
                    "Report status updated successfully",

                report

            });

        } catch (error) {

            console.error(
                "Status update error:",
                error
            );

            return res.status(500).json({

                message:
                    "Server error while updating report status"

            });

        }

    }
);

// ==========================================
// CITIZEN NOTIFICATIONS - GET
// ==========================================

app.get(
    "/notifications",
    (req, res) => {

        const citizenEmail =
            String(
                req.query.email ||
                req.query.citizenEmail ||
                ""
            )
                .trim()
                .toLowerCase();

        let citizenNotifications = [];

        if (citizenEmail) {

            citizenNotifications =
                notifications.filter(
                    notification =>
                        String(
                            notification.citizenEmail ||
                            ""
                        )
                            .trim()
                            .toLowerCase() ===
                        citizenEmail
                );

        } else {

            citizenNotifications = [];

        }

        const unreadCount =
            citizenNotifications.filter(
                notification =>
                    notification.read === false
            ).length;

        res.status(200).json({

            count:
                citizenNotifications.length,

            unread:
                unreadCount,

            notifications:
                citizenNotifications
                    .slice()
                    .reverse()

        });

    }
);

// ==========================================
// MARK ONE NOTIFICATION AS READ
// ==========================================

app.patch(
    "/notifications/:id/read",
    (req, res) => {

        const notificationId =
            Number(
                req.params.id
            );

        const notification =
            notifications.find(
                item =>
                    item.id ===
                    notificationId
            );

        if (!notification) {

            return res.status(404).json({

                message:
                    "Notification not found"

            });

        }

        const citizenEmail =
            String(
                req.body.citizenEmail ||
                req.body.email ||
                req.query.email ||
                req.query.citizenEmail ||
                ""
            )
                .trim()
                .toLowerCase();

        const notificationEmail =
            String(
                notification.citizenEmail ||
                ""
            )
                .trim()
                .toLowerCase();

        if (
            notificationEmail &&
            notificationEmail !== citizenEmail
        ) {

            return res.status(403).json({

                message:
                    "You are not authorized to update this notification"

            });

        }

        if (
            notificationEmail &&
            !citizenEmail
        ) {

            return res.status(403).json({

                message:
                    "Citizen email is required"

            });

        }

        notification.read =
            true;

        return res.status(200).json({

            message:
                "Notification marked as read",

            notification

        });

    }
);

// ==========================================
// MARK ALL NOTIFICATIONS AS READ
// ==========================================

app.patch(
    "/notifications/read-all",
    (req, res) => {

        const citizenEmail =
            String(
                req.body.email ||
                req.body.citizenEmail ||
                ""
            )
                .trim()
                .toLowerCase();

        if (!citizenEmail) {

            return res.status(400).json({

                message:
                    "Citizen email is required"

            });

        }

        notifications.forEach(
            notification => {

                const notificationEmail =
                    String(
                        notification.citizenEmail ||
                        ""
                    )
                        .trim()
                        .toLowerCase();

                if (
                    notificationEmail ===
                    citizenEmail
                ) {

                    notification.read =
                        true;

                }

            }
        );

        const remainingUnread =
            notifications.filter(
                notification => {

                    const notificationEmail =
                        String(
                            notification.citizenEmail ||
                            ""
                        )
                            .trim()
                            .toLowerCase();

                    return (
                        notificationEmail ===
                        citizenEmail &&
                        notification.read === false
                    );

                }
            ).length;

        return res.status(200).json({

            message:
                "Notifications marked as read",

            unread:
                remainingUnread

        });

    }
);

// ==========================================
// ADMIN ALERTS - GET
// ==========================================

app.get(
    "/admin-alerts",
    (req, res) => {

        const unreadCount =
            adminAlerts.filter(
                alert =>
                    alert.read === false
            ).length;

        res.status(200).json({

            count:
                adminAlerts.length,

            unread:
                unreadCount,

            alerts:
                adminAlerts
                    .slice()
                    .reverse()

        });

    }
);

// ==========================================
// MARK ADMIN ALERT AS READ
// ==========================================

app.patch(
    "/admin-alerts/:id/read",
    (req, res) => {

        const alertId =
            Number(
                req.params.id
            );

        const alert =
            adminAlerts.find(
                item =>
                    item.id ===
                    alertId
            );

        if (!alert) {

            return res.status(404).json({

                message:
                    "Admin alert not found"

            });

        }

        alert.read =
            true;

        return res.status(200).json({

            message:
                "Admin alert marked as read",

            alert

        });

    }
);

// ==========================================
// TEST NOTIFICATION
// ==========================================

app.post(
    "/test-notification",
    (req, res) => {

        const citizenEmail =
            String(
                req.body.email ||
                req.body.citizenEmail ||
                ""
            )
                .trim()
                .toLowerCase() ||
            null;

        const notification =
            createNotification(

                999999,

                "test",

                "🔔 Test Notification",

                "CivicEye AI notification system is working successfully.",

                citizenEmail

            );

        return res.status(200).json({

            message:
                "Test notification created successfully",

            notification

        });

    }
);

// ==========================================
// 14-DAY SOLVED REPORT CLEANUP
// ==========================================

function cleanupOldSolvedReports() {

    const now =
        Date.now();

    const FOURTEEN_DAYS =
        14 *
        24 *
        60 *
        60 *
        1000;

    const beforeCount =
        reports.length;

    reports =
        reports.filter(
            report => {

                if (
                    String(
                        report.status || ""
                    ).toLowerCase() !==
                    "solved"
                ) {

                    return true;

                }

                if (
                    !report.solvedAt
                ) {

                    return true;

                }

                const solvedTime =
                    new Date(
                        report.solvedAt
                    ).getTime();

                if (
                    Number.isNaN(
                        solvedTime
                    )
                ) {

                    return true;

                }

                const age =
                    now -
                    solvedTime;

                return (
                    age <
                    FOURTEEN_DAYS
                );

            }
        );

    const deletedCount =
        beforeCount -
        reports.length;

    if (
        deletedCount > 0
    ) {

        console.log(
            `🗑️ 14-day auto cleanup: ${deletedCount} solved report(s) deleted`
        );

    }

}

// ==========================================
// RUN CLEANUP EVERY HOUR
// ==========================================

setInterval(
    cleanupOldSolvedReports,
    60 * 60 * 1000
);

// ==========================================
// START SERVER
// ==========================================

const PORT =
    process.env.PORT ||
    5000;

app.listen(
    PORT,
    () => {

        console.log(
            `CivicEye AI Backend running on port ${PORT}`
        );

        console.log(
            "🤖 AI complaint processing: ACTIVE"
        );

        console.log(
            "🔍 Duplicate complaint detection: ACTIVE"
        );

        console.log(
            "🔔 Duplicate citizen notifications: ACTIVE"
        );

        console.log(
            "🔔 Duplicate admin alerts: ACTIVE"
        );

        console.log(
            "🔔 Citizen notifications: ACTIVE"
        );

        console.log(
            "🔔 Citizen-specific notifications: ACTIVE"
        );

        console.log(
            "🔔 Admin alerts: ACTIVE"
        );

        console.log(
            "🗑️ 14-day solved auto cleanup: ACTIVE"
        );

    }
);