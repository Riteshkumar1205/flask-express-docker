from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# In-memory student dictionary
students = {}

# ---------------------------
# ROUTES
# ---------------------------

@app.route('/')
def home():
    """Root route for quick check"""
    app.logger.debug("Root route accessed")
    return '✅ Flask Backend Running — visit /health or POST to /submit'

@app.get("/health")
def health():
    """Health check route"""
    app.logger.debug("Health route accessed")
    return jsonify(status="ok", message="Flask backend is healthy")

@app.post("/submit")
def submit():
    """Main route to handle actions from the frontend"""
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    # 1️⃣ Grade Checker
    if action == "grade":
        try:
            score = int(data.get("score", 0))
        except ValueError:
            return jsonify(error="Score must be an integer"), 400

        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        return jsonify(result=f"Grade: {grade}")

    # 2️⃣ Add or Update Student
    elif action == "add_student":
        name = (data.get("name") or "").strip()
        grade = (data.get("grade") or "").strip().upper()

        if not name:
            return jsonify(error="Name is required"), 400
        if grade not in {"A", "B", "C", "D", "F"}:
            return jsonify(error="Grade must be one of A/B/C/D/F"), 400

        students[name] = grade
        return jsonify(result=f"{name} -> {grade} saved successfully.")

    # 3️⃣ Show All Students
    elif action == "show_students":
        return jsonify(students)

    # 4️⃣ Write to File
    elif action == "write_file":
        content = data.get("content")
        if content is None:
            return jsonify(error="Content is required"), 400

        with open("data.txt", "w") as f:
            f.write(content)
        return jsonify(result="File written successfully.")

    # 5️⃣ Read from File
    elif action == "read_file":
        try:
            with open("data.txt", "r") as f:
                content = f.read()
            return jsonify(content=content)
        except FileNotFoundError:
            return jsonify(error="File not found"), 404

    # Invalid Action
    return jsonify(error="Invalid Action. Please provide a valid action."), 400

# ---------------------------
# MAIN ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    print("🚀 Starting Flask backend on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
