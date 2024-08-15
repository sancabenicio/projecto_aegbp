document.addEventListener("DOMContentLoaded", function () {
    const genderRadioButtons = document.querySelectorAll('input[name="gender"]');
    const otherGenderField = document.getElementById('id_other_gender');
    const isStudentRadioButtons = document.querySelectorAll('input[name="is_student"]');
    const studentFields = document.getElementById('student_fields').querySelectorAll('input, select');

    function toggleOtherGenderField() {
        let otherSelected = false;
        genderRadioButtons.forEach(button => {
            if (button.checked && button.value === 'other') {
                otherSelected = true;
            }
        });
        otherGenderField.disabled = !otherSelected;
    }

    function toggleStudentFields() {
        let studentSelected = false;
        isStudentRadioButtons.forEach(button => {
            if (button.checked && button.value === 'True') {
                studentSelected = true;
            }
        });
        studentFields.forEach(field => {
            field.disabled = !studentSelected;
        });
    }

    genderRadioButtons.forEach(button => {
        button.addEventListener('change', toggleOtherGenderField);
    });

    isStudentRadioButtons.forEach(button => {
        button.addEventListener('change', toggleStudentFields);
    });

    // Initial check to set fields correctly on page load
    toggleOtherGenderField();
    toggleStudentFields();
});
