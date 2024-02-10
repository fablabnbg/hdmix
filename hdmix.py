import socket

from flask import Flask, redirect, request


matrixIds = {
    "Kabel": 1,
    "Chromecast": 2,
    "Volumio": 3,
    "BeamerSpace": 1,
    "LautsprecherSpace": 6,
    "BeamerChillecke": 5,
}

#HOST = "192.168.1.10"
HOST = "172.22.35.189"
PORT = 5000


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
    matrixState = requestMatrixState()
    inputLautsprecherSpace = int(matrixState.split(f"O{matrixIds['LautsprecherSpace']}I")[1][0])
    inputBeamerSpace = int(matrixState.split(f"O{matrixIds['BeamerSpace']}I")[1][0])
    inputBeamerChillecke = int(matrixState.split(f"O{matrixIds['BeamerChillecke']}I")[1][0])

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
                        <input type=submit name=LautsprecherSpace value=Kabel class="btn {'btn-primary' if inputLautsprecherSpace == 1 else 'btn-secondary'}" />
                        <input type=submit name=LautsprecherSpace value=Chromecast class="btn {'btn-primary' if inputLautsprecherSpace == 2 else 'btn-secondary'}" />
                        <input type=submit name=LautsprecherSpace value=Volumio class="btn {'btn-primary' if inputLautsprecherSpace == 3 else 'btn-secondary'}" />
                    </div>

                    <div style="margin-bottom: 2rem">
                        <h3>Beamer *space</h3>
                        <input type=submit name=BeamerSpace value=Kabel class="btn {'btn-primary' if inputBeamerSpace == 1 else 'btn-secondary'}" />
                        <input type=submit name=BeamerSpace value=Chromecast class="btn {'btn-primary' if inputBeamerSpace == 2 else 'btn-secondary'}" />
                        <input type=submit name=BeamerSpace value=Volumio class="btn {'btn-primary' if inputBeamerSpace == 3 else 'btn-secondary'}" />
                    </div>

                    <div>
                        <h3>Beamer Chillecke</h3>
                        <input type=submit name=BeamerChillecke value=Kabel class="btn {'btn-primary' if inputBeamerChillecke == 1 else 'btn-secondary'}" />
                        <input type=submit name=BeamerChillecke value=Chromecast class="btn {'btn-primary' if inputBeamerChillecke == 2 else 'btn-secondary'}" />
                        <input type=submit name=BeamerChillecke value=Volumio class="btn {'btn-primary' if inputBeamerChillecke == 3 else 'btn-secondary'}" />
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
            switchInput(matrixIds[input], matrixIds[output])
            print(f"{input} -> {output}")

    return redirect("/")
