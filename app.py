from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from PIL import Image
from io import BytesIO
import rembg

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File Uploaded', 'error')
            return redirect(url_for('upload_file'))
        file = request.files['file']
        if file.filename == '':
            flash('No File Selected', 'error')
            return redirect(url_for('upload_file'))
        if file:
            try:
                input_image = Image.open(file.stream)
                output_image = rembg.remove(input_image, alpha_matte=True)

                img_io = BytesIO()
                output_image.save(img_io, 'PNG')
                img_io.seek(0)

                return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='_rmbg.png')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(url_for('upload_file'))

    return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True, port=5100)
