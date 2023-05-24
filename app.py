from flask import Flask, render_template, request, url_for, redirect
import os
from face_comparer import FaceComparer
import cv2


app = Flask(__name__)
faceComparer = FaceComparer()



@app.route('/', methods=['GET', 'POST'])
def upload_photo():

    if request.method == 'POST':
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']
        
        # Save photo1 with original filename
        photo1_filename = photo1.filename
        photo1_path = os.path.join('./static/input/', photo1_filename)
        photo1.save(photo1_path)

        sqr_photo1 = faceComparer.get_drawn_face(photo1_path)
        photo1_path_output = os.path.join('./static/output/', photo1_filename)
        cv2.imwrite(photo1_path_output, sqr_photo1)
        
        # Save photo2 with original filename
        photo2_filename = photo2.filename
        photo2_path = os.path.join('./static/input/', photo2_filename)
        photo2.save(photo2_path)


        sqr_photo2 = faceComparer.get_drawn_face(photo2_path)
        photo2_path_output = os.path.join('./static/output/', photo2_filename)
        cv2.imwrite(photo2_path_output, sqr_photo2)


        # Get the URLs for the saved photos
        photo1_url = url_for('static', filename=f'output/{photo1_filename}')
        photo2_url = url_for('static', filename=f'output/{photo2_filename}')

        percen = faceComparer.compare_faces(photo1_path, photo2_path)
        
        return render_template('index.html', photo1_url=photo1_url, photo2_url=photo2_url, percen=percen)
    
    return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete_photos():
    if 'delete' in request.form and request.form['delete'] == 'true':
        input_dir = './static/input'
        output_dir = './static/output'

        # Delete photos in input directory
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Delete photos in output directory
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return redirect(url_for('upload_photo'))




if __name__ == '__main__':
    app.run(debug=True)
