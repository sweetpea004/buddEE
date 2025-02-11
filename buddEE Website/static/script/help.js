// variables
const openSignupLogin = document.querySelector("#open-signup-login");
const closeSignupLogin = document.querySelector("#close-signup-login");
const imgSignupLogin = document.querySelector("#img-signup-login");

const openCreate = document.querySelector("#open-create");
const closeCreate = document.querySelector("#close-create");
const imgCreate = document.querySelector("#img-create");

const openDashboard = document.querySelector("#open-dashboard");
const closeDashboard = document.querySelector("#close-dashboard");
const imgDashboard = document.querySelector("#img-dashboard");

const openAddAct = document.querySelector("#open-add-act");
const closeAddAct = document.querySelector("#close-add-act");
const imgAddAct = document.querySelector("#img-add-act");

const openEditDeleteAct = document.querySelector("#open-edit-delete-act");
const closeEditDeleteAct = document.querySelector("#close-edit-delete-act");
const imgEditDeleteAct = document.querySelector("#img-edit-delete-act");

const openAdopt = document.querySelector("#open-adopt");
const closeAdopt = document.querySelector("#close-adopt");
const imgAdopt = document.querySelector("#img-adopt");

const openAccount = document.querySelector("#open-account");
const closeAccount = document.querySelector("#close-account");
const imgAccount = document.querySelector("#img-account");


// check button presses
openSignupLogin.addEventListener("click", signupLoginOpen);
closeSignupLogin.addEventListener("click", signupLoginClose);

openCreate.addEventListener("click", createOpen);
closeCreate.addEventListener("click", createClose);

openDashboard.addEventListener("click", dashboardOpen);
closeDashboard.addEventListener("click", dashboardClose);

openAddAct.addEventListener("click", addActivityOpen);
closeAddAct.addEventListener("click", addActivityClose);

openEditDeleteAct.addEventListener("click", editDeleteActivityOpen);
closeEditDeleteAct.addEventListener("click", editDeleteActivityClose);

openAdopt.addEventListener("click", adoptionOpen);
closeAdopt.addEventListener("click", adoptionClose);

openAccount.addEventListener("click", accountOpen);
closeAccount.addEventListener("click", accountClose);


// button press functions
function signupLoginOpen() {
    // show image
    imgSignupLogin.classList.remove("hidden");

    // show close image button and hide open image button
    openSignupLogin.classList.add("hidden");
    closeSignupLogin.classList.remove("hidden");
}

function signupLoginClose() {
    // hide image
    imgSignupLogin.classList.add("hidden");

    // show open image button and hide close image button
    openSignupLogin.classList.remove("hidden");
    closeSignupLogin.classList.add("hidden");
}

function createOpen() {
    // show image
    imgCreate.classList.remove("hidden");

    // show close image button and hide open image button
    openCreate.classList.add("hidden");
    closeCreate.classList.remove("hidden");
}

function createClose() {
    // hide image
    imgCreate.classList.add("hidden");

    // show open image button and hide close image button
    openCreate.classList.remove("hidden");
    closeCreate.classList.add("hidden");
}

function dashboardOpen() {
    // show image
    imgDashboard.classList.remove("hidden");

    // show close image button and hide open image button
    openDashboard.classList.add("hidden");
    closeDashboard.classList.remove("hidden");
}

function dashboardClose() {
    // hide image
    imgDashboard.classList.add("hidden");

    // show open image button and hide close image button
    openDashboard.classList.remove("hidden");
    closeDashboard.classList.add("hidden");
}

function addActivityOpen() {
    // show image
    imgAddAct.classList.remove("hidden");

    // show close image button and hide open image button
    openAddAct.classList.add("hidden");
    closeAddAct.classList.remove("hidden");
}

function addActivityClose() {
    // hide image
    imgAddAct.classList.add("hidden");

    // show open image button and hide close image button
    openAddAct.classList.remove("hidden");
    closeAddAct.classList.add("hidden");
}

function editDeleteActivityOpen() {
    // show image
    imgEditDeleteAct.classList.remove("hidden");

    // show close image button and hide open image button
    openEditDeleteAct.classList.add("hidden");
    closeEditDeleteAct.classList.remove("hidden");
}

function editDeleteActivityClose() {
    // hide image
    imgEditDeleteAct.classList.add("hidden");

    // show open image button and hide close image button
    openEditDeleteAct.classList.remove("hidden");
    closeEditDeleteAct.classList.add("hidden");
}

function adoptionOpen() {
    // show image
    imgAdopt.classList.remove("hidden");

    // show close image button and hide open image button
    openAdopt.classList.add("hidden");
    closeAdopt.classList.remove("hidden");
}

function adoptionClose() {
    // hide image
    imgAdopt.classList.add("hidden");

    // show open image button and hide close image button
    openAdopt.classList.remove("hidden");
    closeAdopt.classList.add("hidden");
}

function accountOpen() {
    // show image
    imgAccount.classList.remove("hidden");

    // show close image button and hide open image button
    openAccount.classList.add("hidden");
    closeAccount.classList.remove("hidden");
}

function accountClose() {
    // hide image
    imgAccount.classList.add("hidden");

    // show open image button and hide close image button
    openAccount.classList.remove("hidden");
    closeAccount.classList.add("hidden");
}
