import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.recommendation import recommendation_bp
from routes.auth import auth_bp

# Set up static file folder (pointing to client/dist)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
static_folder_path = os.path.join(PROJECT_ROOT, "client", "dist")

app = Flask(__name__, static_folder=static_folder_path, static_url_path="")

CORS(app)

# Register blueprints
app.register_blueprint(recommendation_bp)
app.register_blueprint(auth_bp)

# Catch-all route to serve React SPA (index.html)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Fallback to index.html for React Router to handle client-side routing
        if os.path.exists(os.path.join(app.static_folder, "index.html")):
            return send_from_directory(app.static_folder, "index.html")
        return {"message": "Crop Recommendation API Running (Client not compiled yet)"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host="0.0.0.0", port=port)