from flask import Flask,render_template,request,Response
from werkzeug.utils import secure_filename
import os
import subprocess
import re
import markdown
#sudo /home/sixsquare/analyse_web_python/.venv/bin/python /home/sixsquare/analyse_web_python/src/__main__.py
app = Flask(__name__,template_folder='html')
#目前有提供的服務
services = ['slither','static analyse','echidna','securify2','ConFuzzius','etainter']
#目前支援的版本
versions = ['0.8.25', '0.8.24', '0.8.23', '0.8.22', '0.8.21', '0.8.20', '0.8.19', '0.8.18', '0.8.17', '0.8.16', '0.8.15', '0.8.14', '0.8.13', '0.8.12', '0.8.11', '0.8.10', '0.8.9', '0.8.8', '0.8.7', '0.8.6', '0.8.5', '0.8.4', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.6', '0.7.5', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.7.0', '0.6.12', '0.6.11', '0.6.10', '0.6.9', '0.6.8', '0.6.7', '0.6.6', '0.6.5', '0.6.4', '0.6.3', '0.6.2', '0.6.1', '0.6.0', '0.5.17', '0.5.16', '0.5.15', '0.5.14', '0.5.13', '0.5.12', '0.5.11', '0.5.10', '0.5.9', '0.5.8', '0.5.7', '0.5.6', '0.5.5', '0.5.4', '0.5.3', '0.5.2', '0.5.1', '0.5.0', '0.4.26','0.4.25']
#每個對應的版本可以丟入的參數
#第一個位子是參數，後面的位子是他可以加的後綴，None表示可以自訂義輸入，如果只有參數表示不需要後綴
arguments = [
    #slither 參數選項
    [['--compile-force-framework','truffle',None],['--compile-libraries',None],['--compile-remove-metadata'],
     ['--compile-custom-build',None],['--skip-clean'],
    ],
    #static analyse 參數選項
    [],
    #echidna 參數選項
    [['-d'],['-e',None],['-f','f_suffix1','f_suffix2','f_suffix3','f_suffix4'],['-g','g_suffix1','g_suffix2','g_suffix3','g_suffix4',None]],
    #securify2 參數選項
    [],
    #ConFuzzius 參數選項
    [],
    #etainter 參數選項
    [],
    #manticore 參數選項
    []
]
@app.route('/')
def home():
    return render_template('solidity_analyse.html',services=services,versions=versions,arguments=arguments)

#最後要記得避免自訂義的命令注入攻擊
@app.route('/analyse_file',methods=['POST'])
def analyse_file():
    try:
        file = request.files.get('file')
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('./src/save_file', filename))
            file_path = f'./src/save_file/{filename}'
        service = request.form.get('service')
        version = request.form.get('version')
        # print(service,version)
        param_names = [value for key, value in request.form.items() if key.startswith('paramName')]
        param_values = [request.form.get(f'paramValue{i}') for i, _ in enumerate(param_names)]
        custom_inputs = [request.form.get(f'customInput{i}') for i, _ in enumerate(param_names)]
        print(param_names,param_values,custom_inputs)
        if service not in services:
            return "Service part found in services list", 200
        elif version not in versions:
            return "version part found in versions list", 200
        else:
            #設定服務啟動位子與回傳報告
            match service:
                case 'slither':
                    try:
                        result = subprocess.run(
                            ["bash", "./slither_analyse.sh", file_path, version],
                            cwd="./src/slither/",  
                            capture_output=True,  
                            text=True  
                        )
                        result.check_returncode()
                        index = result.stderr.find("INFO:Detectors:")
                        if index != -1:
                            contents = result.stderr[index:]
                            markdown_contents = markdown.markdown(contents)
                            return Response(markdown_contents, mimetype='text/markdown')
                        else:
                            return Response("Slither report processing error", status=500)
                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")
                        return Response(str(e), status=500)
                case 'static analyse':
                    try:
                        subprocess.run(["bash", "./src/StaticAnalyse/analyse.sh", file_path, version], check=True)

                        file_path = "./error-report.txt"
                        try:
                            with open(file_path, 'r') as file:
                                contents = file.read()
                            os.remove(file_path)
                            return Response(contents, mimetype='text/plain')
                        except IOError:
                            return Response("File not found", status=500)
                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)
                case 'echidna':
                    try:
                        subprocess.run(
                            ["bash", "./fuzzy_testing.sh", file_path, version],
                            cwd="./src/echinda/",
                            check=True
                        )

                        result_path = "./src/echinda/result"
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            os.remove(result_path)
                            return Response(contents, mimetype='text/plain')
                        except IOError:
                            return Response("File not found", status=500)

                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)

                    except Exception as e:
                        return Response(str(e), status=500)
                case 'securify2':
                    try:
                        subprocess.run(
                            ["bash", "./securify2_analyse.sh", file_path, version],
                            cwd="./src/securify/",
                            check=True
                        )
                        result_path = "./src/securify/result"
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            os.remove(result_path)
                            contents = remove_ansi_codes(contents)
                            start_index = contents.find('Severity')
                            if start_index != -1:
                                return Response(contents[start_index:], mimetype='text/plain')
                            return Response("No vulnerabilities found in the contract.", status=500)
                        except IOError:
                            return Response("File not found", status=500)
                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)
                    except Exception as e:
                        return Response(str(e), status=500)
                case 'ConFuzzius':
                    try:
                        result = subprocess.run(
                            ["bash", "./ConFuzzius_analyse.sh", file_path, version],
                            cwd="./src/ConFuzzius/",
                            check=True
                        )
                        result_path = "./src/ConFuzzius/result"
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            os.remove(result_path)
                            return Response(contents, mimetype='text/plain')
                            
                        except IOError:
                            return Response("File not found", status=500)
                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)
                    except Exception as e:
                        return Response(str(e), status=500)
                #只能丟bytecode
                case 'etainter':
                    try:
                        result = subprocess.run(
                            ["bash", "./etainter_analyse.sh", file_path, version],
                            cwd="./src/etainter/",
                            check=True
                        )
                        print("Output:", result.stdout)
                        print("Errors:", result.stderr)
                        result_path = "./src/etainter/result"
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            os.remove(result_path)
                            return Response(contents, mimetype='text/plain')
                            
                        except IOError:
                            return Response("File not found", status=500)
                    except subprocess.CalledProcessError:
                        return Response("Failed to execute command", status=500)
                    except Exception as e:
                        return Response(str(e), status=500)
    except Exception as e:
        print(e)
        return "Please upload the file that need analysis!!!", 200

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
def remove_ansi_codes(text):
    return ansi_escape.sub('', text)



if __name__ == '__main__':
    app.run(debug=True)
