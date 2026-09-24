from flask import Flask, request
from supabase import create_client
import os
from html import escape

app = Flask(__name__)

# Supabase connection
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


@app.route("/")
def home():
    return """
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
      background: #f7f9fc;
      color: #172033;
      line-height: 1.6;
    }

    header {
      background: #ffffff;
      border-bottom: 1px solid #e8ecf2;
      padding: 18px 7%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
    }

    .logo {
      font-size: 25px;
      font-weight: 800;
      color: #1769e0;
    }

    nav {
      display: flex;
      gap: 24px;
      align-items: center;
    }

    nav a {
      text-decoration: none;
      color: #344054;
      font-weight: 600;
    }

    .nav-btn {
      background: #1769e0;
      color: white;
      padding: 10px 17px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 700;
    }

    .hero {
      padding: 75px 7% 65px;
      text-align: center;
      background: linear-gradient(135deg, #eaf3ff, #ffffff);
    }

    .hero h1 {
      font-size: clamp(35px, 6vw, 58px);
      margin-bottom: 16px;
    }

    .hero h1 span {
      color: #1769e0;
    }

    .hero p {
      max-width: 680px;
      margin: 0 auto 30px;
      color: #5b667a;
      font-size: 18px;
    }

    .search-box {
      max-width: 850px;
      margin: auto;
      background: white;
      padding: 12px;
      border-radius: 14px;
      box-shadow: 0 10px 35px rgba(23, 44, 78, .12);
      display: grid;
      grid-template-columns: 1fr 1fr auto;
      gap: 10px;
    }

    .search-box input {
      border: 1px solid #d9e0ea;
      border-radius: 9px;
      padding: 14px;
      font-size: 15px;
      width: 100%;
    }

    .search-btn {
      border: 0;
      background: #1769e0;
      color: white;
      padding: 0 24px;
      border-radius: 9px;
      font-weight: 700;
      cursor: pointer;
    }

    section {
      padding: 60px 7%;
    }

    .section-title {
      text-align: center;
      margin-bottom: 35px;
    }

    .section-title h2 {
      font-size: 32px;
      margin-bottom: 8px;
    }

    .section-title p {
      color: #667085;
    }

    .services {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      max-width: 1100px;
      margin: auto;
    }

    .card {
      background: white;
      padding: 28px 18px;
      border-radius: 14px;
      text-align: center;
      border: 1px solid #e8ecf2;
    }

    .icon {
      font-size: 38px;
      margin-bottom: 10px;
    }

    .card h3 {
      margin-bottom: 5px;
    }

    .card p {
      color: #667085;
      font-size: 14px;
    }

    .worker-cta {
      max-width: 1100px;
      margin: auto;
      background: #1769e0;
      color: white;
      padding: 45px;
      border-radius: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 25px;
    }

    .worker-cta p {
      color: #dceaff;
      margin-top: 6px;
    }

    .register-btn {
      background: white;
      color: #1769e0;
      text-decoration: none;
      padding: 13px 22px;
      border-radius: 9px;
      font-weight: 800;
      white-space: nowrap;
    }

    footer {
      text-align: center;
      padding: 25px;
      background: #101828;
      color: #cbd5e1;
      font-size: 14px;
    }

    @media (max-width: 800px) {
      nav a:not(.nav-btn) {
        display: none;
      }

      .search-box {
        grid-template-columns: 1fr;
      }

      .search-btn {
        padding: 14px;
      }

      .services {
        grid-template-columns: repeat(2, 1fr);
      }

      .worker-cta {
        flex-direction: column;
        text-align: center;
      }
    }

    @media (max-width: 480px) {
      .services {
        grid-template-columns: 1fr;
      }

      header {
        padding: 16px 5%;
      }

      section {
        padding: 45px 5%;
      }

      .hero {
        padding: 55px 5%;
      }
    }
  </style>
</head>

<body>

<header>
  <div class="logo">Work.com</div>

  <nav>
    <a href="/">Home</a>
    <a href="#services">Services</a>
    <a href="/register" class="nav-btn">Register as Worker</a>
  </nav>
</header>

<main>

  <section class="hero">
    <h1>Find Skilled Workers <span>Near You</span></h1>

    <p>
      Connect with local carpenters, electricians, plumbers, mechanics,
      painters and other skilled professionals.
    </p>

    <<form class="search-box" method="GET" action="/search">
  <input type="text" name="skill" placeholder="What service do you need?">
  <input type="text" name="location" placeholder="Enter your location">
  <button class="search-btn" type="submit">Search Workers</button>
</form>
  </section>

  <section id="services">

    <div class="section-title">
      <h2>Popular Services</h2>
      <p>Find the right professional for your work.</p>
    </div>

    <div class="services">

      <div class="card">
        <div class="icon">🔨</div>
        <h3>Carpenter</h3>
        <p>Furniture & woodwork</p>
      </div>

      <div class="card">
        <div class="icon">⚡</div>
        <h3>Electrician</h3>
        <p>Electrical repair & installation</p>
      </div>

      <div class="card">
        <div class="icon">🚰</div>
        <h3>Plumber</h3>
        <p>Water & pipe services</p>
      </div>

      <div class="card">
        <div class="icon">🔧</div>
        <h3>Mechanic</h3>
        <p>Vehicle repair & maintenance</p>
      </div>

      <div class="card">
        <div class="icon">🧱</div>
        <h3>Mason</h3>
        <p>Construction & brickwork</p>
      </div>

      <div class="card">
        <div class="icon">🎨</div>
        <h3>Painter</h3>
        <p>Home & commercial painting</p>
      </div>

      <div class="card">
        <div class="icon">❄️</div>
        <h3>AC Technician</h3>
        <p>AC repair & servicing</p>
      </div>

      <div class="card">
        <div class="icon">🛠️</div>
        <h3>Other Services</h3>
        <p>More skilled professionals</p>
      </div>

    </div>
  </section>

  <section id="register">

    <div class="worker-cta">

      <div>
        <h2>Are you a skilled worker?</h2>

        <p>
          Register your skills and let customers find your services.
        </p>
      </div>

      <a class="register-btn" href="/register">
        Register Now
      </a>

    </div>

  </section>

</main>

<footer>
  © 2026 Work.com · Connecting customers with skilled workers
</footer>

</body>
</html>
"""


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Work.com - Worker Registration</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f7f9fc;
            margin: 0;
            padding: 0;
        }

        header {
            background: white;
            padding: 20px 7%;
            border-bottom: 1px solid #e8ecf2;
        }

        .logo {
            font-size: 25px;
            font-weight: 800;
            color: #1769e0;
        }

        .container {
            max-width: 550px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,.08);
        }

        h1 {
            text-align: center;
            color: #172033;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: 600;
        }

        input,
        textarea {
            width: 100%;
            padding: 13px;
            margin-top: 7px;
            border: 1px solid #d9e0ea;
            border-radius: 8px;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 14px;
            background: #1769e0;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 700;
        }

        .back {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #1769e0;
            text-decoration: none;
        }
    </style>
</head>

<body>

<header>
    <div class="logo">Work.com</div>
</header>

<div class="container">

    <h1>Worker Registration</h1>

    <form method="POST" action="/register">

        <label>Full Name</label>
        <input type="text" name="name" required>

        <label>Skill / Profession</label>
        <input
            type="text"
            name="skill"
            placeholder="Carpenter, Mechanic, Electrician..."
            required
        >

        <label>Phone Number</label>
        <input type="tel" name="phone" required>

        <label>Location</label>
        <input type="text" name="location" required>

        <label>Experience</label>
        <input
            type="text"
            name="experience"
            placeholder="Example: 5 years"
        >

        <label>Description</label>
        <textarea
            name="description"
            rows="4"
            placeholder="Describe your work and services"
        ></textarea>

        <button type="submit">
            Register as Worker
        </button>

    </form>

    <a class="back" href="/">
        ← Back to Work.com
    </a>

</div>

</body>
</html>
"""

    # Get form data
    name = request.form.get("name", "").strip()
    skill = request.form.get("skill", "").strip()
    phone = request.form.get("phone", "").strip()
    location = request.form.get("location", "").strip()
    experience = request.form.get("experience", "").strip()
    description = request.form.get("description", "").strip()

    # Save worker permanently in Supabase
    try:
        supabase.table("workers").insert({
            "name": name,
            "skill": skill,
            "phone": phone,
            "location": location,
            "experience": experience,
            "description": description
        }).execute()

    except Exception as e:
        print("Supabase error:", e)

        return """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work.com - Error</title>
</head>

<body style="
    font-family: Arial;
    background:#f7f9fc;
    text-align:center;
    padding:40px;
">

    <div style="
        background:white;
        max-width:550px;
        margin:auto;
        padding:30px;
        border-radius:15px;
    ">

        <h1 style="color:#1769e0;">Work.com</h1>

        <h2>Registration could not be saved</h2>

        <p>
            Please try again in a moment.
        </p>

        <br>

        <a href="/register" style="
            display:inline-block;
            background:#1769e0;
            color:white;
            padding:12px 22px;
            border-radius:8px;
            text-decoration:none;
            font-weight:bold;
        ">
            Try Again
        </a>

    </div>

</body>
</html>
"""

    # Escape values before displaying them in HTML
    safe_name = escape(name)
    safe_skill = escape(skill)

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work.com - Registration Successful</title>
</head>

<body style="
    font-family: Arial;
    background:#f7f9fc;
    text-align:center;
    padding:40px;
">

    <div style="
        background:white;
        max-width:550px;
        margin:auto;
        padding:30px;
        border-radius:15px;
    ">

        <h1 style="color:#1769e0;">Work.com</h1>

        <h2>Registration Successful! 🎉</h2>

        <p>
            Thank you, <strong>{safe_name}</strong>.
        </p>

        <p>
            Your <strong>{safe_skill}</strong> worker registration
            has been saved successfully.
        </p>

        <br>

        <a href="/" style="
            display:inline-block;
            background:#1769e0;
            color:white;
            padding:12px 22px;
            border-radius:8px;
            text-decoration:none;
            font-weight:bold;
        ">
            Back to Home
        </a>

    </div>

</body>
</html>
"""

@app.route("/search")
def search():

    skill = request.args.get("skill", "").strip()
    location = request.args.get("location", "").strip()

    try:
        query = supabase.table("workers").select("*")

        if skill:
            query = query.ilike("skill", f"%{skill}%")

        if location:
            query = query.ilike("location", f"%{location}%")

        result = query.order("created_at", desc=True).execute()
        workers = result.data

    except Exception as e:
        print("Search error:", e)
        return "<h2>Unable to search workers. Please try again.</h2>"

    cards = ""

    for worker in workers:
        cards += f"""
        <div style="
            background:white;
            padding:20px;
            margin:15px auto;
            max-width:600px;
            border-radius:12px;
            box-shadow:0 3px 15px rgba(0,0,0,.08);
        ">
            <h2>{escape(worker.get("name", ""))}</h2>
            <p><strong>Skill:</strong> {escape(worker.get("skill", ""))}</p>
            <p><strong>Location:</strong> {escape(worker.get("location", ""))}</p>
            <p><strong>Experience:</strong> {escape(worker.get("experience", ""))}</p>
            <p>{escape(worker.get("description", ""))}</p>
            <p><strong>Phone:</strong> {escape(worker.get("phone", ""))}</p>
        </div>
        """

    if not cards:
        cards = """
        <div style="
            background:white;
            padding:30px;
            max-width:600px;
            margin:20px auto;
            border-radius:12px;
            text-align:center;
        ">
            <h2>No workers found</h2>
            <p>Try another skill or location.</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Work.com - Search Workers</title>
    </head>

    <body style="
        font-family:Arial;
        background:#f7f9fc;
        margin:0;
        padding:30px;
    ">

        <h1 style="
            text-align:center;
            color:#1769e0;
        ">Work.com</h1>

        <h2 style="text-align:center;">
            Available Workers
        </h2>

        {cards}

        <div style="text-align:center; margin-top:25px;">
            <a href="/" style="
                display:inline-block;
                background:#1769e0;
                color:white;
                padding:12px 22px;
                border-radius:8px;
                text-decoration:none;
                font-weight:bold;
            ">
                ← Back to Home
            </a>
        </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()
