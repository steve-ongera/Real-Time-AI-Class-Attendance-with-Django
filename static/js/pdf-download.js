// This script uses the html2pdf library to convert the page to PDF

// Function to download the page as PDF
function downloadPageAsPDF() {
    // Get the content of the page
    const element = document.body;

    // Configure the PDF options
    const opt = {
        margin:       1,
        filename:     'attendance_report.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    // Generate and download the PDF
    html2pdf().set(opt).from(element).save();
}