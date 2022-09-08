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
        weight = float(request.form['weight'])
        gender = request.form['gender'][0].upper()
        height = int(request.form['height'])
        date_of_birth = datetime.strptime(request.form['date_of_birth'], "%Y-%m-%d")

        user = FitwellUser.get_user_byEmail(email)

        if Auth.register(
            user=user,
            email=email,
            password=password,
            weight=weight,
            gender=gender,
            height=height,
            date_of_birth=date_of_birth
        ):
            return jsonify({'url': url_for('index')})
        else:
            flash('* User already exists')
            return jsonify({'url': url_for('register')})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = FitwellUser.get_user_byEmail(email)

        if Auth.login(user, password):
            return jsonify({'url': url_for('log')})
        else:
            flash('* Please check your login details and try again')
            return jsonify({'url': url_for('index')})
        
@app.route('/log', methods=['GET', 'POST'])
@login_required
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

        activity_calories_consumed = FitwellLog.calculate_activities_calories(
            weight=weight,
            walking_duration=walking_duration,
            running_duration=running_duration,
            swimming_duration=swimming_duration,
            bicycling_duration=bicycling_duration
        )

        email = current_user.get_id()

        new_log = FitwellLog(email, date_time, weight, walking_duration, running_duration, \
        swimming_duration, bicycling_duration, activity_calories_consumed)

        return jsonify({'activity_calories_consumed': round(activity_calories_consumed, 2)})

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

    elif request.method == 'POST':
        return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    elif request.method == 'POST':
        data = json.loads(request.form['json_data'])

        for record in data:
            email = record['email']
            date_time = record['datetime']
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
            weight = float(record['weight'])
            walking_duration = int(record['walking'])
            running_duration = int(record['running'])
            swimming_duration = int(record['swimming'])
            bicycling_duration = int(record['bicycling'])

            activity_calories_consumed = FitwellLog.calculate_activities_calories(
                weight=weight,
                walking_duration=walking_duration,
                running_duration=running_duration,
                swimming_duration=swimming_duration,
                bicycling_duration=bicycling_duration
            )

            email = email

            new_log = FitwellLog(email, date_time, weight, walking_duration, running_duration, \
            swimming_duration, bicycling_duration, activity_calories_consumed)
        
        return jsonify({'url': url_for('upload')})
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/database')
@login_required
def database():
    email = current_user.get_id()
    json_data = FitwellLog.get_datetime_calories(email=email)
    return json_data

if __name__ == "__main__":
    app.run(debug=True)