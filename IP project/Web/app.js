// Wait for DOM to fully load before executing
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const recommendationForm = document.getElementById('recommendationForm');
    const recommendationResult = document.getElementById('recommendationResult');
    const resultContent = document.getElementById('resultContent');


    // Handle form submission event
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(event) {
            // Prevent default form submission behavior
            event.preventDefault();
            
            // Get form data
            const height = document.getElementById('height').value;
            const weight = document.getElementById('weight').value;
            const age = document.getElementById('age').value;
            const gender = document.querySelector('input[name="gender"]:checked').value;
            const activityLevel = document.getElementById('activityLevel').value;
            
            // Form validation
            if (!validateForm(height, weight, age, activityLevel)) {
                return false;
            }
            
            // Create user data object
            const userData = {
                height: parseFloat(height),
                weight: parseFloat(weight),
                age: parseInt(age),
                gender: gender,
                activityLevel: activityLevel
            };
            
            // Print user data to console
            console.log('User input data:', JSON.stringify(userData, null, 2));
            
            // Show loading status
            resultContent.innerHTML = '<div class="text-center"><div class="spinner-border text-success" role="status"></div><p class="mt-2">Generating recommendations...</p></div>';
            recommendationResult.classList.remove('d-none');
            
            // Call backend API to get recommendation results
            fetch('http://localhost:5001/api/recommend-diet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response abnormal');
                }
                return response.json();
            })
            .then(data => {
                // Display recommendation results using API returned data
                displayRecommendationFromAPI(data);
            })
            .catch(error => {
                console.error('Failed to get recommendation:', error);
                resultContent.innerHTML = `<div class="alert alert-danger">Failed to get recommendation: ${error.message}</div>`;
            });
        });
    }


    // Form validation function
    function validateForm(height, weight, age, activityLevel) {
        // Validate height
        if (isNaN(height) || height < 100 || height > 250) {
            alert('Please enter a valid height (100-250 cm)');
            return false;
        }
        
        // Validate weight
        if (isNaN(weight) || weight < 30 || weight > 200) {
            alert('Please enter a valid weight (30-200 kg)');
            return false;
        }
        
        // Validate age
        if (isNaN(age) || age < 1 || age > 120) {
            alert('Please enter a valid age (1-120 years)');
            return false;
        }
        
        // Validate activity level
        if (!activityLevel) {
            alert('Please select your activity level');
            return false;
        }
        
        return true;
    }

    // Display API returned recommendation results function
    function displayRecommendationFromAPI(data) {
        if (data.error) {
            // Display error message in modal
            document.getElementById('modalResultContent').innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
            // Show modal
            const recommendationModal = new bootstrap.Modal(document.getElementById('recommendationModal'));
            recommendationModal.show();
            return;
        }
        
        const recommendation = data;
        const bmiInfo = recommendation["BMI Index"] || '';
        const recommendedRecipes = [];
        
        // Generate recommendation result HTML
        let resultHTML = ``;
        
        // Add API returned recommendation data
        for (const [key, value] of Object.entries(recommendation)) {
            resultHTML += `<div class="mb-2"><strong>${key}: </strong> ${value}</div>`;
        }
        
        // Add dietary recommendations
        resultHTML += `
            <hr>
            <div class="mb-2"><strong>Dietary Recommendations:</strong></div>
        `;
        
        // Add dietary suggestions based on BMI category
        const bmiCategory = bmiInfo || '';
        
        if (bmiCategory.includes('Underweight')) {
            resultHTML += `
                <ul>
                    <li>Increase intake of quality proteins such as lean meat, fish, eggs, and soy products</li>
                    <li>Moderately increase healthy fats like nuts, olive oil, and avocados</li>
                    <li>Eat more whole grain foods for complex carbohydrates</li>
                    <li>Consume sufficient fruits and vegetables daily</li>
                </ul>
            `;
        } else if (bmiCategory.includes('Normal')) {
            resultHTML += `
                <ul>
                    <li>Maintain a balanced diet including various food types</li>
                    <li>Control intake of refined sugar and processed foods</li>
                    <li>Maintain sufficient protein intake</li>
                    <li>Eat more fresh fruits, vegetables, and whole grains</li>
                </ul>
            `;
        } else {
            resultHTML += `
                <ul>
                    <li>Control total calorie intake, reduce high-calorie foods</li>
                    <li>Increase the proportion of vegetables and fruits</li>
                    <li>Choose lean meats and low-fat dairy products</li>
                    <li>Reduce refined carbohydrates and added sugars</li>
                    <li>Avoid fried and high-fat foods</li>
                </ul>
            `;
        }
        
        // No recipe recommendations in this version
        
        // Display results in modal
        document.getElementById('modalResultContent').innerHTML = resultHTML;
        
        // Show modal
        const recommendationModal = new bootstrap.Modal(document.getElementById('recommendationModal'));
        recommendationModal.show();
        
        // Add modal close event listener to clear loading status
        const modalElement = document.getElementById('recommendationModal');
        modalElement.addEventListener('hidden.bs.modal', function () {
            // Clear "Generating recommendations" loading prompt
            document.getElementById('resultContent').innerHTML = '';
            document.getElementById('recommendationResult').classList.add('d-none');
        });
    }

});
