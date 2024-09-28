from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <html>
        <head>
            <title>Flask AJAX Example</title>
            <script>
                function changeDivContent() {
                    fetch('/update_div')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('myDiv').innerHTML = data.new_content;
                        });
                }
            </script>
        </head>
        <body>
            <div id="myDiv"><p>Hello, World!</p></div>
            <button onclick="changeDivContent()">Change Content</button>
        </body>
    </html>
    """

@app.route("/update_div")
def update_div():
    return jsonify(new_content="<p>New content from Flask!</p>")

if __name__ == '__main__':
    app.run(debug=True)