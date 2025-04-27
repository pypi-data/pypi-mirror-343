from flask import Flask, request, send_from_directory
import os
import argparse
import stat
import pwd
import grp
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/data/'

def list_files(directory):
    try:
        return [{'name': f, 'is_dir': os.path.isdir(os.path.join(directory, f))} for f in os.listdir(directory)]
    except OSError:
        return []

def list_directory_contents(req_path, directory):
    entries = os.listdir(directory)
    directories = []
    files = []

    for entry in entries:
        path = os.path.join(directory, entry)
        stat_info = os.stat(path)
        permissions = stat.filemode(stat_info.st_mode)
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        group = grp.getgrgid(stat_info.st_gid).gr_name
        size = stat_info.st_size
        if size > 1024 * 1024 * 1024: 
            size = "%.2f GB" % (size/1024.0/1024.0/1024.0)
        elif size > 1024 * 1024:
            size = "%.2f MB" % (size/1024.0/1024.0)
        elif size > 1024:
            size = "%.2f KB" % (size/1024.0)
        else:
            size = "%.2f B" % (size)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_info.st_mtime))
        
        if os.path.isdir(path):
            directories.append((permissions, owner, group, size, mtime, entry))
        else:
            files.append((permissions, owner, group, size, mtime, entry))
    
    # Sort directories and files
    directories.sort(key=lambda x: x[-1])
    files.sort(key=lambda x: x[-1])

    # Create HTML table
    html_output = "<table border='1' style='border-collapse: collapse;'>"
    html_output += "<tr><th>Type</th><th>Permissions</th><th>Owner</th><th>Group</th><th>Size</th><th>Last Modified</th><th>Name</th></tr>"

    print("debug ",req_path)

    # Add directories to table
    for dir_info in directories:
        html_output += '''<tr style="color: blue;" ><td>Directory</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><a href="/{}{}" style="color:blue;">{}</a></td></tr>'''.format(dir_info[0],dir_info[1],dir_info[2],dir_info[3],dir_info[4],req_path,dir_info[5],dir_info[5])

    # Add files to table
    for file_info in files:
        html_output += '''<tr style="color: green;" >
            <td>File</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td><a style="color:green;" href="/download/{}">{}</a></td>
        </tr>'''.format(file_info[0],file_info[1],file_info[2],file_info[3],file_info[4],req_path+file_info[5],file_info[5])

    html_output += "</table>"

    return html_output

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    if req_path and not req_path.endswith('/'):
        req_path += '/'

    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        return 'Path not found'

    files_output = list_directory_contents(req_path, abs_path)
    return '''
    <!doctype html>
    <title>Directory listing for ''' + req_path + '''</title>
    <h1>Directory listing for ''' + req_path + '''</h1>
    <pre>''' + files_output + '''</pre>
    <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"></iframe>
    <form method="post" action="/upload?path='''+req_path+'''" enctype=multipart/form-data target="hidden_iframe" onsubmit="return addMessage();">
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

@app.route('/list/<path:req_path>')
def list_directory(req_path):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)
    return list_directory_contents(abs_path)

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument("--port", type=int, default=25000, help="Port to serve on")
    parser.add_argument("--dir", type=str, default="/data", help="Directory to serve")
    parser.add_argument("--debug", type=bool, default=True, help="Debug mode")
    args = parser.parse_args()
    app.config['UPLOAD_FOLDER'] = args.dir
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
    
if __name__ == '__main__':
    main()
