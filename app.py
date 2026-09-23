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


if __name__ == "__main__":
    app.run()
