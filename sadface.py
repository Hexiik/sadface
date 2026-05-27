from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

terminal_log = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>sadface</title>

    <style>
        body {
            background: #111;
            color: #0f0;
            font-family: monospace;
            padding: 20px;
        }

        textarea {
            width: 100%;
            height: 80px;
            background: #000;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 10px;
        }

        button {
            margin-top: 10px;
            padding: 10px 20px;
            background: #000;
            color: #0f0;
            border: 1px solid #0f0;
            cursor: pointer;
        }

        pre {
            margin-top: 20px;
            background: #000;
            padding: 15px;
            border: 1px solid #0f0;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            height: 500px;
            overflow-y: scroll;
        }
    </style>
</head>

<body>

<h1>Phone Terminal</h1>

<form method="POST">
    <textarea name="command" placeholder="Enter command..."></textarea>
    <br>
    <button type="submit">Run</button>
</form>

<pre>{{ output }}</pre>

<script>
    const pre = document.querySelector("pre");
    pre.scrollTop = pre.scrollHeight;
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global terminal_log

    if request.method == "POST":
        command = request.form.get("command")

        terminal_log.append(f"$ {command}")

        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True
            )

            terminal_log.append(result)

        except subprocess.CalledProcessError as e:
            terminal_log.append(e.output)

    full_output = "\n".join(terminal_log)

    return render_template_string(
        HTML,
        output=full_output
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)