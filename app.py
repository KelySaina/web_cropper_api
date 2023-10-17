from flask import Flask, request, jsonify, render_template, send_file
from datetime import date
from flask_cors import CORS
import os
from flask import send_from_directory
from modules.cropper import Cropper
from modules.archive import ArchiveFiles
from modules.toImage import toImgClass

import shutil

app = Flask(__name__)
CORS(app)

# Use os.path.join for file paths
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "imagesUploaded")
app.config['CROPPED_FOLDER'] = os.path.join(os.getcwd(), "imagesCropped")

global_orig = ''


@app.route('/')
def home():
    return "Welcome Cropper API KelySaina"


@app.route('/imagesUploaded/<path:filename>')
def croppedd_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/imagesCropped/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['CROPPED_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    today_date = date.today().strftime("%Y-%m-%d")
    host = '127.0.0.1'

    if 'image' not in request.files:
        return 'No file part'

    file = request.files['image']

    if file.filename == '':
        return 'No selected file'

    if file:
        global global_orig
        output_directory = os.path.join(
            app.config['UPLOAD_FOLDER'], today_date)
        os.makedirs(output_directory, exist_ok=True)
        file.save(os.path.join(output_directory, file.filename))

        fileN, file_extension = os.path.splitext(file.filename)

        if file_extension.lower() == '.pdf':
            i = toImgClass()
            fn = i.fromPDF(os.path.join(output_directory, file.filename))
            imgFromPDFName = f"{fileN}.png"
            uploaded_url = f'http://{host}:5000/imagesUploaded/{today_date}/{imgFromPDFName}'

            global_orig = os.path.join(output_directory, imgFromPDFName)
        else:
            fn = file.filename
            uploaded_url = f'http://{host}:5000/imagesUploaded/{today_date}/{fn}'

            global_orig = os.path.join(output_directory, fn)

        return jsonify({"url": uploaded_url, 'msg': 'uploaded'})


@app.route('/crop', methods=['POST'])
def crop_file():
    filename = request.form['name']

    if not filename:
        print('no')

    file_name, file_extension = os.path.splitext(filename)

    fn, file_extension = os.path.splitext(filename)

    if file_extension.lower() == '.pdf':
        fn = f"{fn}.png"
    else:
        fn = f"{fn}{file_extension}"

    today_date = date.today().strftime("%Y-%m-%d")

    output_directory = os.path.join(
        os.getcwd(), f"imagesCropped/{today_date}/{file_name}/")
    get_directory = os.path.join(os.getcwd(), f"imagesUploaded/{today_date}/")

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory, exist_ok=True)

    treat_url = os.path.join(get_directory, fn)

    c = Cropper()

    return jsonify({"urls": c.cropper(treat_url)})


@app.route('/process_items', methods=['POST'])
def process_items():
    items = request.json.get('items')

    if items:
        exist_check = all(os.path.exists(item) for item in items)

        if exist_check:
            directory = os.path.dirname(items[0])
            filenames = [os.path.basename(item) for item in items]
            a = ArchiveFiles()

            archive_path = a.archive_files(filenames, global_orig, directory)

            if archive_path != 'No files to archive':
                return jsonify({"archive_path": archive_path, "msg": 'archived'})
            else:
                return jsonify({"msg": 'No files to archive.'})
        else:
            return jsonify({"msg": 'Some or all items do not exist on the server.'})
    else:
        return jsonify({"msg": 'No items received. Please provide items in the request.'})


@app.route('/get_archive/<path:archive_path>')
def get_items(archive_path):
    return send_file(archive_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
