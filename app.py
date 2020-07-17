from flask import Flask,request, render_template, Markup
import json
import chardet

app = Flask(__name__)
app.config.from_object("config.Config")

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 


@app.errorhandler(Exception)
def handle_exception(exception):
    return render_template('exception.html',exception=exception)


@app.route('/')
def render_file_data():
   
    filename=request.args.get('filename', default = 'file1.txt', type = str)

    file_obj = open('./files/'+filename, "rb")
    file_data=file_obj.read()

    start_range=request.args.get('start_range', default = 0, type = int)
    end_range=request.args.get('end_range', default = len(file_data), type = int)

    if start_range>len(file_data) or end_range>len(file_data) or (start_range<0 and end_range<0):
        raise Exception('Line number is not in valid range')

    encoding_type=chardet.detect(file_data)
    if encoding_type['encoding']!='ascii':
        file_data=file_data.decode(encoding_type['encoding'])
        file_data=file_data.split('\n')
        new_list=file_data[start_range:end_range]
        file_data=''.join(new_list)
    else:
        file_data=file_data.decode('utf-8')
        file_data=file_data.split('\n')
        new_list=file_data[start_range:end_range]
        file_data=''.join(new_list)
    return render_template('index.html',data=file_data,file=filename,start=start_range,end=end_range)
    


if __name__ == '__main__':
    app.run(debug=True)
    


