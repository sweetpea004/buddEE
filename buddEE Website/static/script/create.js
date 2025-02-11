// set global variables
const petName = document.querySelector("#pet-name");
const petNameErrorText = document.querySelector("#pet-name-error-text");
const speciesGroup = document.querySelector("#choose-species");
const speciesErrorText = document.querySelector("#species-error-text");
const submitButton = document.querySelector("#submit");

// check that the pets name is not empty when it loses focus
petName.addEventListener("blur", validatePetName);

// add event listeners for each radio (species)
let speciesRadios = document.querySelectorAll('input[name="species"]');
for (let radio of speciesRadios) {
    radio.addEventListener("click", validateSpecies);
}

// check all the other values have been validated before being able to submit
submitButton.addEventListener("click", validateAll);

function validatePetName() {
    // checks whether the pet name field is empty
    // adds or removes error idicator as needed
    if (petName.value == "" || petName.value == " ") {
        petNameErrorText.classList.remove("hidden");
        return false;
    } else {
        petNameErrorText.classList.add("hidden");
        return true;
    }
}

function validateSpecies() {
    // checks whether an option is selected
    // adds or removes error idicator as needed
    let selected = document.querySelector('input[name="species"]:checked');
    if (selected) {
        speciesErrorText.classList.add("hidden");
        return true;
    } else {
        speciesErrorText.classList.remove("hidden");
        return false;
    }
}

function validateAll(event) {
    // calls each validation functions
    let validPetName = validatePetName();
    let validSpecies = validateSpecies();

    allValid = validPetName && validSpecies;

    if (allValid == false) {
        // stops the form from submitting
        event.preventDefault();
    }
}
