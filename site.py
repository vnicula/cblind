@app.route("/Welcome/<name>") # at the endpoint /<name>
def Welcome_name(name): # call method Welcome_name
  return "Welcome" + name + "!" # which returns "Welcome + name + !