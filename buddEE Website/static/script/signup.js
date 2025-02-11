// set const global variables
const username = document.querySelector("#username");
const usernameErrorText = document.querySelector("#username-error-text");
const createPassword = document.querySelector("#create-password");
const confirmPassword = document.querySelector("#password-confirm");
const passwordErrorText = document.querySelector("#password-error-text");
const passwordEmptyErrorText = document.querySelector("#password-empty-error-text");
const confirmPasswordEmptyErrorText = document.querySelector("#confirm-password-empty-error-text")
const submitButton = document.querySelector("#submit")

// check that name is not empty when it loses focus
username.addEventListener("blur", validateUsername);

function validateUsername() {
    // checks whether the name field is empty
    // adds or removes error idicator as needed
    if (username.value == "" || username.value == " ") {
        usernameErrorText.classList.remove("hidden");
        return false;
    } else {
        usernameErrorText.classList.add("hidden");
        return true;
    }
}

// check that the password isnt an empty string
createPassword.addEventListener("blur", checkPasswordEmpty);

function checkPasswordEmpty() {
    // confirms the password input box isn't empty
    if (createPassword.value == '') {
        passwordEmptyErrorText.classList.remove('hidden');
        return false;
    } else {
        passwordEmptyErrorText.classList.add('hidden');
        return true;
    }
}

// check that the confirm password isnt an empty string
confirmPassword.addEventListener("blur", checkConfirmPasswordEmpty);

function checkConfirmPasswordEmpty() {
    // confirms the confirm password input box isn't empty
    if (confirmPassword.value == '') {
        confirmPasswordEmptyErrorText.classList.remove('hidden');
        return false;
    } else {
        confirmPasswordEmptyErrorText.classList.add('hidden');
        return true;
    }
}

// Checks to see if both passwords match
confirmPassword.addEventListener("blur", validatePasswords);

function validatePasswords() {
    // confirms if the two passwords match and raises an error if they don't
    if (createPassword.value == confirmPassword.value) {
        passwordErrorText.classList.add('hidden');
        return true;
    } else {
        passwordErrorText.classList.remove('hidden');
        return false;
    }
}

// check all the other values have been validated before being able to submit
submitButton.addEventListener("click", validateAll);

function validateAll(event) {
    // calls each validation functions
    let validUsername = validateUsername();
    let validPassword = checkPasswordEmpty();
    let validConfirmPassword = checkConfirmPasswordEmpty();
    let validPasswords = validatePasswords();

    allValid = validUsername && validPassword && validConfirmPassword && validPasswords

    if (allValid == false) {
        // stops the form from submitting
        event.preventDefault();
    }
}