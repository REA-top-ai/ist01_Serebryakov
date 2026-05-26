import logging
import json
from flask import Flask, jsonify, render_template, session, redirect, request
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import ai
import config
import crud
import deck_api
import poker_math
from database import SessionLocal, init_db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
with open("auth_google.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

init_db()

google_auth = GoogleClient(
    client_id=data['web']["client_id"],
    client_secret=data['web']["client_secret"],
    redirect_uri="http://localhost:5050/google/oauth2callback",
)

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

@app.route('/')
def index():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    db = SessionLocal()
    try:
        return render_template('index.html',
                               total=crud.count_hands(db),
                               recent=crud.get_recent_hands(db, 8))
    finally:
        db.close()

@app.route("/google/")
def google_index():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
        
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/oauth2/v2/userinfo")
        
    r.raise_for_status()
    user_data = r.json()
    return f"Hello, {user_data.get('name')}!"

@app.route("/google/oauth2callback")
def google_oauth2callback():
    code= request.args.get("code")
    error = request.args.get("error")
    
    if error:
        return f"Error: {error}"
        
    if not code:
        return redirect(google_auth.authorize_url(
            scope=SCOPES,
            response_type="code",
        ))
        
    auth_data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    
    session["access_token"] = auth_data.get("access_token")
    return redirect("/")

@app.route('/analyzer')
def analyzer():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    return render_template('analyzer.html', card_images=deck_api.all_images())


@app.route('/history')
def history():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    db = SessionLocal()
    try:
        return render_template('history.html', records=crud.get_all_hands(db))
    finally:
        db.close()


@app.route('/history/<int:record_id>')
def history_detail(record_id):
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    db = SessionLocal()
    try:
        record = crud.get_hand(db, record_id)
        if record is None:
            return render_template('404.html'), 404
        return render_template('history_detail.html', record=record)
    finally:
        db.close()


@app.route('/analyze', methods=['POST'])
def analyze():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    data= request.get_json(force=True, silent=True) or {}
    hole =(data.get('hole_cards') or '').strip()
    board = (data.get('board') or '').strip()

    if not hole:
        return jsonify({'error': 'hole_cards is required'}), 400

    try:
        players = max(2, min(9, int(data.get('players') or 2)))
        pot = max(0.0, float(data.get('pot') or 0))
        bet = max(0.0, float(data.get('bet') or 0))
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid number: {e}'}), 400

    try:
        result = poker_math.analyze(hole, board, players, pot, bet)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    rec = ai.get_ai_recommendation(result)

    db = SessionLocal()
    try:
        hand_id = crud.create_hand(db, result, rec)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return jsonify({'ok': True, 'result': result, 'ai': rec, 'id': hand_id})

@app.errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    app.logger.exception('500: %s', e)
    return render_template('404.html'), 500

if __name__ == "__main__":
    app.run(
        host="localhost", port=5050,
        debug=True,
        use_reloader=False
    )