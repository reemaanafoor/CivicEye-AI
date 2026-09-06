/* =====================================================
   CIVICEYE AI - MAIN SCRIPT
===================================================== */


/* =====================================================
   DASHBOARD COUNTERS
===================================================== */

let counters =
    document.querySelectorAll(".counter");


counters.forEach(counter => {

    let target =
        +counter.getAttribute("data-target");

    let count = 0;


    let update = () => {

        if (count < target) {

            count += 5;

            if (count > target) {
                count = target;
            }

            counter.innerText = count;

            setTimeout(update, 20);

        }

        else {

            counter.innerText = target;

        }

    };


    update();

});



/* =====================================================
   PAGE LOADER
===================================================== */

window.addEventListener(
    "load",
    function () {

        const loader =
            document.querySelector(".loader");


        if (loader) {

            setTimeout(
                function () {

                    loader.style.display =
                        "none";

                },
                3000
            );

        }

    }
);



/* =====================================================
   REPORT SUCCESS MESSAGE
===================================================== */

const submitButton =
    document.querySelector(
        ".report button"
    );


const successMessage =
    document.getElementById(
        "successMessage"
    );


if (
    submitButton &&
    successMessage
) {

    submitButton.addEventListener(
        "click",
        function () {

            successMessage.style.display =
                "block";


            setTimeout(
                function () {

                    successMessage.style.display =
                        "none";

                },
                3000
            );

        }
    );

}



/* =====================================================
   LOGIN
===================================================== */

function loginUser() {

    const accountType =
        document.querySelector(
            "select"
        );


    if (
        accountType &&
        accountType.value === "Admin"
    ) {

        window.location.href =
            "admin.html";

    }

    else {

        window.location.href =
            "citizen.html";

    }

}



/* =====================================================
   CURRENT LOCATION
===================================================== */

function getCurrentLocation() {


    const locationInput =
        document.getElementById(
            "issueLocation"
        );


    const locationStatus =
        document.getElementById(
            "locationStatus"
        );


    if (!locationInput) {

        return;

    }



    if (
        !navigator.geolocation
    ) {

        alert(
            "⚠️ Geolocation is not supported by this browser."
        );

        return;

    }



    if (locationStatus) {

        locationStatus.textContent =
            "🔄 Getting your current location...";

    }



    navigator.geolocation.getCurrentPosition(


        function(position) {


            const latitude =
                position.coords.latitude;


            const longitude =
                position.coords.longitude;



            locationInput.value =
                latitude.toFixed(6) +
                ", " +
                longitude.toFixed(6);



            if (locationStatus) {

                locationStatus.textContent =
                    "✅ Current location captured successfully.";

            }

        },


        function(error) {


            console.error(
                "Location error:",
                error
            );


            if (locationStatus) {

                locationStatus.textContent =
                    "⚠️ Unable to get your location. Please enter it manually.";

            }

        },


        {

            enableHighAccuracy: true,

            timeout: 10000,

            maximumAge: 0

        }

    );

}
