from flask import Flask, flash, request, redirect, url_for, render_template, Markup
import os
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from compressor import compressor

app = Flask(__name__, static_folder=join(dirname(realpath(__file__)), 'static/'))

# MEMBUAT DIR KALAU BELUM ADA
ORIGINAL_FOLDER = join(dirname(realpath(__file__)), 'static/original/')
os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
COMPRESSED_FOLDER = join(dirname(realpath(__file__)), 'static/compressed/')
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

app.secret_key = "pencitraan"
app.config['ORIGINAL_FOLDER'] = ORIGINAL_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER
app.config['PREFIX_COMP'] = "compressed_"
app.config['MAX_CONTENT_LENGTH'] = 120 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['bmp', 'dds', 'dib', 'eps', 'gif', 'icns', 'ico', 
'im', 'jpeg', 'jpg', 'msp', 'pcx', 'png', 'pbm', 'sgi', 'spi', 'tga', 
'tiff', 'webp', 'xbm'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def process_image():
    # GET REQUEST FILE DAN COMPRESSION RATE
    file = request.files['file']
    comprate = request.form.get('comp-rate', type=int)
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['ORIGINAL_FOLDER'], filename))

        # FUNGSI COMPRESSOR MENGEMBALIKAN DUA NILAI: "return (runtime, comprate)"
        runtime, comprate = compressor(app.config['ORIGINAL_FOLDER'], app.config['COMPRESSED_FOLDER'], filename, comprate, app.config['PREFIX_COMP'])
        runtime = round(runtime, 4)
        comprate = round(comprate, 2)
        
        return render_template('home.html', filename=filename, runtime=runtime, cprate=comprate)
    else:
        flash(Markup('Allowed image types are as specificied <a href="http://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html" target="_blank">here.</a>'))
        return redirect(request.url)

@app.route('/original/<filename>')
def display_org(filename):
    return redirect(url_for('static', filename='original/' + filename), code=301)

@app.route('/compressed/<filename>')
def display_comp(filename):
    return redirect(url_for('static', filename='compressed/' + app.config['PREFIX_COMP']+ filename), code=301)

@app.route('/how-to-use')
def howtouse():
    return render_template("howtouse.html")

@app.route('/about-us')
def aboutus():
    return render_template("aboutus.html")

if __name__ == "__main__":
    app.run(debug=True)
