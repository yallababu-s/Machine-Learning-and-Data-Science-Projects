from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Load the pre-trained model
filename = 'Final_Model_Attrition_Prediction.sav'
model = pickle.load(open(filename, 'rb'))

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input features from form
        Age = int(request.form['Age'])
        EducationField = int(request.form['EducationField'])
        Department = int(request.form['Department'])
        MonthlyRate = int(request.form['MonthlyRate'])
        EnvironmentSatisfaction = int(request.form['EnvironmentSatisfaction'])
        JobInvolvement = int(request.form['JobInvolvement'])
        StandardHours = int(request.form['StandardHours'])
        PerformanceRating= int(request.form['PerformanceRating'])

        # Format the input data into a numpy array
        input_data = np.array([[Age, EducationField, Department, MonthlyRate, EnvironmentSatisfaction, JobInvolvement, StandardHours, PerformanceRating]])

        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        print(prediction)
        # Map prediction to result
        result = 'This employee will Attrition or quit his job in the future' if prediction[0] == 1 else 'This employee won’t Attrition or quit his job in the future'
        print(result)
        # Render the result in output.html
        return render_template('output.html', result=result)

    except Exception as e:
        # If any error occurs, log it and send a response
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    # Ensure it runs on the appropriate host and port
    app.run(host='0.0.0.0', port=8080, debug=True)