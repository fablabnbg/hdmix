import socket

from flask import Flask, redirect, request


HOST = "172.22.35.189"
PORT = 5000

inputIds =  {
    "in1": 1,
    "in2": 2,
    "in3": 3,
    "in4": 4,
    "in5": 5,
    "in6": 6,
    "in7": 7,
    "in8": 8,
}

outputIds =  {
    "outA": 1,
    "outB": 2,
    "outC": 3,
    "outD": 4,
    "outE": 5,
    "outF": 6,
    "outG": 7,
    "outH": 8,
}

in1Label  = "Kabel *space"
in2Label  = "Chromecast Main"
in3Label  = "Volumio"
in4Label  = "Chromecast Chillout"
in5Label  = ""
in6Label  = ""
in7Label  = ""
in8Label  = "Xbox Main"

outALabel = "Beamer *space"
outBLabel = ""
outCLabel = "Lautsprecher Chillout"
outDLabel = ""
outELabel = "Beamer Chillout"
outFLabel = "Lautsprecher *space"
outGLabel = "Werkstatt"
outHLabel = "Xbox Main"

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
    currentInput1   = int(matrixState.split(f"O{outputIds['outA']}I")[1][0])
    currentInput2   = int(matrixState.split(f"O{outputIds['outB']}I")[1][0])
    currentInput3   = int(matrixState.split(f"O{outputIds['outC']}I")[1][0])
    currentInput4   = int(matrixState.split(f"O{outputIds['outD']}I")[1][0])
    currentInput5   = int(matrixState.split(f"O{outputIds['outE']}I")[1][0])
    currentInput6   = int(matrixState.split(f"O{outputIds['outF']}I")[1][0])
    currentInput7   = int(matrixState.split(f"O{outputIds['outG']}I")[1][0])
    currentInput8   = int(matrixState.split(f"O{outputIds['outH']}I")[1][0])

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
                        <h3>"{outFLabel}"</h3>
                        <button type=submit name=outF value=in1 class="btn {'btn-primary' if currentInput6 == inputIds['in1'] else 'btn-secondary'}">{in1Label}</button>
                        <button type=submit name=outF value=in3 class="btn {'btn-primary' if currentInput6 == inputIds['in3'] else 'btn-secondary'}">{in3Label}</button>
                        <button type=submit name=outF value=in2 class="btn {'btn-primary' if currentInput6 == inputIds['in2'] else 'btn-secondary'}">{in2Label}</button>
                        <button type=submit name=outF value=in4 class="btn {'btn-primary' if currentInput6 == inputIds['in4'] else 'btn-secondary'}">{in4Label}</button>
                        <button type=submit name=outF value=in8 class="btn {'btn-primary' if currentInput6 == inputIds['in8'] else 'btn-secondary'}">{in8Label}</button>
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>"{outALabel}"</h3>
                        <button type=submit name=outA value=in1 class="btn {'btn-primary' if currentInput1 == inputIds['in1'] else 'btn-secondary'}">{in1Label}</button>
                        <button type=submit name=outA value=in3 class="btn {'btn-primary' if currentInput1 == inputIds['in3'] else 'btn-secondary'}">{in3Label}</button>
                        <button type=submit name=outA value=in2 class="btn {'btn-primary' if currentInput1 == inputIds['in2'] else 'btn-secondary'}">{in2Label}</button>
                        <button type=submit name=outA value=in4 class="btn {'btn-primary' if currentInput1 == inputIds['in4'] else 'btn-secondary'}">{in4Label}</button>
                        <button type=submit name=outA value=in8 class="btn {'btn-primary' if currentInput1 == inputIds['in8'] else 'btn-secondary'}">{in8Label}</button>
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>"{outELabel}"</h3>
                        <button type=submit name=outE value=in1 class="btn {'btn-primary' if currentInput5 == inputIds['in1'] else 'btn-secondary'}">{in1Label}</button>
                        <button type=submit name=outE value=in3 class="btn {'btn-primary' if currentInput5 == inputIds['in3'] else 'btn-secondary'}">{in3Label}</button>
                        <button type=submit name=outE value=in2 class="btn {'btn-primary' if currentInput5 == inputIds['in2'] else 'btn-secondary'}">{in2Label}</button>
                        <button type=submit name=outE value=in4 class="btn {'btn-primary' if currentInput5 == inputIds['in4'] else 'btn-secondary'}">{in4Label}</button>
                        <button type=submit name=outE value=in8 class="btn {'btn-primary' if currentInput5 == inputIds['in8'] else 'btn-secondary'}">{in8Label}</button>
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>"{outGLabel}"</h3>
                        <button type=submit name=outG value=in1 class="btn {'btn-primary' if currentInput7 == inputIds['in1'] else 'btn-secondary'}">{in1Label}</button>
                        <button type=submit name=outG value=in3 class="btn {'btn-primary' if currentInput7 == inputIds['in3'] else 'btn-secondary'}">{in3Label}</button>
                        <button type=submit name=outG value=in2 class="btn {'btn-primary' if currentInput7 == inputIds['in2'] else 'btn-secondary'}">{in2Label}</button>
                        <button type=submit name=outG value=in4 class="btn {'btn-primary' if currentInput7 == inputIds['in4'] else 'btn-secondary'}">{in4Label}</button>
                        <button type=submit name=outG value=in8 class="btn {'btn-primary' if currentInput7 == inputIds['in8'] else 'btn-secondary'}">{in8Label}</button>
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
            switchInput(inputIds[input], outputIds[output])
            print(f"{input} -> {output}")

    return redirect("/")
