from flask import Flask, render_template
from flaskwebgui import FlaskUI

import os, json, pickle, socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyrobogui import robo


def write_pickle(data, filepath):
    """Save python dict to a pickle"""
    pickle_out = open(filepath,"wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()
    
def read_pickle(filepath):
    """Read pickle file"""
    infile = open(filepath,'rb')
    data = pickle.load(infile)
    infile.close()
    return data


def read_json(filepath):
    """Return a dict form a json file"""
    with open(filepath) as j:
        adict = json.load(j)
    return adict

def write_json(data, filepath):
    """Write dict to Json file"""
    with open(filepath, "w") as f:
        json.dump(data, f)

def update_json(new_data, filepath):
    old_data = read_json(filepath)
    old_data.update(new_data)
    write_json(old_data, filepath)

def cfg():
    return read_json("data.json")

def get_server_ip():
    """Get ip address of current device"""
    ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    return ip

ubuntu_cursor_sizes = {
    "Default":24,
    "Medium":32,
    "Large": 48,  
    "Larger": 64,
    "Largest": 96
    }

def set_ubuntu_cursor_size(size):
    os.system(f"gsettings set org.gnome.desktop.interface cursor-size {size}")

def default_cursor():
    set_ubuntu_cursor_size(size=ubuntu_cursor_sizes["Default"])

def largest_cursor():
    set_ubuntu_cursor_size(size=ubuntu_cursor_sizes["Largest"])


#Reset at start of the server the data saved previously
try:
    os.remove("data.json")
except:
    pass

websites = {
    "youtube": "https://www.youtube.com/",
    "netfilx": "https://www.netflix.com",
    "google" : "https://www.google.com/",
    "protv"  : "https://protvplus.ro/tv-live/1-pro-tv",
    "digitv" : "https://www.digi24.ro/live/digi24"
}




app = Flask(__name__)


@app.route("/")
def home_server():
    ip = get_server_ip()
    if not os.path.isfile("data.json"):
        write_json({"server_started": True, 
                    "server_ip": ip,
                    "browser_opened": False,
                    },  "data.json")
        return render_template("server.html", context={"server_ip": ip})
    else:
        return render_template("client.html", context={"server_ip": ip,
                                                       "links": list(websites.keys())
                                                        })

@app.route("/youtube")
def open_youtube():
    #b = webdriver.Chrome("./chromedriver")
    #b.get(websites["youtube"])
    return render_template("controls.html")




if __name__ == "__main__":
    #app.run(debug=True, threaded=True)
    FlaskUI(app, width=400, height=230).run()
    