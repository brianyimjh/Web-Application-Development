from init import *

app = create_app()

# Route to the relevant webpage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        weight = request.form['weight']
        gender = request.form['gender']
        print(f"Email: {email}\nPassword: {password}\nWeight: {weight}\nGender: {gender}")

        return jsonify({'email': email, 'password': password, 'weight': weight, 'gender': gender})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Email: {email}\nPassword: {password}")
        
        return jsonify({'email': email, 'password': password})

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('log.html')

    elif request.method == 'POST':
        date_time = request.form['date_time']
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
        weight = float(request.form['weight'])
        walking_duration = int(request.form['walking_duration'])
        running_duration = int(request.form['running_duration'])
        swimming_duration = int(request.form['swimming_duration'])
        bicycling_duration = int(request.form['bicycling_duration'])

        walking_calorie_consumed = 0.084
        running_calorie_consumed = 0.21
        swimming_calorie_consumed = 0.13
        bicycling_calorie_consumed = 0.064

        total_calories_consumed = round((walking_calorie_consumed*walking_duration + \
        running_calorie_consumed*running_duration + \
        swimming_calorie_consumed*swimming_duration + \
        bicycling_calorie_consumed*bicycling_duration) * \
        weight, 2)

        new_log = FitwellLog(date_time, weight, walking_duration, running_duration, swimming_duration, bicycling_duration, total_calories_consumed)

        return jsonify({'total_calories_consumed': total_calories_consumed})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

    elif request.method == 'POST':
        return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    elif request.method == 'POST':
        email = request.form['email']
        date_time = request.form['datetime']
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
        weight = float(request.form['weight'])
        walking = int(request.form['walking'])
        running = int(request.form['running'])
        swimming = int(request.form['swimming'])
        bicycling = int(request.form['bicycling'])

        walking_calorie_consumed = 0.084
        running_calorie_consumed = 0.21
        swimming_calorie_consumed = 0.13
        bicycling_calorie_consumed = 0.064

        total_calories_consumed = round((walking_calorie_consumed*walking + \
        running_calorie_consumed*running + \
        swimming_calorie_consumed*swimming + \
        bicycling_calorie_consumed*bicycling) * \
        weight, 2)

        new_log = FitwellUpload(email, date_time, weight, walking, running, swimming, bicycling, total_calories_consumed)
        
        return render_template('upload.html')
        
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/database')
def database():
    json_data = FitwellUpload.get_datetime_calories()
    return json_data

if __name__ == "__main__":
    app.run(debug=True)