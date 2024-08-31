import socket

from flask import Flask, redirect, request


matrixIds = {
    # Inputs
    "Kabel *space":         1,
    "Chromecast Main":      2,
    "Volumio":              3,
    "Chromecast Chillecke": 4,
    "Xbox Main":            8,

    # Outputs
    "BeamerSpace":              1, # A
    "LautsprecherChillecke":    3, # C
    "LautsprecherSpace":        6, # F
    "BeamerChillecke":          5, # E
    "Werkstatt":                7, # G
}

HOST = "172.22.35.189"
PORT = 5000

inputIds =  {
    "input1": 1,
    "input2": 2,
    "input3": 3,
    "input4": 4,
    "input5": 5,
    "input6": 6,
    "input7": 7,
    "input8": 8,
}

outputIds =  {
    "output1": 1, # A
    "output2": 2, # B
    "output3": 3, # C
    "output4": 4, # D
    "output5": 5, # E
    "output6": 6, # F
    "output7": 7, # G
    "output8": 8, # H
}

input1Label  = "Kabel *space"
input2Label  = "Chromecast Main"
input3Label  = "Voumeio"
input4Label  = "Chromecast Chillout"
input5Label  = ""
input6Label  = ""
input7Label  = ""
input8Label  = "Xbox Main"

output1Label = "Beamer *space"
output2Label = ""
output3Label = "Lautsprecher Chillout"
output4Label = ""
output5Label = "Beamer Chillout"
output6Label = "Lautsprecher *space"
output7Label = "Werkstatt"
output8Label = "Xbox Main"

app = Flask(__name__)


def switchInput(input, output):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(f"MT00SW{input:02d}{output:02d}NT"))


def requestMatrixState():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode("MT00RD0000NT"))

        data = ""
        while not data.endswith("END"):
            data += str(s.recv(1024), "ascii")
        return data


@app.route("/")
def index():
    matrixState             = requestMatrixState()
    #inputLautsprecherSpace  = int(matrixState.split(f"O{matrixIds['LautsprecherSpace']}I")[1][0])
    #inputBeamerSpace        = int(matrixState.split(f"O{matrixIds['BeamerSpace']}I")[1][0])
    #inputBeamerChillecke    = int(matrixState.split(f"O{matrixIds['BeamerChillecke']}I")[1][0])
    #inputWerkstatt          = int(matrixState.split(f"O{matrixIds['Werkstatt']}I")[1][0])

    currentInput1   = int(matrixState.split(f"O{outputIds['output1']}I")[1][0])
    currentInput2   = int(matrixState.split(f"O{outputIds['output2']}I")[1][0])
    currentInput3   = int(matrixState.split(f"O{outputIds['output3']}I")[1][0])
    currentInput4   = int(matrixState.split(f"O{outputIds['output4']}I")[1][0])
    currentInput5   = int(matrixState.split(f"O{outputIds['output5']}I")[1][0])
    currentInput6   = int(matrixState.split(f"O{outputIds['output6']}I")[1][0])
    currentInput7   = int(matrixState.split(f"O{outputIds['output7']}I")[1][0])
    currentInput8   = int(matrixState.split(f"O{outputIds['output8']}I")[1][0])

    return f"""
<!doctype html>
<html lang="en" data-bs-theme="dark">
    <head>
        <meta charset="utf8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>HDMI-Matrix</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    </head>

    <body>
        <div class="col-xl-2" style="margin-left: 1.5rem">
            <section id=content>
                <form action=/switch>
                    <div style="margin-top: 1rem; margin-bottom: 2rem">
                        <h3>Lautsprecher *space</h3>
                        <input type=submit name=output6 value=input1Label   class="btn {'btn-primary' if currentInput6 == inputIds['input1'] else 'btn-secondary'}" />
                        <input type=submit name=output6 value=input3Label   class="btn {'btn-primary' if currentInput6 == inputIds['input3'] else 'btn-secondary'}" />
                        <input type=submit name=output6 value=input2Label   class="btn {'btn-primary' if currentInput6 == inputIds['input2'] else 'btn-secondary'}" />
                        <input type=submit name=output6 value=input4Label   class="btn {'btn-primary' if currentInput6 == inputIds['input4'] else 'btn-secondary'}" />
                        <input type=submit name=output6 value=input8Label   class="btn {'btn-primary' if currentInput6 == inputIds['input8'] else 'btn-secondary'}" />
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>Beamer *space</h3>
                        <input type=submit name=output1 value=input1Label   class="btn {'btn-primary' if currentInput1 == inputIds['input1'] else 'btn-secondary'}" />
                        <input type=submit name=output1 value=input3Label   class="btn {'btn-primary' if currentInput1 == inputIds['input3'] else 'btn-secondary'}" />
                        <input type=submit name=output1 value=input2Label   class="btn {'btn-primary' if currentInput1 == inputIds['input2'] else 'btn-secondary'}" />
                        <input type=submit name=output1 value=input4Label   class="btn {'btn-primary' if currentInput1 == inputIds['input4'] else 'btn-secondary'}" />
                        <input type=submit name=output1 value=input8Label   class="btn {'btn-primary' if currentInput1 == inputIds['input8'] else 'btn-secondary'}" />
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>Beamer Chillecke</h3>
                        <input type=submit name=output5 value=input1Label   class="btn {'btn-primary' if currentInput5 == inputIds['input1'] else 'btn-secondary'}" />
                        <input type=submit name=output5 value=input3Label   class="btn {'btn-primary' if currentInput5 == inputIds['input3'] else 'btn-secondary'}" />
                        <input type=submit name=output5 value=input2Label   class="btn {'btn-primary' if currentInput5 == inputIds['input2'] else 'btn-secondary'}" />
                        <input type=submit name=output5 value=input4Label   class="btn {'btn-primary' if currentInput5 == inputIds['input4'] else 'btn-secondary'}" />
                        <input type=submit name=output5 value=input8Label   class="btn {'btn-primary' if currentInput5 == inputIds['input8'] else 'btn-secondary'}" />
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>Werkstatt</h3>
                        <input type=submit name=output7 value=input1Label   class="btn {'btn-primary' if currentInput7 == inputIds['input1'] else 'btn-secondary'}" />
                        <input type=submit name=output7 value=input3Label   class="btn {'btn-primary' if currentInput7 == inputIds['input3'] else 'btn-secondary'}" />
                        <input type=submit name=output7 value=input2Label   class="btn {'btn-primary' if currentInput7 == inputIds['input2'] else 'btn-secondary'}" />
                        <input type=submit name=output7 value=input4Label   class="btn {'btn-primary' if currentInput7 == inputIds['input4'] else 'btn-secondary'}" />
                        <input type=submit name=output7 value=input8Label   class="btn {'btn-primary' if currentInput7 == inputIds['input8'] else 'btn-secondary'}" />
                    </div>
                </form>
            </section>
        </div>
    </body>
</html>"""


@app.route("/switch")
def switch():
    if len(request.args) != 0:
        for output in request.args:
            input = request.args.get(output)
            #switchInput(matrixIds[input], matrixIds[output])
            switchInput(inputIds[input], outputIds[output])
            print(f"{input} -> {output}")

    return redirect("/")
