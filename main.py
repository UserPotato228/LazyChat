from flask import *
import json

app = Flask(__name__)
app.secret_key="1234544"

messages = []

@app.route("/")
def index():
    if "name" not in session:
        return redirect("/auth")
    return render_template("index.html")
    

@app.route("/auth", methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        if "name" in session:
            return redirect("/")
        return render_template("auth.html")
    else:
        if request.form.get("name") == "" or request.form.get("name") == None:
            return("<script>alert('ВВЕДИТЕ НИК');document.location='/auth';</script>")
        else:
            session["name"] = request.form.get("name")
            flash("Вы вошли как %s"%session["name"])
            return redirect("/")
    
@app.route("/send", methods=["GET","POST"])
def send():
    if request.method == "POST":
        content = request.json
        print(content)
        if content['message'] == '':
            return(500, "internal error");
        messages.append({"id": len(messages), "name":session['name'], "message":content['message']})
        print(messages)
        
        return ("200", "OK")
    else:
        json_data = json.dumps(messages)
        print(json_data)
        return(json_data)
    
app.run(debug=1, host="0.0.0.0")