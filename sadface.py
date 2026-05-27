from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

terminal_log = []
current_dir = os.path.expanduser("~")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SADFACE</title>

    <style>
        body {
            background: #111;
            color: #fff;
            font-family: monospace;
            padding: 20px;
        }

        h2 {
            color: #fff;
        }

        textarea {
            width: 100%;
            height: 70px;
            background: #000;
            color: #fff;
            border: 1px solid #fff;
            padding: 10px;
            resize: none;
            font-family: monospace;
            font-size: 15px;
        }

        button {
            margin-top: 10px;
            padding: 10px 20px;
            background: #000;
            color: #fff;
            border: 1px solid #fff;
            cursor: pointer;
            font-family: monospace;
        }

        pre {
            margin-top: 20px;
            background: #000;
            padding: 15px;
            border: 1px solid #fff;
            height: 500px;
            overflow-y: scroll;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }
    </style>
</head>

<body>

<h2>Directory: {{ current_dir }}</h2>

<form method="POST" id="terminalForm">

<textarea
    name="command"
    id="commandBox"
    placeholder="Enter command..."
></textarea>

<br>

<button type="submit">Run</button>

</form>

<pre>{{ output }}</pre>

<script>

const pre = document.querySelector("pre");
pre.scrollTop = pre.scrollHeight;

const box = document.getElementById("commandBox");
const form = document.getElementById("terminalForm");

box.addEventListener("keydown", function(e) {

    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.submit();
    }

});

</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    global current_dir

    if request.method == "POST":

        command = request.form.get("command", "").strip()

        if command:

            terminal_log.append(f"{current_dir} $ {command}")

            if command.startswith("cd "):

                new_dir = command[3:].strip()

                if new_dir == "~":
                    new_dir = os.path.expanduser("~")

                if not os.path.isabs(new_dir):
                    new_dir = os.path.join(current_dir, new_dir)

                new_dir = os.path.abspath(new_dir)

                if os.path.isdir(new_dir):
                    current_dir = new_dir
                    terminal_log.append(f"Changed directory to {current_dir}")

                else:
                    terminal_log.append("Directory not found.")

            else:

                try:

                    result = subprocess.check_output(
                        command,
                        shell=True,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=current_dir
                    )

                    terminal_log.append(result)

                except subprocess.CalledProcessError as e:

                    terminal_log.append(e.output)

    return render_template_string(
        HTML,
        output="\\n".join(terminal_log),
        current_dir=current_dir
    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=3000
    )