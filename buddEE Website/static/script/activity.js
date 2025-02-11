// set global variables
const date = document.querySelector("#date");
const dateErrorText = document.querySelector("#date-error-text");
const hours = document.querySelector("#hours");
const minutes = document.querySelector("#minutes");
const timeErrorText = document.querySelector("#time-error-text");
const timeZeroErrorText = document.querySelector("#time-zero-error-text");
const activityGroup = document.querySelector("#choose-activity");
const activityErrorText = document.querySelector("#activity-error-text");
const submitButton = document.querySelector("#submit");

// set the maximum date that can be selected to today's date (users cannot enter in future exercises)
let today = new Date();
let dd = today.getDate();
let mm = today.getMonth()+1; //January is 0 so need to add 1 to make it 1!
let yyyy = today.getFullYear();
if (dd < 10) {
  dd ='0'+ dd
} 
if (mm < 10){
  mm ='0'+ mm
} 

today = yyyy + '-' + mm + '-' + dd;
date.setAttribute("max", today);

// check that the date is not empty when it loses focus
date.addEventListener("blur", validateDate);

function validateDate() {
    // checks whether the date field is empty
    // adds or removes error idicator as needed
    if (date.value == "") {
        dateErrorText.classList.remove("hidden");
        return false;
    } else {
        dateErrorText.classList.add("hidden");
        return true;
    }
}

// check that the time is not empty when they're blurred
hours.addEventListener("blur", validateHours);
minutes.addEventListener("blur", validateMinutes);

function validateHours() {
    // checks whether either time fields is empty
    // adds or removes error idicator as needed
    if (hours.value.length == 0) {
        timeErrorText.classList.remove("hidden");
        return false;
    } else {
        timeErrorText.classList.add("hidden");
        return true;
    }
}

function validateMinutes() {
    // checks whether either time fields is empty
    // adds or removes error idicator as needed
    if (minutes.value.length == 0) {
        timeErrorText.classList.remove("hidden");
        return false;
    } else {
        timeErrorText.classList.add("hidden");
        return true;
    }
}

// add event listeners for each radio (activities)
let activityRadios = document.querySelectorAll('input[name="activity"]');
for (let radio of activityRadios) {
    radio.addEventListener("click", validateActivity);
}

function validateActivity() {
    // checks whether an option is selected
    // adds or removes error idicator as needed
    let selected = document.querySelector('input[name="activity"]:checked');
    if (selected) {
        activityErrorText.classList.add("hidden");
        return true;
    } else {
        activityErrorText.classList.remove("hidden");
        return false;
    }
}

// check all the other values have been validated before being able to submit
submitButton.addEventListener("click", validateAll);

function validateAll(event) {
    // calls each validation functions
    let validDate = validateDate();
    let validHours = validateHours();
    let validMinutes = validateMinutes();
    let validActivity = validateActivity();
    let validTime;

    if (hours.value == 0 && minutes.value == 0) {
        validTime = false;
        timeZeroErrorText.classList.remove("hidden");
    } else {
        validTime = true;
        timeErrorText.classList.add("hidden");
    }

    allValid = validDate && validHours && validMinutes && validActivity && validTime;

    // check that overall time does not equal zero

    if (allValid == false) {
        // stops the form from submitting
        event.preventDefault();
    }
}