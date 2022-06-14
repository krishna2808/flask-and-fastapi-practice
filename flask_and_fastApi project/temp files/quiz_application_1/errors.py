from blog import app 





# create custom error  pages 


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404 


@app.errorhandler(500)
def page_not_found(error):
    return render_template("errors/500.html")


