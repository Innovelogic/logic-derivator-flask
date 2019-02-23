import os , BooleanApplication
from flask import Flask,render_template,json, request
import hello

from BooleanApplication import *

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blogHome')
def blogHome():
    return render_template('blog-home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blogSingle')
def blogSingle():
    return render_template('blog-single.html')

@app.route('/portfolioDetails')
def portfolioDetails():
    return render_template('portfolio-details.html')

@app.route('/nlpUp', methods=['POST'])
def nlpUp():
    try:
        example_sentence = request.form['input']
        results = do_conversion(example_sentence)
        return render_template('blog-home.html', results=results)
        #return json.dumps({'results': results})
        # return json.dumps({'message': 'User created successfully !'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/upload', methods=['POST'])
def upload_file():

    try:
        print("H0")
        file = request.files['image']
        print("H1")
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(f)
        print("H2")
        file.save(f)
        print("H3")
        os.system('python hello.py')
        result = hello.vo
        print(result)
        print(file.filename)
        return render_template('blog-single.html', result=[file.filename,result])
        #return json.dumps({'results': results})
        # return json.dumps({'message': 'User created successfully !'})
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    app.run()
