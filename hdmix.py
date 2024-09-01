import socket

from flask import Flask, redirect, request


HOST = "172.22.35.189"
PORT = 5000


# array order like on device
inputs = [
    "Kabel *space", 
    "Chromecast Main",
    "Volumio",
    "Chromecast Chillout",
    "",
    "",
    "",
    "Xbox Main",
]

# array order like on device
# (output name, display position)
outputs = [
    ("Beamer *space",           2),
    ("",                        0),
    ("Lautsprecher Chillout",   4), 
    ("",                        0),
    ("Beamer Chillout",         5),
    ("Lautsprecher *space",     1),
    ("Werkstatt",               3),
    ("",                        0),
]


app = Flask(__name__)


def switchInput(input, output):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(f"MT00SW0{input}0{output}NT"))


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
    matrixState = requestMatrixState()

    response = f"""
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
                <form action=/switch>"""
    # sort outputs on display by given order and filter out the unused outputs, but don't skip any indices
    for outputIndex, output in sorted(filter(lambda o: o[1][0] != "", enumerate(outputs)), key=lambda o: o[1][1]):
        response += f"""
                    <div style="margin-top: 1rem; margin-bottom: 2rem">
                        <h3>{output[0]}</h3>"""

        # enumerate the inputs before filtering to not skip any indices
        for inputIndex, input in filter(lambda i: i[1] != "", enumerate(inputs)):
            inputActive = int(matrixState.split(f"O{outputIndex + 1}I")[1][0]) == inputIndex + 1
            response += f"""<button type=submit name={outputIndex + 1} value={inputIndex + 1} class="btn {'btn-primary' if inputActive else 'btn-secondary'}" style="margin: 0.2rem">{input}</button>"""
        response += "</div>"

    response += """
                </form>
            </section>
        </div>
    </body>
</html>"""
    return response


@app.route("/switch")
def switch():
    if len(request.args) != 0:
        for output in request.args:
            input = request.args.get(output)
            switchInput(input, output)
            print(f"{input}({inputs[int(input) - 1]}) -> {output}({outputs[int(output) - 1][0]})")

    return redirect("/")

