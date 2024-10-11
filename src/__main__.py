from flask import Flask,render_template,request,Response
from werkzeug.utils import secure_filename
import os
import subprocess
import re
import markdown
import uuid
import shutil
#sudo /home/sixsquare/analyse_web_python/.venv/bin/python /home/sixsquare/analyse_web_python/src/__main__.py
app = Flask(__name__,template_folder='html')

app.config['UPLOAD_FOLDER'] = './src/save_file'
app.config['SCRIPT_FOLDER'] = './src/scripts'

#目前有提供的服務
services = ['slither','static analyse','echidna','securify2','ConFuzzius','etainter','mythril']
#目前支援的版本
versions = ['0.8.25', '0.8.24', '0.8.23', '0.8.22', '0.8.21', '0.8.20', '0.8.19', '0.8.18', '0.8.17', '0.8.16', '0.8.15', '0.8.14', '0.8.13', '0.8.12', '0.8.11', '0.8.10', '0.8.9', '0.8.8', '0.8.7', '0.8.6', '0.8.5', '0.8.4', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.6', '0.7.5', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.7.0', '0.6.12', '0.6.11', '0.6.10', '0.6.9', '0.6.8', '0.6.7', '0.6.6', '0.6.5', '0.6.4', '0.6.3', '0.6.2', '0.6.1', '0.6.0', '0.5.17', '0.5.16', '0.5.15', '0.5.14', '0.5.13', '0.5.12', '0.5.11', '0.5.10', '0.5.9', '0.5.8', '0.5.7', '0.5.6', '0.5.5', '0.5.4', '0.5.3', '0.5.2', '0.5.1', '0.5.0', '0.4.26','0.4.25']
#每個對應的版本可以丟入的參數
#第一個位子是參數，後面的位子是他可以加的後綴，None表示可以自訂義輸入，如果只有參數表示不需要後綴
parameters = [
    #slither 參數選項
    [['--compile-force-framework','foundry', 'buidler', 'hardhat', 'truffle', 'waffle', 'solc', 'embark', 'dapp',
      'etherlime', 'etherscan', 'vyper', 'brownie', 'solc-json', 'standard', 'archive'],
     ['--compile-libraries',None],['--compile-remove-metadata'],['--compile-custom-build',None],['--skip-clean'],
     ['--ignore-compile'],
     ['--detect','abiencoderv2-array', 'arbitrary-send-erc20', 'arbitrary-send-erc20-permit',
      'arbitrary-send-eth', 'array-by-reference', 'controlled-array-length', 'assembly',
      'assert-state-change', 'backdoor', 'weak-prng', 'boolean-cst', 'boolean-equal', 'shadowing-builtin',
      'cache-array-length', 'codex', 'constant-function-asm', 'constant-function-state', 'pragma',
      'controlled-delegatecall', 'costly-loop', 'constable-states', 'immutable-states',
      'cyclomatic-complexity', 'dead-code', 'delegatecall-loop', 'deprecated-standards',
      'divide-before-multiply', 'domain-separator-collision', 'encode-packed-collision',
      'enum-conversion', 'external-function', 'function-init-state', 'erc20-interface',
      'erc721-interface', 'incorrect-exp', 'incorrect-return', 'solc-version', 'incorrect-equality',
      'incorrect-unary', 'incorrect-using-for', 'shadowing-local', 'locked-ether', 'low-level-calls',
      'mapping-deletion', 'events-access', 'events-maths', 'missing-inheritance', 'missing-zero-check',
      'incorrect-modifier', 'msg-value-loop', 'calls-loop', 'multiple-constructors', 'name-reused',
      'naming-convention', 'variable-scope', 'protected-vars', 'public-mappings-nested',
      'redundant-statements', 'reentrancy-benign', 'reentrancy-eth', 'reentrancy-events',
      'reentrancy-unlimited-gas', 'reentrancy-no-eth', 'return-bomb', 'return-leave', 'reused-constructor',
      'rtlo', 'shadowing-abstract', 'incorrect-shift', 'similar-names', 'shadowing-state', 'storage-array',
      'suicidal', 'tautological-compare', 'timestamp', 'too-many-digits', 'tx-origin', 'tautology',
      'unchecked-lowlevel', 'unchecked-send', 'unchecked-transfer', 'unimplemented-functions',
      'erc20-indexed', 'uninitialized-fptr-cst', 'uninitialized-local', 'uninitialized-state',
      'uninitialized-storage', 'unprotected-upgrade', 'unused-return', 'unused-state', 'var-read-using-this',
      'void-cst', 'write-after-write'],
        ['--exclude','abiencoderv2-array', 'arbitrary-send-erc20', 'arbitrary-send-erc20-permit',
      'arbitrary-send-eth', 'array-by-reference', 'controlled-array-length', 'assembly',
      'assert-state-change', 'backdoor', 'weak-prng', 'boolean-cst', 'boolean-equal', 'shadowing-builtin',
      'cache-array-length', 'codex', 'constant-function-asm', 'constant-function-state', 'pragma',
      'controlled-delegatecall', 'costly-loop', 'constable-states', 'immutable-states',
      'cyclomatic-complexity', 'dead-code', 'delegatecall-loop', 'deprecated-standards',
      'divide-before-multiply', 'domain-separator-collision', 'encode-packed-collision',
      'enum-conversion', 'external-function', 'function-init-state', 'erc20-interface',
      'erc721-interface', 'incorrect-exp', 'incorrect-return', 'solc-version', 'incorrect-equality',
      'incorrect-unary', 'incorrect-using-for', 'shadowing-local', 'locked-ether', 'low-level-calls',
      'mapping-deletion', 'events-access', 'events-maths', 'missing-inheritance', 'missing-zero-check',
      'incorrect-modifier', 'msg-value-loop', 'calls-loop', 'multiple-constructors', 'name-reused',
      'naming-convention', 'variable-scope', 'protected-vars', 'public-mappings-nested',
      'redundant-statements', 'reentrancy-benign', 'reentrancy-eth', 'reentrancy-events',
      'reentrancy-unlimited-gas', 'reentrancy-no-eth', 'return-bomb', 'return-leave', 'reused-constructor',
      'rtlo', 'shadowing-abstract', 'incorrect-shift', 'similar-names', 'shadowing-state', 'storage-array',
      'suicidal', 'tautological-compare', 'timestamp', 'too-many-digits', 'tx-origin', 'tautology',
      'unchecked-lowlevel', 'unchecked-send', 'unchecked-transfer', 'unimplemented-functions',
      'erc20-indexed', 'uninitialized-fptr-cst', 'uninitialized-local', 'uninitialized-state',
      'uninitialized-storage', 'unprotected-upgrade', 'unused-return', 'unused-state', 'var-read-using-this',
      'void-cst', 'write-after-write'],
        ['--exclude-dependencies'],['--exclude-optimization'],['--exclude-informational'],['--exclude-low'],
        ['--exclude-medium'],['--exclude-high'],['--fail-pedantic'],['--fail-low'],['--fail-medium'],['--fail-high'],
        ['--fail-none'],['--no-fail-pedantic'],['--show-ignored-findings']    
    ],
    #static analyse 參數選項
    [],
    #echidna 參數選項
    [["--test-mode","property","assertion","dapptest","optimization","overflow","exploration"],["--timeout",None],["--test-limit",None],["--rpc-url",None],["--shrink-limit",None],
     ["--seq-len",None],["--sender",None]],
    #securify2 參數選項
    [['--ignore-pragma'],['--use-patterns',None],['--exclude-patterns',None],['--include-severity',None],['--exclude-severity',None],['--from-blockchain',None]],
    #ConFuzzius 參數選項
    [['-a',None],['-c',None],['--evm',None],['-g',None],['-t',None],['-n',None],['-pc',None],['-pm',None],['--seed',None],['--rpc-host',None],['--rpc-port',None],['--data-dependency','0','1'],
     ['--constraint-solving','0','1'],['--environmental-instrumentation','0','1'],['--max-individual-length',None],['--max-symbolic-execution',None]],
    #etainter 參數選項
    [],
    #mythril 參數選項
    []
]


@app.route('/')
def home():
    return render_template('solidity_analyse.html',services=services,versions=versions,parameters=parameters)

#最後要記得避免自訂義的命令注入攻擊
@app.route('/analyse_file',methods=['POST'])
def analyse_file():
    try:
        file = request.files.get('file')
        if not file:
            return "No file provided", 200
        file_path, user_dir = save_user_file(file)
        # print("file_path is ",file_path,file)
        service = request.form.get('service')
        version = request.form.get('version')
        # print(service,version)
        param_names = [value for key, value in request.form.items() if key.startswith('paramName')]
        param_values = [request.form.get(f'paramValue{i}') for i, _ in enumerate(param_names)]
        custom_inputs = [request.form.get(f'customInput{i}') for i, _ in enumerate(param_names)]
        # print(param_names,param_values,custom_inputs)
        if service not in services or version not in versions:
            return "Invalid service or version specified", 200 
        else:
            #設定服務啟動位子與回傳報告
            try:
                args = parse_command_line_args(param_names, param_values, custom_inputs, service)
                if "Invalid" in args:
                    return Response(args, status=200)
                match service:
                    case 'slither':
                        script_name = "slither_analyse.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result:
                            index = result.stderr.find("INFO:Detectors:")
                            if index != -1:
                                contents = result.stderr[index:]
                                markdown_contents = markdown.markdown(contents)
                                return Response(markdown_contents, mimetype='text/markdown')
                            return Response("Please check if the Solidity version matches the contract or verify if there are any input errors in the parameters.\n\
                                            Here is the error message content.\n"+result.stderr, status=200)
                        else:
                            return Response("Failed to execute Slither analysis", status=200)
                    case 'static analyse':
                        try:
                            subprocess.run(["bash", "./src/StaticAnalyse/analyse.sh", file_path, version], check=True)

                            file_path = "./error-report.txt"
                            try:
                                with open(file_path, 'r') as file:
                                    contents = file.read()
                                os.remove(file_path)
                                return Response(contents, mimetype='text/markdown')
                            except IOError:
                                return Response("File not found", status=500)
                        except subprocess.CalledProcessError:
                            return Response("Failed to execute command", status=500)
                    case 'echidna':
                        script_name = "fuzzy_testing.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result is None:
                            return Response("Failed to execute echidna analysis", status=200)
                        result_path = os.path.join(user_dir,"result")
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                                markdown_contents = markdown.markdown(contents)
                            return Response(markdown_contents, mimetype='text/markdown')
                        except IOError:
                            return Response("Result file not found", status=200)
                    case 'securify2':
                        script_name = "securify2_analyse.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result is None:
                            return Response("Failed to execute securify2 analysis", status=200)
                        result_path = os.path.join(user_dir,"result")
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            contents = remove_ansi_codes(contents)
                            start_index = contents.find('Severity')
                            if start_index != -1:
                                markdown_contents = markdown.markdown(contents[start_index:])
                                return Response(markdown_contents, mimetype='text/markdown')
                            else:
                                return Response("Please check if the Solidity version matches the contract or verify if there are any input errors in the parameters.\n\
                                            Here is the error message content.\n"+result.stderr, status=200)
                        except IOError:
                            return Response("Result file not found", status=200)
                    case 'ConFuzzius':
                        script_name = "ConFuzzius_analyse.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result is None:
                            return Response("Failed to execute ConFuzzius analysis.\nPlease check if the Solidity version matches the contract or verify if there are any input errors in the parameters.", status=200)
                        result_path = os.path.join(user_dir,"result")
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                                lines = contents.splitlines()
                                contents = "\n".join(lines[:-6])
                                contents = remove_ansi_codes(contents)
                                markdown_contents = markdown.markdown(contents)
                            return Response(markdown_contents, mimetype='text/markdown')
                        except IOError:
                            return Response("Result file not found", status=200)
                    #只能丟bytecode
                    case 'etainter':
                        script_name = "etainter_analyse.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result is None:
                            return Response("Failed to execute etainter analysis.\nPlease check if the Solidity version matches the contract or verify if there are any input errors in the parameters.", status=200)
                        result_path = os.path.join(user_dir,"result")
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                            contents = remove_ansi_codes(contents)
                            markdown_contents = markdown.markdown(contents)
                            return Response(markdown_contents, mimetype='text/markdown')
                        except IOError:
                            return Response("Result file not found", status=200)
                    case 'mythril':
                        script_name = "mythril.sh"
                        copy_script(script_name, user_dir)
                        result = execute_command(["bash", script_name, file_path, version,args], cwd=user_dir)
                        if result is None:
                            return Response("Failed to execute echidna analysis", status=200)
                        result_path = os.path.join(user_dir,"result")
                        try:
                            with open(result_path, 'r') as file:
                                contents = file.read()
                                markdown_contents = markdown.markdown(contents)
                            return Response(markdown_contents, mimetype='text/markdown')
                        except IOError:
                            return Response("Result file not found", status=200)
            finally:
                if os.path.exists(user_dir):
                    shutil.rmtree(user_dir)
    except Exception as e:
        print(e)
        return "Please upload the file that need analysis!!!", 200

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
def remove_ansi_codes(text):
    return ansi_escape.sub('', text)

def save_user_file(file):
    user_id = str(uuid.uuid4())
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    os.makedirs(user_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(user_dir, filename)
    file.save(file_path)

    return file_path, user_dir

def copy_script(script_name, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
    script_path = os.path.join(app.config['SCRIPT_FOLDER'], script_name)
    shutil.copy(script_path, destination_dir)


def execute_command(command, cwd):
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        result.check_returncode()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
def find_service_index(service):
    try:
        index = services.index(service)
        return index
    except ValueError:
        return -1

def find_argument_index(available_parameters, argument):
    for index, param in enumerate(available_parameters):
        if param[0] == argument:
            return index
    return -1

def parse_command_line_args(param_names, param_values, custom_inputs, service):
    index = find_service_index(service)
    if index == -1:
        return "Invalid service."

    available_parameters = parameters[index]
    args = ""
    
    for i in range(len(param_names)):
        argument_index = find_argument_index(available_parameters, param_names[i])
        #param_names為空則跳過
        if param_names[i] == '':
            continue
        if argument_index == -1:
            return f"Invalid parameter option: {param_names[i]}."
        argument_array = available_parameters[argument_index]

        if param_values[i] is not None and custom_inputs[i] == "" and param_values[i] in argument_array:
            args += param_names[i] + " " + param_values[i] + " "
        elif param_values[i] =="null" and custom_inputs[i] != "" and None in argument_array:
            args += param_names[i] + " " + custom_inputs[i] + " "
        elif len(argument_array) == 1:
            args += param_names[i] + " "
        else:
            return f"Invalid parameter combination for: {param_names[i]}."

    return args
if __name__ == '__main__':
    app.run(debug=True)
