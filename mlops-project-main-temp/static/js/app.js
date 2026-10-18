// ScoreSense Client-Side Controller
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictionForm');
  const submitBtn = document.getElementById('submitBtn');

  if (!form || !submitBtn) return;

  form.addEventListener('submit', (e) => {
    const hours = parseFloat(document.getElementById('hours_studied')?.value);
    const attendance = parseFloat(document.getElementById('attendance')?.value);
    const previous = parseFloat(document.getElementById('previous_marks')?.value);

    // Client-side quick range validation
    if (isNaN(hours) || hours < 0 || hours > 24) {
      alert('Hours Studied must be between 0 and 24.');
      e.preventDefault();
      return;
    }

    if (isNaN(attendance) || attendance < 0 || attendance > 100) {
      alert('Attendance must be between 0% and 100%.');
      e.preventDefault();
      return;
    }

    if (isNaN(previous) || previous < 0 || previous > 100) {
      alert('Previous Marks must be between 0% and 100%.');
      e.preventDefault();
      return;
    }

    // Prevent double submissions
    submitBtn.disabled = true;
    submitBtn.textContent = 'Predicting...';
  });
});
