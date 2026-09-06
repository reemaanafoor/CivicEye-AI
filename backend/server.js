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

    if (
        issueText.includes("water")
    ) {

        return "Water Supply Authority";

    }

    if (
        issueText.includes("garbage")
    ) {

        return "Local Municipal Authority";

    }

    if (
        issueText.includes("road")
    ) {

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
            .trim() ===
        "road damage"
    ) {

        return "High";

    }

    if (
        String(issue || "")
            .toLowerCase()
            .trim() ===
        "water leakage"
    ) {

        return "High";

    }

    if (
        String(issue || "")
            .toLowerCase()
            .trim() ===
        "street light issue"
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
                oldLocation === normalizedLocation &&
                report.isDuplicate !== true
            );

        });

    if (duplicate) {

        return {

            isDuplicate:
                true,

            duplicateReportId:
                duplicate.id

        };

    }

    return {

        isDuplicate:
            false,

        duplicateReportId:
            null

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

        read:
            false,

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

        read:
            false,

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

                    message:
                        "No image uploaded"

                });

            }

            // ----------------------------------
            // REPORT DATA
            // ----------------------------------

            const issue =
                req.body.issue ||
                "Other";

            const description =
                req.body.description ||
                "";

            const location =
                req.body.location ||
                "Unknown";

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

            // ----------------------------------
            // DUPLICATE CHECK
            // ----------------------------------

            const duplicateResult =
                checkDuplicate(
                    issue,
                    location
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
            // CREATE REPORT
            // ----------------------------------

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
                    duplicateResult.isDuplicate,

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

            // ----------------------------------
            // SAVE REPORT
            // ----------------------------------

            reports.push(
                report
            );

            // ==================================
            // DUPLICATE REPORT
            // ==================================

            if (
                duplicateResult.isDuplicate
            ) {

                console.log(
                    `⚠️ Duplicate complaint detected: ${report.id}`
                );

                console.log(
                    `🔗 Existing report: ${duplicateResult.duplicateReportId}`
                );

                // --------------------------------
                // CITIZEN NOTIFICATION ONLY
                // --------------------------------

                createNotification(

                    report.id,

                    "duplicate",

                    "⚠️ Duplicate Complaint Detected",

                    `Your ${issue} complaint appears to be a duplicate. A similar complaint already exists for this issue and location. Existing Complaint ID: ${duplicateResult.duplicateReportId}`,

                    citizenEmail

                );

                // --------------------------------
                // IMPORTANT:
                // NO ADMIN ALERT
                // NO NORMAL ADMIN REPORT
                // --------------------------------

                console.log(
                    "🚫 Duplicate report excluded from Admin Dashboard"
                );

                console.log(
                    "🚫 Duplicate report excluded from Admin Alerts"
                );

                return res.status(200).json({

                    message:
                        "Duplicate complaint detected",

                    duplicate:
                        true,

                    report

                });

            }

            // ==================================
            // NORMAL REPORT
            // ==================================

            console.log(
                `✅ New normal report created: ${report.id}`
            );

            // ----------------------------------
            // CITIZEN NOTIFICATION
            // ----------------------------------

            createNotification(

                report.id,

                "report_submitted",

                "📢 Report Submitted",

                `Your ${issue} report has been submitted successfully and is now pending review.`,

                citizenEmail

            );

            // ----------------------------------
            // ADMIN ALERT
            // ----------------------------------

            createAdminAlert(

                report.id,

                "new_report",

                "📢 New Citizen Report",

                `A new ${issue} report has been submitted from ${location}.`

            );

            return res.status(200).json({

                message:
                    "Report analysed successfully 🚀",

                duplicate:
                    false,

                report

            });

        } catch (error) {

            console.error(
                "Upload error:",
                error
            );

            return res.status(500).json({

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

        // ======================================
        // DUPLICATE REPORTS ARE NOT SENT
        // TO ADMIN DASHBOARD
        // ======================================

        const adminReports =
            reports.filter(
                report =>
                    report.isDuplicate !== true
            );

        res.status(200).json(
            adminReports
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

            if (
                report.isDuplicate === true
            ) {

                return res.status(403).json({

                    message:
                        "Duplicate complaints cannot be processed from the Admin Dashboard"

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
// DELETE REPORT
// ==========================================

app.delete(
    "/reports/:id",
    (req, res) => {

        try {

            const reportId =
                Number(
                    req.params.id
                );

            const index =
                reports.findIndex(
                    report =>
                        report.id ===
                        reportId
                );

            if (index === -1) {

                return res.status(404).json({

                    message:
                        "Report not found"

                });

            }

            reports.splice(
                index,
                1
            );

            return res.status(200).json({

                message:
                    "Report deleted successfully"

            });

        } catch (error) {

            console.error(
                "Delete report error:",
                error
            );

            return res.status(500).json({

                message:
                    "Server error while deleting report"

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

        // ======================================
        // GET CITIZEN EMAIL
        // ======================================

        const citizenEmail =
            String(
                req.query.email ||
                req.query.citizenEmail ||
                ""
            )
            .trim()
            .toLowerCase();

        // ======================================
        // FILTER NOTIFICATIONS
        // ======================================

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

            // No email = return empty list.
            // This prevents one citizen from
            // seeing another citizen's notifications.

            citizenNotifications = [];

        }

        // ======================================
        // UNREAD COUNT
        // ======================================

        const unreadCount =
            citizenNotifications.filter(
                notification =>
                    notification.read === false
            ).length;

        // ======================================
        // RESPONSE
        // ======================================

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

        // ======================================
        // FIND NOTIFICATION
        // ======================================

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

        // ======================================
        // GET CITIZEN EMAIL
        // ======================================

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

        // ======================================
        // GET NOTIFICATION OWNER
        // ======================================

        const notificationEmail =
            String(
                notification.citizenEmail ||
                ""
            )
            .trim()
            .toLowerCase();

        // ======================================
        // SECURITY CHECK
        // ======================================

        /*
         * If the notification belongs to a citizen,
         * only that same citizen can mark it as read.
         */

        if (
            notificationEmail &&
            notificationEmail !== citizenEmail
        ) {

            console.log(
                `🚫 Unauthorized notification access attempt: ${notificationId}`
            );

            return res.status(403).json({

                message:
                    "You are not authorized to update this notification"

            });

        }

        // ======================================
        // EMAIL REQUIRED
        // ======================================

        if (
            notificationEmail &&
            !citizenEmail
        ) {

            return res.status(403).json({

                message:
                    "Citizen email is required"

            });

        }

        // ======================================
        // MARK AS READ
        // ======================================

        notification.read =
            true;

        console.log(
            `✅ Notification ${notificationId} marked as read for ${citizenEmail}`
        );

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

        // ======================================
        // REQUIRE CITIZEN EMAIL
        // ======================================

        if (!citizenEmail) {

            return res.status(400).json({

                message:
                    "Citizen email is required"

            });

        }

        // ======================================
        // ONLY MARK THIS CITIZEN'S NOTIFICATIONS
        // ======================================

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

        // ======================================
        // REMAINING UNREAD COUNT
        // ======================================

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

                // --------------------------------
                // KEEP UNSOLVED REPORTS
                // --------------------------------

                if (
                    String(
                        report.status || ""
                    ).toLowerCase() !==
                    "solved"
                ) {

                    return true;

                }

                // --------------------------------
                // KEEP IF SOLVED TIME MISSING
                // --------------------------------

                if (
                    !report.solvedAt
                ) {

                    return true;

                }

                const solvedTime =
                    new Date(
                        report.solvedAt
                    ).getTime();

                // --------------------------------
                // KEEP INVALID DATES
                // --------------------------------

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

                // --------------------------------
                // DELETE AFTER 14 DAYS
                // --------------------------------

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
            "🔍 Duplicate complaint detection: ACTIVE"
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
            "🚫 Duplicate reports hidden from Admin Dashboard: ACTIVE"
        );

        console.log(
            "🔐 Notification ownership security: ACTIVE"
        );

        console.log(
            "🗑️ 14-day solved auto cleanup: ACTIVE"
        );

    }
);