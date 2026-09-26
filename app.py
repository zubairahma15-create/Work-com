from flask import Flask, request, redirect, url_for
from supabase import create_client
from html import escape
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        password = request.form.get("password", "")

        if password != os.environ.get("ADMIN_PASSWORD"):
            return """
            <h2 style="font-family:Arial;text-align:center;margin-top:60px;">
                Incorrect password
            </h2>
            <p style="text-align:center;font-family:Arial;">
                <a href="/admin">Try again</a>
            </p>
            """, 401

        try:
            result = (
                supabase
                .table("workers")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )

            workers = result.data or []

            rows = ""

            for worker in workers:
                rows += f"""
                <tr>
                    <td>{worker.get("name", "")}</td>
                    <td>{worker.get("skill", "")}</td>
                    <td>{worker.get("phone", "")}</td>
                    <td>{worker.get("location", "")}</td>
                    <td>{worker.get("experience", "")}</td>
                </tr>
                """

            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Work.com Admin</title>
                <style>
                    body {{
                        font-family: Arial;
                        margin: 20px;
                        background: #f5f7fa;
                    }}

                    h1 {{
                        color: #1565c0;
                    }}

                    .count {{
                        background: white;
                        padding: 15px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}

                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        background: white;
                    }}

                    th, td {{
                        padding: 12px;
                        border-bottom: 1px solid #ddd;
                        text-align: left;
                    }}

                    th {{
                        background: #1565c0;
                        color: white;
                    }}
                </style>
            </head>

            <body>

                <h1>Work.com Admin Dashboard</h1>

                <div class="count">
                    <strong>Total Registered Workers:</strong>
                    {len(workers)}
                </div>

                <table>
                    <tr>
                        <th>Name</th>
                        <th>Skill</th>
                        <th>Phone</th>
                        <th>Location</th>
                        <th>Experience</th>
                    </tr>

                    {rows}

                </table>

            </body>
            </html>
            """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Work.com Admin Login</title>

        <style>
            body {
                font-family: Arial;
                background: #f5f7fa;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }

            h1 {
                color: #1565c0;
                text-align: center;
            }

            input {
                width: 100%;
                padding: 14px;
                margin: 15px 0;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 14px;
                background: #1565c0;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
        </style>
    </head>

    <body>

        <div class="box">

            <h1>Work.com Admin</h1>

            <form method="POST">

                <input
                    type="password"
                    name="password"
                    placeholder="Admin Password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

        </div>

    </body>
    </html>
    """


# =========================================================
# HOME PAGE
# =========================================================

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html lang="en">

<head>
<meta name="google-site-verification" content="U5lX7y6Xwd0Ggm8ZcVTa34J3s-NFNDRAj_jgfTWZTAQ" />
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
}

header {
    background: white;
    padding: 18px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e5e9f0;
}

.logo {
    font-size: 28px;
    font-weight: 800;
    color: #1769e0;
}

nav {
    display: flex;
    gap: 22px;
}

nav a {
    text-decoration: none;
    color: #344054;
    font-weight: 700;
}

nav a:hover {
    color: #1769e0;
}

.hero {
    background: #eef6ff;
    padding: 60px 20px;
}

.hero-content {
    max-width: 1100px;
    margin: auto;
}

.badge {
    display: inline-block;
    background: #dcecff;
    color: #1769e0;
    padding: 9px 15px;
    border-radius: 25px;
    font-weight: 700;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 48px;
    line-height: 1.1;
    max-width: 700px;
    margin-bottom: 18px;
}

.hero h1 span {
    color: #1769e0;
}

.hero p {
    color: #667085;
    font-size: 18px;
    line-height: 1.6;
    max-width: 620px;
    margin-bottom: 28px;
}

.search-box {
    background: white;
    max-width: 800px;
    padding: 10px;
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(16,24,40,.08);
    display: flex;
    gap: 10px;
}

.search-box input {
    flex: 1;
    border: 1px solid #d0d5dd;
    border-radius: 9px;
    padding: 15px;
    font-size: 15px;
    outline: none;
}

.search-box input:focus {
    border-color: #1769e0;
}

.search-btn {
    border: none;
    background: #1769e0;
    color: white;
    padding: 0 24px;
    border-radius: 9px;
    font-weight: 700;
    font-size: 15px;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 55px 20px;
}

.section-label {
    color: #1769e0;
    font-weight: 800;
    margin-bottom: 9px;
}

.section-title {
    font-size: 34px;
    margin-bottom: 10px;
}

.section-text {
    color: #667085;
    margin-bottom: 28px;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.category-card {
    background: white;
    padding: 23px;
    border-radius: 16px;
    border: 1px solid #e5e9f0;
    box-shadow: 0 5px 18px rgba(16,24,40,.05);
    text-decoration: none;
    color: #172033;
    transition: .2s;
}

.category-card:hover {
    transform: translateY(-3px);
}

.category-icon {
    width: 54px;
    height: 54px;
    background: #eaf3ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    margin-bottom: 15px;
}

.category-card h3 {
    margin-bottom: 7px;
}

.category-card p {
    color: #667085;
    font-size: 14px;
}

.how-box {
    background: #eef6ff;
    border-radius: 18px;
    padding: 35px;
}

.steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    margin-top: 25px;
}

.step {
    text-align: center;
}

.step-icon {
    width: 60px;
    height: 60px;
    background: #dcecff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto auto 15px;
    font-size: 27px;
}

.step h3 {
    margin-bottom: 8px;
}

.step p {
    color: #667085;
    font-size: 14px;
    line-height: 1.5;
}

.cta {
    max-width: 1100px;
    margin: 0 auto 55px;
    background: #1769e0;
    color: white;
    padding: 35px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.cta h2 {
    margin-bottom: 7px;
}

.cta p {
    color: #dbeafe;
}

.cta a {
    background: white;
    color: #1769e0;
    padding: 14px 22px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 800;
}

footer {
    background: #101828;
    color: #cbd5e1;
    padding: 30px 7%;
    text-align: center;
}

footer strong {
    display: block;
    color: white;
    font-size: 21px;
    margin-bottom: 8px;
}

@media (max-width: 700px) {

    header {
        padding: 16px 5%;
    }

    nav {
        gap: 10px;
    }

    nav a {
        font-size: 13px;
    }

    .hero {
        padding: 45px 20px;
    }

    .hero h1 {
        font-size: 36px;
    }

    .search-box {
        flex-direction: column;
    }

    .search-btn {
        padding: 14px;
    }

    .category-grid {
        grid-template-columns: 1fr;
    }

    .steps {
        grid-template-columns: 1fr;
    }

    .cta {
        margin: 0 20px 40px;
        flex-direction: column;
        gap: 22px;
        text-align: center;
    }
}

</style>

</head>

<body>

<header>

    <div class="logo">Work.com</div>

    <nav>
        <a href="/">Home</a>
        <a href="/workers">Workers</a>
        <a href="/register">Register</a>
    </nav>

</header>


<section class="hero">

<div class="hero-content">

    <div class="badge">
        🛡️ Trusted · Skilled · Local
    </div>

    <h1>
        Find <span>Skilled Workers</span>
        for Your Work
    </h1>

    <p>
        Connect with local professionals for
        home, business and everyday services.
    </p>

    <form class="search-box"
          method="GET"
          action="/search">

        <input
            type="text"
            name="skill"
            placeholder="Skill e.g. Driver, Carpenter"
        >

        <input
            type="text"
            name="location"
            placeholder="Location"
        >

        <button class="search-btn" type="submit">
            🔍 Search
        </button>

    </form>

</div>

</section>


<section class="container">

    <div class="section-label">
        OUR SERVICES
    </div>

    <h2 class="section-title">
        Popular Categories
    </h2>

    <p class="section-text">
        Find professionals for different types of work.
    </p>


    <div class="category-grid">

        <a class="category-card"
           href="/search?skill=Carpenter">
            <div class="category-icon">🔨</div>
            <h3>Carpenter</h3>
            <p>Furniture and woodwork</p>
        </a>


        <a class="category-card"
           href="/search?skill=Electrician">
            <div class="category-icon">⚡</div>
            <h3>Electrician</h3>
            <p>Electrical repair and installation</p>
        </a>


        <a class="category-card"
           href="/search?skill=Plumber">
            <div class="category-icon">🚰</div>
            <h3>Plumber</h3>
            <p>Water and pipe services</p>
        </a>


        <a class="category-card"
           href="/search?skill=Mechanic">
            <div class="category-icon">🔧</div>
            <h3>Mechanic</h3>
            <p>Vehicle repair and maintenance</p>
        </a>


        <a class="category-card"
           href="/search?skill=Driver">
            <div class="category-icon">🚗</div>
            <h3>Driver</h3>
            <p>Professional driving services</p>
        </a>


        <a class="category-card"
           href="/search?skill=Caterer">
            <div class="category-icon">🍽️</div>
            <h3>Catering</h3>
            <p>Food and event catering services</p>
        </a>


        <a class="category-card"
           href="/search?skill=Painter">
            <div class="category-icon">🎨</div>
            <h3>Painter</h3>
            <p>Interior and exterior painting</p>
        </a>


        <a class="category-card"
           href="/search?skill=Cook">
            <div class="category-icon">👨‍🍳</div>
            <h3>Cook</h3>
            <p>Home and professional cooking</p>
        </a>


        <a class="category-card"
           href="/search?skill=Cleaner">
            <div class="category-icon">🧹</div>
            <h3>Cleaner</h3>
            <p>Home and commercial cleaning</p>
        </a>


        <a class="category-card"
           href="/search?skill=Mason">
            <div class="category-icon">🧱</div>
            <h3>Mason</h3>
            <p>Construction and brickwork</p>
        </a>


        <a class="category-card"
           href="/search?skill=Barber">
            <div class="category-icon">💇</div>
            <h3>Barber</h3>
            <p>Hair cutting and grooming</p>
        </a>


        <a class="category-card"
           href="/search?skill=Handyman">
            <div class="category-icon">🛠️</div>
            <h3>Handyman</h3>
            <p>General repair and maintenance</p>
        </a>

    </div>

</section>


<section class="container">

<div class="how-box">

    <div class="section-label">
        HOW IT WORKS
    </div>

    <h2 class="section-title">
        Get Started in 3 Simple Steps
    </h2>

    <div class="steps">

        <div class="step">
            <div class="step-icon">👤</div>
            <h3>1. Register</h3>
            <p>
                Register your skills and services.
            </p>
        </div>

        <div class="step">
            <div class="step-icon">🔍</div>
            <h3>2. Find Workers</h3>
            <p>
                Search by skill and location.
            </p>
        </div>

        <div class="step">
            <div class="step-icon">📞</div>
            <h3>3. Contact</h3>
            <p>
                Contact the worker directly.
            </p>
        </div>

    </div>

</div>

</section>


<section class="cta">

    <div>
        <h2>Ready to get your work done?</h2>
        <p>Register your skills on Work.com.</p>
    </div>

    <a href="/register">
        Register Now
    </a>

</section>


<footer>

    <strong>Work.com</strong>

    © 2026 Work.com · Connecting customers
    with skilled workers

</footer>

</body>

</html>
"""


# =========================================================
# WORKER REGISTRATION
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    # -------------------------
    # SAVE WORKER
    # -------------------------

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        skill = request.form.get("skill", "").strip()
        phone = request.form.get("phone", "").strip()
        location = request.form.get("location", "").strip()
        experience = request.form.get("experience", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not skill or not phone or not location:
            return """
            <h2 style="font-family:Arial;text-align:center;margin-top:60px;">
                Please fill all required fields.
            </h2>

            <p style="text-align:center;font-family:Arial;">
                <a href="/register">← Back to registration</a>
            </p>
            """, 400

        try:

            supabase.table("workers").insert({
                "name": name,
                "skill": skill,
                "phone": phone,
                "location": location,
                "experience": experience,
                "description": description
            }).execute()

            # Important:
            # Redirect after successful POST.
            # This prevents the form from being submitted again
            # when the page is refreshed.

            return redirect(url_for("registration_success"))

        except Exception as e:

            print("Registration error:", e)

            return """
            <div style="
                font-family:Arial;
                max-width:600px;
                margin:60px auto;
                padding:30px;
                text-align:center;
            ">

                <h2>Registration could not be completed.</h2>

                <p style="color:#667085;">
                    Please try again.
                </p>

                <a href="/register"
                   style="
                   display:inline-block;
                   margin-top:20px;
                   background:#1769e0;
                   color:white;
                   padding:12px 20px;
                   border-radius:8px;
                   text-decoration:none;
                   font-weight:bold;
                   ">
                    ← Back to Registration
                </a>

            </div>
            """, 500


    # -------------------------
    # REGISTRATION FORM
    # -------------------------

    return """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Work.com - Register as a Worker</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #172033;
}

header {
    background: white;
    padding: 18px 7%;
    border-bottom: 1px solid #e5e9f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 27px;
    font-weight: 800;
    color: #1769e0;
}

.home-link {
    color: #1769e0;
    text-decoration: none;
    font-weight: 700;
}

.container {
    max-width: 650px;
    margin: 45px auto;
    padding: 0 20px;
}

.intro {
    text-align: center;
    margin-bottom: 25px;
}

.intro h1 {
    font-size: 34px;
    margin-bottom: 10px;
}

.intro p {
    color: #667085;
    font-size: 16px;
    line-height: 1.5;
}

.form-card {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #e5e9f0;
    box-shadow: 0 8px 25px rgba(16,24,40,.07);
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    font-weight: 700;
    margin-bottom: 8px;
}

input,
textarea,
select {
    width: 100%;
    padding: 14px;
    border: 1px solid #d0d5dd;
    border-radius: 10px;
    font-size: 16px;
    font-family: Arial, sans-serif;
    outline: none;
    background: white;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #1769e0;
    box-shadow: 0 0 0 3px #eaf3ff;
}

textarea {
    min-height: 120px;
    resize: vertical;
}

.hint {
    display: block;
    color: #667085;
    font-size: 12px;
    margin-top: 6px;
}

.register-btn {
    width: 100%;
    border: none;
    background: #1769e0;
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 800;
    cursor: pointer;
}

.register-btn:hover {
    background: #1258bd;
}

@media (max-width: 600px) {

    header {
        padding: 16px 5%;
    }

    .logo {
        font-size: 24px;
    }

    .container {
        margin: 30px auto;
        padding: 0 15px;
    }

    .intro h1 {
        font-size: 29px;
    }

    .form-card {
        padding: 22px;
        border-radius: 15px;
    }

}

</style>

</head>

<body>

<header>

    <div class="logo">
        Work.com
    </div>

    <a class="home-link" href="/">
        ← Home
    </a>

</header>


<div class="container">

    <div class="intro">

        <h1>Register as a Worker</h1>

        <p>
            Create your worker profile and let customers
            find your services on Work.com.
        </p>

    </div>


    <div class="form-card">

        <form method="POST" action="/register">

            <div class="form-group">

                <label for="name">
                    Full Name *
                </label>

                <input
                    id="name"
                    type="text"
                    name="name"
                    placeholder="Enter your full name"
                    required
                >

            </div>


            <div class="form-group">

                <label for="skill">
                    Skill / Profession *
                </label>

                <input
                    id="skill"
                    type="text"
                    name="skill"
                    placeholder="e.g. Driver, Carpenter, Caterer"
                    required
                >

                <span class="hint">
                    You can enter any profession.
                </span>

            </div>


            <div class="form-group">

                <label for="phone">
                    Phone Number *
                </label>

                <input
                    id="phone"
                    type="tel"
                    name="phone"
                    placeholder="Enter your phone number"
                    required
                >

            </div>


            <div class="form-group">

                <label for="location">
                    Location *
                </label>

                <input
                    id="location"
                    type="text"
                    name="location"
                    placeholder="e.g. Srinagar"
                    required
                >

            </div>


            <div class="form-group">

                <label for="experience">
                    Experience
                </label>

                <input
                    id="experience"
                    type="text"
                    name="experience"
                    placeholder="e.g. 5 years"
                >

            </div>


            <div class="form-group">

                <label for="description">
                    About Your Work
                </label>

                <textarea
                    id="description"
                    name="description"
                    placeholder="Describe your services and the work you provide..."
                ></textarea>

            </div>


            <button
                class="register-btn"
                type="submit">

                ✓ Register as Worker

            </button>

        </form>

    </div>

</div>

</body>

</html>
"""


# =========================================================
# REGISTRATION SUCCESS
# =========================================================

@app.route("/registration-success")
def registration_success():

    return """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Work.com - Registration Successful</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    margin: 0;
}

.success-box {
    background: white;
    max-width: 550px;
    margin: 80px auto;
    padding: 40px 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(16,24,40,.08);
}

.icon {
    font-size: 55px;
    margin-bottom: 15px;
}

h1 {
    color: #172033;
}

p {
    color: #667085;
    line-height: 1.6;
}

.buttons {
    margin-top: 25px;
}

a {
    display: inline-block;
    margin: 6px;
    padding: 12px 20px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: 700;
}

.home {
    background: #1769e0;
    color: white;
}

.workers {
    background: #eaf3ff;
    color: #1769e0;
}

</style>

</head>

<body>

<div class="success-box">

    <div class="icon">🎉</div>

    <h1>Registration Successful!</h1>

    <p>
        Your worker profile has been successfully
        added to Work.com.
    </p>

    <div class="buttons">

        <a class="home" href="/">
            Go to Home
        </a>

        <a class="workers" href="/workers">
            View Workers
        </a>

    </div>

</div>

</body>

</html>
"""


# =========================================================
# SEARCH WORKERS
# =========================================================

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

        result = (
            query
            .order("created_at", desc=True)
            .execute()
        )

        worker_list = result.data

    except Exception as e:

        print("Search error:", e)

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Unable to search workers. Please try again.
        </h2>
        """


    cards = ""

    for worker in worker_list:

        name = escape(worker.get("name") or "")
        skill_value = escape(worker.get("skill") or "")
        location_value = escape(worker.get("location") or "")
        experience = escape(worker.get("experience") or "")
        description = escape(worker.get("description") or "")
        phone = escape(worker.get("phone") or "")

        initial = escape(
            (worker.get("name") or "?")[:1].upper()
        )

        cards += f"""
        <div class="worker-card">

            <div class="worker-top">

                <div class="worker-avatar">
                    {initial}
                </div>

                <div>

                    <h2>{name}</h2>

                    <span class="skill-badge">
                        🔧 {skill_value}
                    </span>

                </div>

            </div>


            <div class="worker-info">

                <div class="info-item">

                    <span>📍</span>

                    <div>
                        <small>Location</small>
                        <strong>{location_value}</strong>
                    </div>

                </div>


                <div class="info-item">

                    <span>🕒</span>

                    <div>
                        <small>Experience</small>
                        <strong>
                            {experience or "Not specified"}
                        </strong>
                    </div>

                </div>

            </div>


            <div class="description">
                {description or "Skilled professional available for work."}
            </div>


            <a class="contact-btn"
               href="tel:{phone}">

                📞 Contact Worker

            </a>

        </div>
        """


    if not cards:

        cards = """
        <div class="empty-box">

            <div style="font-size:45px;">
                🔍
            </div>

            <h2>No workers found</h2>

            <p>
                Try another skill or location.
            </p>

        </div>
        """


    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Work.com - Search Results</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #172033;
}}

header {{
    background: white;
    padding: 18px 7%;
    border-bottom: 1px solid #e5e9f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    color: #1769e0;
    font-size: 26px;
    font-weight: 800;
}}

.home-btn {{
    color: #1769e0;
    text-decoration: none;
    font-weight: 700;
}}

.hero {{
    text-align: center;
    padding: 40px 20px 20px;
}}

.hero h1 {{
    margin-bottom: 8px;
}}

.hero p {{
    color: #667085;
}}

.container {{
    max-width: 1100px;
    margin: auto;
    padding: 20px;
}}

.worker-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 22px;
}}

.worker-card {{
    background: white;
    border: 1px solid #e5e9f0;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(16,24,40,.06);
}}

.worker-top {{
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 22px;
}}

.worker-avatar {{
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: #eaf3ff;
    color: #1769e0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    font-weight: 800;
}}

.worker-top h2 {{
    margin: 0 0 7px;
    font-size: 21px;
}}

.skill-badge {{
    display: inline-block;
    background: #eef6ff;
    color: #1769e0;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}}

.worker-info {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 18px;
}}

.info-item {{
    display: flex;
    gap: 9px;
    align-items: center;
    background: #f8fafc;
    padding: 11px;
    border-radius: 10px;
}}

.info-item span {{
    font-size: 20px;
}}

.info-item small {{
    display: block;
    color: #667085;
    font-size: 11px;
    margin-bottom: 3px;
}}

.info-item strong {{
    font-size: 14px;
}}

.description {{
    color: #667085;
    font-size: 14px;
    line-height: 1.6;
    padding: 12px 0 18px;
}}

.contact-btn {{
    display: block;
    text-align: center;
    background: #1769e0;
    color: white;
    padding: 13px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: 700;
}}

.empty-box {{
    background: white;
    max-width: 600px;
    margin: 30px auto;
    padding: 45px 25px;
    text-align: center;
    border-radius: 18px;
}}

.empty-box p {{
    color: #667085;
}}

@media (max-width: 700px) {{

    .worker-grid {{
        grid-template-columns: 1fr;
    }}

    .worker-info {{
        grid-template-columns: 1fr;
    }}

}}

</style>

</head>

<body>

<header>

    <div class="logo">
        Work.com
    </div>

    <a class="home-btn" href="/">
        ← Home
    </a>

</header>


<section class="hero">

    <h1>Search Results</h1>

    <p>
        Find skilled professionals by skill and location.
    </p>

</section>


<div class="container">

    <div class="worker-grid">

        {cards}

    </div>

</div>

</body>

</html>
"""


# =========================================================
# ALL WORKERS
# =========================================================

@app.route("/workers")
def workers():

    try:

        result = (
            supabase
            .table("workers")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        worker_list = result.data

    except Exception as e:

        print("Workers error:", e)

        return """
        <h2 style="
            font-family:Arial;
            text-align:center;
            margin-top:50px;
        ">
            Unable to load workers. Please try again.
        </h2>
        """


    cards = ""

    for worker in worker_list:

        name = escape(worker.get("name") or "")
        skill = escape(worker.get("skill") or "")
        location = escape(worker.get("location") or "")
        experience = escape(worker.get("experience") or "")
        description = escape(worker.get("description") or "")
        phone = escape(worker.get("phone") or "")

        initial = escape(
            (worker.get("name") or "?")[:1].upper()
        )

        cards += f"""
        <div class="worker-card">

            <div class="worker-top">

                <div class="worker-avatar">
                    {initial}
                </div>

                <div>

                    <h2>{name}</h2>

                    <span class="skill-badge">
                        🔧 {skill}
                    </span>

                </div>

            </div>


            <div class="worker-info">

                <div class="info-item">

                    <span>📍</span>

                    <div>
                        <small>Location</small>
                        <strong>{location}</strong>
                    </div>

                </div>


                <div class="info-item">

                    <span>🕒</span>

                    <div>
                        <small>Experience</small>
                        <strong>
                            {experience or "Not specified"}
                        </strong>
                    </div>

                </div>

            </div>


            <div class="description">
                {description or "Skilled professional available for work."}
            </div>


            <a class="contact-btn"
               href="tel:{phone}">

                📞 Contact Worker

            </a>

        </div>
        """


    if not cards:

        cards = """
        <div class="empty-box">

            <div style="font-size:45px;">
                👷
            </div>

            <h2>No workers registered yet</h2>

            <p>
                Worker profiles will appear here after registration.
            </p>

        </div>
        """


    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Work.com - Skilled Workers</title>

<style>

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #172033;
}}

header {{
    background: white;
    padding: 18px 7%;
    border-bottom: 1px solid #e6eaf0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 25px;
    font-weight: 800;
    color: #1769e0;
}}

.home-btn {{
    text-decoration: none;
    color: #1769e0;
    font-weight: 700;
}}

.hero {{
    text-align: center;
    padding: 45px 20px 30px;
}}

.hero h1 {{
    font-size: 38px;
    margin-bottom: 10px;
}}

.hero p {{
    color: #667085;
    font-size: 17px;
}}

.workers-container {{
    max-width: 1100px;
    margin: auto;
    padding: 20px;
}}

.worker-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 22px;
}}

.worker-card {{
    background: white;
    border: 1px solid #e5e9f0;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(16,24,40,.06);
}}

.worker-top {{
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 22px;
}}

.worker-avatar {{
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: #eaf3ff;
    color: #1769e0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    font-weight: 800;
}}

.worker-top h2 {{
    font-size: 21px;
    margin-bottom: 7px;
}}

.skill-badge {{
    display: inline-block;
    background: #eef6ff;
    color: #1769e0;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}}

.worker-info {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 18px;
}}

.info-item {{
    display: flex;
    gap: 9px;
    align-items: center;
    background: #f8fafc;
    padding: 11px;
    border-radius: 10px;
}}

.info-item span {{
    font-size: 20px;
}}

.info-item small {{
    display: block;
    color: #667085;
    font-size: 11px;
    margin-bottom: 3px;
}}

.info-item strong {{
    font-size: 14px;
}}

.description {{
    color: #667085;
    font-size: 14px;
    line-height: 1.6;
    padding: 12px 0 18px;
}}

.contact-btn {{
    display: block;
    text-align: center;
    background: #1769e0;
    color: white;
    padding: 13px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: 700;
}}

.empty-box {{
    background: white;
    max-width: 600px;
    margin: 30px auto;
    padding: 45px 25px;
    text-align: center;
    border-radius: 18px;
}}

.empty-box p {{
    color: #667085;
    margin-top: 8px;
}}

footer {{
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    background: #101828;
    color: #cbd5e1;
}}

@media (max-width: 700px) {{

    .worker-grid {{
        grid-template-columns: 1fr;
    }}

    .hero h1 {{
        font-size: 30px;
    }}

    .worker-info {{
        grid-template-columns: 1fr;
    }}

    header {{
        padding: 16px 5%;
    }}

}}

</style>

</head>

<body>

<header>

    <div class="logo">
        Work.com
    </div>

    <a class="home-btn" href="/">
        ← Home
    </a>

</header>


<section class="hero">

    <h1>Skilled Workers</h1>

    <p>
        Find trusted local professionals for your work.
    </p>

</section>


<div class="workers-container">

    <div class="worker-grid">

        {cards}

    </div>

</div>


<footer>

    © 2026 Work.com · Connecting customers with skilled workers

</footer>

</body>

</html>
"""


# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":
    app.run()
