from flask import Flask, render_template, request, redirect, url_for, session
import secrets 
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort
import uuid
from flask import make_response


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Code d'accès unique
VALID_CODE = "B8K9Z-199394-XY72L"

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        user_code = request.form.get('code')
        if user_code == VALID_CODE:
            token = secrets.token_hex(8)
            session['authenticated'] = True
            session['access_token'] = token   # 🔁 clé cohérente avec /audio/<token>
            return redirect(url_for('single_access', token=token))
        else:
            error = "ACCESS DENIED"
    return render_template("home.html", error=error)

@app.route('/exclusive')
def exclusive():
    token = str(uuid.uuid4())
    session['access_token'] = token
    return render_template('interface.html', token=token)

@app.route('/audio/<token>')
def serve_audio(token):
    if token != session.get('access_token'):
        abort(403)

    session.pop('access_token', None)

    response = make_response(send_file('static/audio/TENSIA.mp3'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Génère un jeton unique par utilisateur/session
@app.route('/single')
def single_access():
    # Génère un token unique et le stocke en session
    token = str(uuid.uuid4())
    session['access_token'] = token
    return render_template('interface.html', token=token)

# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

