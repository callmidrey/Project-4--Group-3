//style.js

document.addEventListener("DOMContentLoaded", function () {
    // Add styles to form elements when the DOM is fully loaded
    styleForm();
});

function styleForm() {
    const form = document.getElementById("dataForm");

    if (form) {
        form.classList.add("styled-form");

        const labels = form.querySelectorAll("label");
        labels.forEach((label) => {
            label.classList.add("styled-label");
        });

        const inputs = form.querySelectorAll("input");
        inputs.forEach((input) => {
            input.classList.add("styled-input");
        });

        const buttons = form.querySelectorAll("button");
        buttons.forEach((button) => {
            button.classList.add("styled-button");
            button.addEventListener("click", submitForm);
        });
    }
}

function submitForm() {
    const formData = {
        first_name: getValueById('first_name'),
        last_name: getValueById('last_name'),
        age: getValueById('age'),
        email: getValueById('email'),
        phone_number: getValueById('phone_number'),
        SK_ID_CURR: getValueById('SK_ID_CURR'),
        AMT_INCOME_TOTAL: getValueById('AMT_INCOME_TOTAL'),
        AMT_REQ_CREDIT_BUREAU_YEAR: getValueById('AMT_REQ_CREDIT_BUREAU_YEAR'),
        OBS_30_CNT_SOCIAL_CIRCLE: getValueById('OBS_30_CNT_SOCIAL_CIRCLE'),
        OBS_60_CNT_SOCIAL_CIRCLE: getValueById('OBS_60_CNT_SOCIAL_CIRCLE'),
        AMT_ANNUITY_x: getValueById('AMT_ANNUITY_x'),
        CNT_INSTALMENT_MATURE_CUM: getValueById('CNT_INSTALMENT_MATURE_CUM'),
        AMT_PAYMENT: getValueById('AMT_PAYMENT'),
        DAYS_ENTRY_PAYMENT: getValueById('DAYS_ENTRY_PAYMENT'),
        AMT_INSTALMENT: getValueById('AMT_INSTALMENT'),
        DAYS_INSTALMENT: getValueById('DAYS_INSTALMENT'),
        NUM_INSTALMENT_NUMBER: getValueById('NUM_INSTALMENT_NUMBER'),
        CNT_INSTALMENT_FUTURE: getValueById('CNT_INSTALMENT_FUTURE'),
        CNT_INSATLMENT: getValueById('CNT_INSATLMENT'),
        MONTHS_BALANCE_Credit_card_balance: getValueById('MONTHS_BALANCE_Credit_card_balance'),
        MONTHS_BALANCE_x: getValueById('MONTHS_BALANCE_x'),
        CNT_FAM_MEMBERS: getValueById('CNT_FAM_MEMBERS'),
        OWN_CAR_AGE: getValueById('OWN_CAR_AGE')
    };

    fetch('/submitData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Data submitted successfully!');
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function getValueById(id) {
    return document.getElementById(id).value;
}
