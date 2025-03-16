document.addEventListener('DOMContentLoaded', () => {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Update file input labels when files are selected
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const label = e.target.parentElement.querySelector('span');
            label.textContent = e.target.files[0]?.name || 'Choose File';
        });
    });

    document.getElementById('analyze-btn').addEventListener('click', async () => {
        const resumeFile = document.getElementById('resume-upload').files[0];
        const requirementsFile = document.getElementById('requirements-upload').files[0];

        if (!resumeFile || !requirementsFile) {
            alert('Please upload both resume and requirements documents');
            return;
        }

        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('requirements', requirementsFile);

        try {
            // Show loading spinner
            loadingSpinner.style.display = 'block';
            document.getElementById('results').style.display = 'none';

            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Server error');
            }

            const results = await response.json();
            displayResults(results);
        } catch (error) {
            console.error('Error analyzing documents:', error);
            alert('Error analyzing documents. Please try again.');
        } finally {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
        }
    });

    function displayResults(results) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';

        // Update match percentage and circle progress
        const matchPercentage = results.overall_match;
        const scoreCircle = document.querySelector('.score-circle');
        const percentageText = document.getElementById('match-percentage');
        
        scoreCircle.style.setProperty('--percentage', `${matchPercentage}%`);
        percentageText.textContent = `${matchPercentage}%`;

        // Update matching skills
        const matchingSkillsList = document.getElementById('matching-skills-list');
        matchingSkillsList.innerHTML = results.matching_skills
            .map(skill => `<li>${skill}</li>`)
            .join('');

        // Update missing skills
        const missingSkillsList = document.getElementById('missing-skills-list');
        missingSkillsList.innerHTML = results.missing_skills
            .map(skill => `<li>${skill}</li>`)
            .join('');
    }
} 