from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/data/'

def list_files(directory):
    try:
        return [{'name': f, 'is_dir': os.path.isdir(os.path.join(directory, f))} for f in os.listdir(directory)]
    except OSError:
        return []

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    if req_path and not req_path.endswith('/'):
        req_path += '/'

    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        return 'Path not found'

    files = list_files(abs_path)

    if os.path.isfile(abs_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], req_path, as_attachment=True)

    return '''
    <!doctype html>
    <title>Directory listing for {}</title>
    <h1>Directory listing for {}</h1>
    <ul style="list-style-type: decimal;">
    '''.format(req_path, req_path) + ''.join(
        '<li><a href="/{}{}" style="color:blue;">{}</a></li>'.format(req_path, f['name'], f['name']) if f['is_dir'] else '<li><a href="/download/{}{}" style="color:green;">{}</a></li>'.format(req_path, f['name'], f['name']) for f in files) + '''
    </ul>
    <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"></iframe>
    <form method="post" action="/upload?path='''+req_path+'''" enctype="multipart/form-data" target="hidden_iframe" onsubmit="return addMessage();">
      <input type=file name=file>
      <input type=submit value=Upload onclick="showUploadingMessage();">
    </form>
    <div id="messages"></div>
    <div id="uploadingMessage" style="display:none;">Uploading...</div>
    <script type="text/javascript">
        function showUploadingMessage() {
            document.getElementById('uploadingMessage').style.display = 'block';
        }

        function addMessage() {
            var iframe = document.getElementById('hidden_iframe');
            iframe.onload = function() {
                var content = iframe.contentDocument || iframe.contentWindow.document;
                var message = content.body.innerHTML;
                var messagesDiv = document.getElementById('messages');
                messagesDiv.innerHTML += '<p>' + message + '</p>';
                document.getElementById('uploadingMessage').style.display = 'none';
            };
            return true;
        }
    </script>
    '''

@app.route('/download/<path:req_path>')
def download_file(req_path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], req_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    req_path = request.args.get('path', '')
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file.save(os.path.join(abs_path, filename))
        return 'File uploaded successfully to: {}'.format(os.path.join(abs_path, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25000, debug=True)
