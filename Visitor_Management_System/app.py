from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import qrcode, io, base64, pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    whom_to_meet = db.Column(db.String(100), nullable=False)
    photo_data = db.Column(db.Text, nullable=True)
    entry_time = db.Column(db.DateTime, default=datetime.now)
    exit_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), default='IN')

BLACKLIST = ['9999999999', '8888888888']

with app.app_context():
    db.create_all()

def generate_qr(data):
    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('ascii')

@app.route('/')
def index():
    active_visitors = Visitor.query.filter_by(status='IN').all()
    overstay_ids = [v.id for v in active_visitors if v.entry_time < (datetime.now() - timedelta(hours=4))]
    total_today = Visitor.query.filter(db.func.date(Visitor.entry_time) == db.func.date(datetime.now())).count()
    return render_template('index.html', visitors=active_visitors, total=total_today, current=len(active_visitors), overstays=overstay_ids)

@app.route('/register', methods=['POST'])
def register():
    phone = request.form.get('phone')
    if phone in BLACKLIST:
        return "<h1 style='color:red; text-align:center; font-family:sans-serif;'>ACCESS DENIED: Number Blacklisted.</h1>"

    new_v = Visitor(
        name=request.form.get('name'), phone=phone,
        whom_to_meet=request.form.get('whom'),
        photo_data=request.form.get('photo_data')
    )
    db.session.add(new_v)
    db.session.commit()
    print(f"NOTIFICATION: {new_v.whom_to_meet} alerted of guest {new_v.name}.")
    return redirect(url_for('view_pass', id=new_v.id))

@app.route('/pass/<int:id>')
def view_pass(id):
    visitor = Visitor.query.get_or_404(id)
    qr = generate_qr(f"EXIT_ID_{visitor.id}")
    return render_template('pass.html', visitor=visitor, qr_code=qr)

@app.route('/logs')
def logs():
    q = request.args.get('search')
    visits = Visitor.query.filter(Visitor.name.contains(q) | Visitor.phone.contains(q)).all() if q else Visitor.query.order_by(Visitor.entry_time.desc()).all()
    return render_template('logs.html', visits=visits)

@app.route('/checkout/<int:id>')
def checkout(id):
    v = Visitor.query.get(id)
    if v:
        v.exit_time, v.status = datetime.now(), 'OUT'
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/export')
def export():
    data = Visitor.query.all()
    df = pd.DataFrame([(v.id, v.name, v.phone, v.entry_time, v.exit_time) for v in data], columns=['ID', 'Name', 'Phone', 'In', 'Out'])
    return Response(df.to_csv(index=False), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=logs.csv"})

if __name__ == '__main__':
    # host='0.0.0.0' allows access from mobile devices on the same Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)