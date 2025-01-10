from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize session data
@app.before_request
def initialize_session():
    if 'total_carbon' not in session:
        session['total_carbon'] = 0
    if 'points' not in session:
        session['points'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        activity = request.form['activity']
        if activity == 'commute':
            mode = request.form['mode']
            distance = float(request.form['distance'])
            if mode == 'car':
                carbon_emission = distance * 0.24
            elif mode == 'bike':
                carbon_emission = 0
                session['points'] += 10
            elif mode == 'public_transit':
                carbon_emission = distance * 0.05
                session['points'] += 5
            session['total_carbon'] += carbon_emission

        elif activity == 'electricity':
            kwh = float(request.form['kwh'])
            carbon_emission = kwh * 0.5
            session['total_carbon'] += carbon_emission
            if kwh < 100:
                session['points'] += 15

        elif activity == 'shopping':
            eco_friendly = request.form.get('eco_friendly') == 'yes'
            if eco_friendly:
                session['points'] += 5

        return redirect(url_for('summary'))

    return render_template('track.html')

@app.route('/summary')
def summary():
    return render_template('summary.html', 
                           total_carbon=session['total_carbon'], 
                           points=session['points'])

if __name__ == '__main__':
    app.run(debug=True)