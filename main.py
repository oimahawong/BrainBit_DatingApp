from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello_world():
    code_html = '''
    <h1>Welcome to </h1>
    
    <form action= "/aboutus" method= "POST"> 
      <label for="uname"><b>Username</b></label>
      <input type="text" placeholder="Enter Username" name="uname" required>
      <br>  
      <label for="email"><b>Email</b></label>
      <input type="text" placeholder="Enter Email" name="email" id="email" required>
      <br>
      <button type="submit" class="signupbtn">Submit</button>
   
    </form>
    '''
    return code_html

@app.route("/aboutus", methods=['POST', 'GET'])
def aboutus():
    if request.method == 'POST':
        userName = request.form['uname']
        userName = userName[:1].upper() + userName[1:]
        return "<p>Hello {}</p>".format(userName)


    return "<p> About us </p>"

