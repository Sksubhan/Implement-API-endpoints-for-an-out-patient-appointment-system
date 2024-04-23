from flask import Flask, jsonify, request
from datetime import datetime, timedelta
app = Flask(__name__)
doctors = [
    {
        "id": 1,
        "name": "Dr. John Doe",
        "specialization": "Cardiologist",
        "location": "Medical Center",
        "availability": {
            "Monday": ["18:00", "19:00", "20:00"],
            "Tuesday": ["18:00", "19:00", "20:00"],
            "Wednesday": ["18:00", "19:00", "20:00"],
            "Thursday": ["18:00", "19:00", "20:00"],
            "Friday": ["18:00", "19:00", "20:00"],
            "Saturday": ["18:00", "19:00", "20:00"]
        }
    },
    {
        "id": 2,
        "name": "Dr. Jane Smith",
        "specialization": "Pediatrician",
        "location": "Children's Hospital",
        "availability": {
            "Monday": ["18:00", "19:00", "20:00"],
            "Tuesday": ["18:00", "19:00", "20:00"],
            "Wednesday": ["18:00", "19:00", "20:00"],
            "Thursday": ["18:00", "19:00", "20:00"],
            "Friday": ["18:00", "19:00", "20:00"],
            "Saturday": ["18:00", "19:00", "20:00"]
        }
    }
]
appointments = []
@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"message": "Doctor not found"}), 404
@app.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_availability(doctor_id):
    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if doctor:
        return jsonify(doctor['availability'])
    else:
        return jsonify({"message": "Doctor not found"}), 404
@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    debugger_pin = data.get('debygger-pin') # please provide debugger pin to check my code
    if debugger_pin != DEBUGGER_PIN:
        return jsonify({"message": "Unauthorized"}), 401
    
    doctor_id = data.get('doctor_id')
    appointment_time = data.get('appointment_time')
    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404
    if appointment_time not in doctor['availability'].get(datetime.strptime(appointment_time, "%Y-%m-%d %H:%M").strftime("%A"), []):
        return jsonify({"message": "Appointment time not available"}), 400
    if datetime.strptime(appointment_time, "%Y-%m-%d %H:%M") < datetime.now():
        return jsonify({"message": "Appointment time must be in the future"}), 400
    if len([app for app in appointments if app['doctor_id'] == doctor_id and app['appointment_time'] == appointment_time]) >= doctor.get('max_appointments', 3):
        return jsonify({"message": "Doctor is fully booked for this time"}), 400
    appointments.append({
        "doctor_id": doctor_id,
        "appointment_time": appointment_time
    })
    return jsonify({"message": "Appointment booked successfully"}), 201
if __name__ == '__main__':
    app.run(debug=True)
