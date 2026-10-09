from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurarea bazei de date SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configurarea Google Gemini API
# ÎNLOCUIEȘTE cu cheia ta reală generată pe Google AI Studio
genai.configure(api_key="-")


# ==========================================
# 1. MODELUL BAZEI DE DATE
# ==========================================
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Saved')  # Saved, Applied, Screening, Interview, Offer, Rejected
    date_applied = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'role': self.role,
            'status': self.status,
            'date_applied': self.date_applied,
            'notes': self.notes
        }


# Crearea bazei de date dacă nu există
with app.app_context():
    db.create_all()


# ==========================================
# 2. RUTE PENTRU INTERFAȚĂ ȘI CRUD
# ==========================================

@app.route('/')
def index():
    # Randează interfața principală (index.html)
    return render_template('index.html')


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    # Returnează toate joburile
    jobs = JobApplication.query.order_by(JobApplication.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])


@app.route('/api/jobs', methods=['POST'])
def add_job():
    # Adaugă un job nou
    data = request.json
    new_job = JobApplication(
        company=data['company'],
        role=data['role'],
        status=data.get('status', 'Applied'),
        date_applied=data.get('date_applied', ''),
        notes=data.get('notes', '')
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    # Actualizează un job existent (ex: schimbare status)
    job = JobApplication.query.get_or_404(job_id)
    data = request.json

    job.company = data.get('company', job.company)
    job.role = data.get('role', job.role)
    job.status = data.get('status', job.status)
    job.date_applied = data.get('date_applied', job.date_applied)
    job.notes = data.get('notes', job.notes)

    db.session.commit()
    return jsonify(job.to_dict())


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    # Șterge un job
    job = JobApplication.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job șters cu succes'})


# ==========================================
# 3. RUTA PENTRU AI INSIGHTS
# ==========================================
@app.route('/api/ai-insight', methods=['POST'])
def get_ai_insight():
    data = request.json
    description = data.get('description', '')

    if not description:
        return jsonify({'error': 'Te rog să introduci o descriere a jobului!'}), 400

    # Promptul către AI
    prompt = f"""
    Ești un expert în recrutare (HR). Analizează următoarea descriere de job și extrage o listă clară formatată frumos (folosește bullet points) cu:
    1. Skill-uri tehnice (Hard skills) principale cerute.
    2. Soft skills cerute.
    3. Un scurt sfat despre ce ar trebui să evidențieze candidatul în CV pentru acest rol.

    Descrierea jobului:
    {description}
    """

    try:
        # Înlocuiește linia veche cu modelul nou cerut:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        return jsonify({'insight': response.text})
    except Exception as e:
        return jsonify({'error': f'Eroare la conectarea cu AI: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)