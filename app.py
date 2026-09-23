from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Work.com - Find Skilled Workers</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #222;
        }

        header {
            background: #0d47a1;
            color: white;
            padding: 18px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 26px;
            font-weight: bold;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin-left: 18px;
            font-size: 15px;
        }

        .hero {
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            color: white;
            text-align: center;
            padding: 70px 20px;
        }

        .hero h1 {
            font-size: 42px;
            margin-bottom: 15px;
        }

        .hero p {
            font-size: 19px;
            margin-bottom: 30px;
        }

        .buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-block;
            padding: 14px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
        }

        .btn-primary {
            background: white;
            color: #0d47a1;
        }

        .btn-secondary {
            border: 2px solid white;
            color: white;
        }

        .section {
            padding: 45px 20px;
            max-width: 1100px;
            margin: auto;
        }

        .section h2 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 30px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        }

        .card .icon {
            font-size: 42px;
            margin-bottom: 12px;
        }

        .card h3 {
            margin-bottom: 8px;
        }

        .card p {
            color: #666;
            font-size: 14px;
        }

        .how {
            background: white;
        }

        .step {
            text-align: center;
            padding: 20px;
        }

        .number {
            width: 45px;
            height: 45px;
            background: #0d47a1;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px;
            font-weight: bold;
            font-size: 20px;
        }

        footer {
            background: #102a43;
            color: white;
            text-align: center;
            padding: 25px;
            margin-top: 20px;
        }

        @media (max-width: 600px) {
            header {
                flex-direction: column;
                gap: 12px;
            }

            nav a {
                margin: 0 7px;
            }

            .hero h1 {
                font-size: 32px;
            }

            .hero {
                padding: 55px 15px;
            }
        }
    </style>
</head>

<body>

<header>
    <div class="logo">Work.com</div>

    <nav>
        <a href="/">Home</a>
        <a href="#workers">Workers</a>
        <a href="#how">How It Works</a>
    </nav>
</header>

<section class="hero">
    <h1>Find Skilled Workers Near You</h1>

    <p>
        Connect with trusted workers for your everyday needs.
    </p>

    <div class="buttons">
        <a href="#workers" class="btn btn-primary">
            Find a Worker
        </a>

        <a href="#" class="btn btn-secondary">
            Register as a Worker
        </a>
    </div>
</section>

<section class="section" id="workers">
    <h2>Popular Services</h2>

    <div class="cards">

        <div class="card">
            <div class="icon">🔨</div>
            <h3>Carpenter</h3>
            <p>Find skilled carpenters for your work.</p>
        </div>

        <div class="card">
            <div class="icon">🔧</div>
            <h3>Mechanic</h3>
            <p>Find mechanics for vehicle repairs.</p>
        </div>

        <div class="card">
            <div class="icon">⚡</div>
            <h3>Electrician</h3>
            <p>Find electricians for electrical work.</p>
        </div>

        <div class="card">
            <div class="icon">🚰</div>
            <h3>Plumber</h3>
            <p>Find plumbers for plumbing services.</p>
        </div>

        <div class="card">
            <div class="icon">🎨</div>
            <h3>Painter</h3>
            <p>Find painters for homes and businesses.</p>
        </div>

        <div class="card">
            <div class="icon">🧱</div>
            <h3>Mason</h3>
            <p>Find experienced construction workers.</p>
        </div>

    </div>
</section>

<section class="section how" id="how">
    <h2>How Work.com Works</h2>

    <div class="cards">

        <div class="step">
            <div class="number">1</div>
            <h3>Choose a Service</h3>
            <p>Select the type of worker you need.</p>
        </div>

        <div class="step">
            <div class="number">2</div>
            <h3>Find a Worker</h3>
            <p>Browse workers available for your job.</p>
        </div>

        <div class="step">
            <div class="number">3</div>
            <h3>Contact</h3>
            <p>Contact the worker and discuss your work.</p>
        </div>

    </div>
</section>

<footer>
    <p>© 2026 Work.com — Connecting People with Skilled Workers</p>
</footer>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        skill = request.form["skill"]
        phone = request.form["phone"]
        location = request.form["location"]
        experience = request.form["experience"]
        description = request.form["description"]

        conn = sqlite3.connect("workers.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                skill TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                experience TEXT,
                description TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO workers
            (name, skill, phone, location, experience, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, skill, phone, location, experience, description))

        conn.commit()
        conn.close()

        return "Worker registered successfully!"
        
            return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Register - Work.com</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #222;
        }

        header {
            background: #0d47a1;
            color: white;
            padding: 18px 22px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 26px;
            font-weight: bold;
        }

        .home-link {
            color: white;
            text-decoration: none;
            font-size: 15px;
        }

        .container {
            max-width: 650px;
            margin: 40px auto;
            padding: 0 18px;
        }

        .form-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
        }

        h1 {
            text-align: center;
            color: #0d47a1;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 7px;
            margin-top: 18px;
        }

        input,
        select,
        textarea {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            background: white;
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        input:focus,
        select:focus,
        textarea:focus {
            outline: none;
            border-color: #1976d2;
        }

        .register-btn {
            width: 100%;
            margin-top: 28px;
            padding: 15px;
            border: none;
            border-radius: 8px;
            background: #0d47a1;
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
        }

        .register-btn:hover {
            background: #083b88;
        }

        footer {
            text-align: center;
            color: #777;
            padding: 25px;
        }

        @media (max-width: 600px) {
            .form-card {
                padding: 22px;
            }

            header {
                padding: 16px;
            }
        }
    </style>
</head>

<body>

<header>
    <div class="logo">Work.com</div>
    <a href="/" class="home-link">← Home</a>
</header>

<div class="container">

    <div class="form-card">

        <h1>👷 Register as a Worker</h1>

        <p class="subtitle">
            Create your worker profile on Work.com
        </p>

        <form method="POST">

            <label for="name">Full Name</label>
            <input
                type="text"
                id="name"
                name="name"
                placeholder="Enter your full name"
                required
            >

            <label for="skill">Your Skill</label>
            <select id="skill" name="skill" required>
                <option value="">Select your skill</option>
                <option value="Carpenter">Carpenter</option>
                <option value="Mechanic">Mechanic</option>
                <option value="Electrician">Electrician</option>
                <option value="Plumber">Plumber</option>
                <option value="Painter">Painter</option>
                <option value="Mason">Mason</option>
                <option value="Other">Other</option>
            </select>

            <label for="phone">Phone Number</label>
            <input
                type="tel"
                id="phone"
                name="phone"
                placeholder="Enter your phone number"
                required
            >

            <label for="location">Location</label>
            <input
                type="text"
                id="location"
                name="location"
                placeholder="City / Area"
                required
            >

            <label for="experience">Years of Experience</label>
            <input
                type="text"
                id="experience"
                name="experience"
                placeholder="Example: 5 years"
            >

            <label for="description">About Your Work</label>
            <textarea
                id="description"
                name="description"
                placeholder="Tell customers about your skills and experience"
            ></textarea>

            <button type="submit" class="register-btn">
                Register Now
            </button>

        </form>

    </div>

</div>

<footer>
    © 2026 Work.com — Connecting People with Skilled Workers
</footer>

</body>
</html>
    """

    
if __name__ == "__main__":
    app.run()
