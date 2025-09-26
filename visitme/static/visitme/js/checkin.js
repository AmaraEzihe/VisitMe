document.addEventListener('DOMContentLoaded', function () {
  /**
   * ------------------------
   * FORM VALIDATION HANDLING
   * ------------------------
   */
  const form = document.getElementById('checkin-form');
  const nextBtn = document.getElementById('next-btn');
  const consentCheckbox = document.getElementById('consent');
  const requiredFields = form.querySelectorAll('[required]');

  function validateForm() {
    let isValid = true;

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        isValid = false;
        field.style.borderColor = '#ff0000';
      } else {
        field.style.borderColor = '#ddd';
      }
    });

    nextBtn.disabled = !consentCheckbox.checked || !isValid;
    return isValid;
  }

  consentCheckbox.addEventListener('change', validateForm);
  requiredFields.forEach((field) => {
    field.addEventListener('input', validateForm);
  });

  form.addEventListener('submit', function (event) {
    const isValid = validateForm();
    if (!consentCheckbox.checked) {
      event.preventDefault();
      alert('Please consent to the terms and conditions.');
    } else if (!isValid) {
      event.preventDefault();
      alert('Please fill all required fields.');
    }
  });
  
// Attach downloadPDF to a button with id 'download-pdf-btn'
document.getElementById('download-pdf-btn')?.addEventListener('click', function () {
  const element = document.getElementById('pass-card');
  html2pdf().from(element).save('visitor_pass.pdf');
});
 
});
