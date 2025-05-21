      // Heatmap Chart (Simulated Feature Importance)
      const heatmapCtx = document.getElementById('heatmapChart').getContext('2d');
      new Chart(heatmapCtx, {
          type: 'bar',
          data: {
              labels: ['Age', 'Cholesterol', 'Blood Pressure', 'Heart Rate', 'Diabetes', 'Smoking'],
              datasets: [{
                  label: 'Feature Correlation (%)',
                  data: [85, 78, 82, 75, 69, 55],
                  backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40']
              }]
          },
          options: { responsive: true, maintainAspectRatio: false }
      });

      // F1 Score Chart
      const f1Ctx = document.getElementById('f1ScoreChart').getContext('2d');
      new Chart(f1Ctx, {
          type: 'line',
          data: {
              labels: ['Decision Tree', 'Random Forest', 'SVM', 'Neural Network'],
              datasets: [{
                  label: 'F1 Score',
                  data: [0.78, 0.85, 0.80, 0.92],
                  borderColor: '#ff9f40',
                  borderWidth: 3,
                  fill: false
              }]
          },
          options: { responsive: true, maintainAspectRatio: false }
      });

      // Pie Chart for Model Performance
      const pieCtx = document.getElementById('pieChart').getContext('2d');
      new Chart(pieCtx, {
          type: 'pie',
          data: {
              labels: ['Logistic Regression', 'SVM', 'Random Forest', 'Neural Network'],
              datasets: [{
                  data: [75, 80, 85, 90],
                  backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0']
              }]
          },
          options: { responsive: true, maintainAspectRatio: false }
      });

      // Bar Chart for Model Accuracy Comparison
      const barCtx = document.getElementById('barChart').getContext('2d');
      new Chart(barCtx, {
          type: 'bar',
          data: {
              labels: ['Logistic Regression', 'SVM', 'Random Forest', 'Neural Network'],
              datasets: [{
                  label: 'Accuracy (%)',
                  data: [78, 83, 88, 92],
                  backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0']
              }]
          },
          options: { responsive: true, maintainAspectRatio: false }
      });