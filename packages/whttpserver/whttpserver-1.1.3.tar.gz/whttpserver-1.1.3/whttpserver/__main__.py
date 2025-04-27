from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import os
import argparse
import stat
import pwd
import grp
import time
import stat

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['UPLOAD_FOLDER'] = '/data/'
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_filemode(st_mode):
    is_dir = 'd' if stat.S_ISDIR(st_mode) else '-'
    perm = ''
    for who in 'USR', 'GRP', 'OTH':
        for what in 'R', 'W', 'X':
            perm += what.lower() if st_mode & getattr(stat, 'S_I' + what + who) else '-'
    return is_dir + perm

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
        if entry.startswith('.'):
            continue
        path = os.path.join(directory, entry)
        stat_info = os.stat(path)
        permissions = get_filemode(stat_info.st_mode)
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
    html_output = "<table>"
    html_output += "<tr><th>Type</th><th>Permissions</th><th>Owner</th><th>Group</th><th>Size</th><th>Last Modified</th><th>Name</th></tr>"

    print("debug ",req_path)

    # Add directories to table
    for dir_info in directories:
        html_output += '''<tr style="color: blue;" ><td>dir</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><a href="/{}{}" style="color:blue;">{}</a></td></tr>'''.format(dir_info[0],dir_info[1],dir_info[2],dir_info[3],dir_info[4],req_path,dir_info[5],dir_info[5])

    # Add files to table
    for file_info in files:
        file_name = file_info[5]
        if file_name.split('.')[-1] in ['html', 'txt', 'sh', 'scala', 'py', 'js', 'css', 'json', 'md', 'yml', 'yaml', 'ini','log']:
            action = "edit"
        else:
            action = "download"
        html_output += '''<tr style="color: green;" >
            <td>File</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td><a style="color:green;" href="/{}/{}">{}</a></td>
        </tr>'''.format(file_info[0],file_info[1],file_info[2],file_info[3],file_info[4],action,req_path+file_name,file_name)

    html_output += "</table>"

    return html_output

@app.route('/edit/<path:filename>', methods=['GET', 'POST'])
def edit_file(filename):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if request.method == 'POST':
        # 保存文件内容
        new_content = request.form['content']
        with open(abs_path, 'w') as file:
            file.write(new_content)
        return redirect(url_for('dir_listing', req_path=os.path.dirname(filename)))
    
    # 读取文件内容
    with open(abs_path, 'r') as file:
        content = file.read()
    
    return render_template('edit_file.html', filename=filename, content=content, parent_path="/"+os.path.dirname(filename))

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    if req_path and not req_path.endswith('/'):
        req_path += '/'

    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        return 'Path not found'

    files_output = list_directory_contents(req_path, abs_path)
    dir1 = app.config['UPLOAD_FOLDER']
    the_path = dir1 +"/"+ req_path
    if the_path.startswith('//'): 
        the_path = the_path[1:]
        
    return '''
    <!doctype html>
    <style>
        table {
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 5px;
        }
    </style>
    <title>Directory listing for ''' + the_path + '''</title>
    <h1><a href="/">Home</a>  Directory listing for ''' + the_path + '''</h1>
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
    abs_parent_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return send_from_directory(abs_parent_path, req_path, as_attachment=True)

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
