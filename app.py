from flask import Flask, request, redirect, url_for, session
from supabase import create_client
from html import escape
import razorpay
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
# =========================================================
# RAZORPAY
# =========================================================

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET
    )
)
# =========================================================
# ADMIN SYSTEM
# =========================================================

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == ADMIN_PASSWORD and ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect("/admin")

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Failed - Work.com</title>
        </head>

        <body style="
            font-family:Arial;
            text-align:center;
            padding:50px;
            background:#f5f7fb;
        ">

            <div style="
                max-width:400px;
                margin:auto;
                background:white;
                padding:30px;
                border-radius:15px;
                box-shadow:0 5px 20px rgba(0,0,0,.08);
            ">

                <h2 style="color:#dc2626;">
                    Incorrect Password
                </h2>

                <p>
                    Please enter the correct admin password.
                </p>

                <a href="/admin/login">
                    Try Again
                </a>

            </div>

        </body>
        </html>
        """, 401


    return """
    <!DOCTYPE html>
    <html>

    <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Admin Login - Work.com</title>

        <style>

            body {
                font-family:Arial;
                background:#f5f7fb;
                display:flex;
                justify-content:center;
                align-items:center;
                min-height:100vh;
                margin:0;
            }

            .box {
                background:white;
                padding:30px;
                border-radius:18px;
                width:90%;
                max-width:400px;
                box-shadow:0 5px 20px rgba(16,24,40,.1);
            }

            h1 {
                text-align:center;
                color:#1769e0;
            }

            h2 {
                text-align:center;
            }

            input {
                width:100%;
                padding:14px;
                margin:15px 0;
                box-sizing:border-box;
                border:1px solid #d0d5dd;
                border-radius:8px;
                font-size:16px;
            }

            button {
                width:100%;
                padding:14px;
                background:#1769e0;
                color:white;
                border:none;
                border-radius:8px;
                font-size:16px;
                font-weight:bold;
            }

            .home {
                display:block;
                text-align:center;
                margin-top:20px;
                color:#1769e0;
                text-decoration:none;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>Work.com</h1>

            <h2>Admin Login</h2>

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

            <a class="home" href="/">
                ← Back to Work.com
            </a>

        </div>

    </body>

    </html>
    """


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):

        return redirect("/admin/login")


    try:

        result = (
            supabase
            .table("workers")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        workers = result.data or []

    except Exception as e:

        return f"""
        <h2 style="font-family:Arial;text-align:center;">
            Admin Dashboard Error
        </h2>

        <p style="font-family:Arial;text-align:center;">
            {escape(str(e))}
        </p>

        <p style="text-align:center;">
            <a href="/admin">Try Again</a>
        </p>
        """, 500


    rows = ""

    for worker in workers:

        worker_id = escape(str(worker.get("id") or ""))
        name = escape(str(worker.get("name") or ""))
        skill = escape(str(worker.get("skill") or ""))
        phone = escape(str(worker.get("phone") or ""))
        location = escape(str(worker.get("location") or ""))
        experience = escape(str(worker.get("experience") or ""))

        rows += f"""
        <tr>

            <td>{name}</td>

            <td>{skill}</td>

            <td>{phone}</td>

            <td>{location}</td>

            <td>{experience}</td>

            <td>

                <a href="/admin/edit/{worker_id}"
                   style="
                   display:inline-block;
                   padding:8px 12px;
                   background:#2563eb;
                   color:white;
                   text-decoration:none;
                   border-radius:6px;
                   margin-right:5px;
                   ">
                    Edit
                </a>

                <form method="POST"
                      action="/admin/delete"
                      style="display:inline;">

                    <input
                        type="hidden"
                        name="worker_id"
                        value="{worker_id}"
                    >

                    <button
                        type="submit"
                        style="
                        padding:8px 12px;
                        background:#dc2626;
                        color:white;
                        border:none;
                        border-radius:6px;
                        "
                    >
                        Delete
                    </button>

                </form>

            </td>

        </tr>
        """


    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Work.com Admin</title>

        <style>

            body {{
                font-family:Arial;
                margin:0;
                padding:20px;
                background:#f5f7fb;
            }}

            .header {{
                background:white;
                padding:20px;
                border-radius:15px;
                margin-bottom:20px;
            }}

            h1 {{
                color:#1769e0;
                margin-top:0;
            }}

            .topbar {{
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:10px;
                flex-wrap:wrap;
            }}

            .logout {{
                background:#667085;
                color:white;
                padding:10px 15px;
                border-radius:8px;
                text-decoration:none;
            }}

            .count {{
                background:white;
                padding:18px;
                border-radius:12px;
                margin-bottom:20px;
                font-size:18px;
            }}

            .search {{
                width:100%;
                padding:14px;
                box-sizing:border-box;
                margin-bottom:20px;
                border:1px solid #d0d5dd;
                border-radius:9px;
                font-size:16px;
            }}

            .table-wrap {{
                overflow-x:auto;
                background:white;
                border-radius:12px;
            }}

            table {{
                width:100%;
                min-width:850px;
                border-collapse:collapse;
            }}

            th, td {{
                padding:13px;
                border-bottom:1px solid #e5e7eb;
                text-align:left;
            }}

            th {{
                background:#1769e0;
                color:white;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <div class="topbar">

                <h1>Work.com Admin</h1>

                <a class="logout"
                   href="/admin/logout">
                    Logout
                </a>

            </div>

        </div>


        <input
            class="search"
            id="workerSearch"
            type="text"
            oninput="filterWorkers()"
            placeholder="Search by name, skill or location..."
        >


        <div class="count">

            <strong>Total Registered Workers:</strong>
            {len(workers)}

        </div>


        <div class="table-wrap">

            <table id="workerTable">

                <tr>
                    <th>Name</th>
                    <th>Skill</th>
                    <th>Phone</th>
                    <th>Location</th>
                    <th>Experience</th>
                    <th>Action</th>
                </tr>

                {rows}

            </table>

        </div>


        <script>

        function filterWorkers() {{

            const search =
                document
                .getElementById("workerSearch")
                .value
                .toLowerCase();

            const rows =
                document.querySelectorAll(
                    "#workerTable tr"
                );

            for (let i = 1; i < rows.length; i++) {{

                const text =
                    rows[i].innerText.toLowerCase();

                rows[i].style.display =
                    text.includes(search) ? "" : "none";

            }}

        }}

        </script>

    </body>

    </html>
    """


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin/login")


# =========================================================
# ADMIN DELETE
# =========================================================

@app.route("/admin/delete", methods=["POST"])
def admin_delete():

    if not session.get("admin_logged_in"):

        return redirect("/admin/login")


    worker_id = request.form.get("worker_id", "")

    if not worker_id:

        return "Worker ID missing", 400


    try:

        supabase.table("workers").delete().eq(
            "id",
            worker_id
        ).execute()

        return redirect("/admin")

    except Exception as e:

        return f"""
        <h2>Delete Error</h2>

        <p>{escape(str(e))}</p>

        <p>
            <a href="/admin">
                Back to Admin
            </a>
        </p>
        """, 500


# =========================================================
# ADMIN EDIT
# =========================================================

@app.route("/admin/edit/<worker_id>", methods=["GET", "POST"])
def admin_edit(worker_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin/login")


    try:

        result = (
            supabase
            .table("workers")
            .select("*")
            .eq("id", worker_id)
            .execute()
        )

        workers_found = result.data or []

        if not workers_found:

            return "Worker not found", 404

        worker = workers_found[0]

    except Exception as e:

        return f"""
        <h2>Unable to load worker</h2>

        <p>{escape(str(e))}</p>

        <p>
            <a href="/admin">
                Back to Admin
            </a>
        </p>
        """, 500


    if request.method == "POST":

        name = request.form.get("name", "").strip()
        skill = request.form.get("skill", "").strip()
        phone = request.form.get("phone", "").strip()
        location = request.form.get("location", "").strip()
        experience = request.form.get("experience", "").strip()
        description = request.form.get("description", "").strip()


        if not name or not skill or not phone or not location:

            return """
            <h2 style="font-family:Arial;text-align:center;">
                Please fill all required fields.
            </h2>

            <p style="text-align:center;">
                <a href="/admin">
                    Back to Admin
                </a>
            </p>
            """, 400


        try:

            supabase.table("workers").update({

                "name": name,
                "skill": skill,
                "phone": phone,
                "location": location,
                "experience": experience,
                "description": description

            }).eq(
                "id",
                worker_id
            ).execute()


            return """
            <!DOCTYPE html>
            <html>

            <head>

                <meta name="viewport"
                      content="width=device-width, initial-scale=1.0">

                <title>Updated - Work.com</title>

            </head>

            <body style="
                font-family:Arial;
                text-align:center;
                margin-top:60px;
            ">

                <h2>
                    Worker updated successfully! ✅
                </h2>

                <p>
                    The worker information has been saved.
                </p>

                <a href="/admin">
                    Back to Admin Dashboard
                </a>

            </body>

            </html>
            """

        except Exception as e:

            return f"""
            <h2>Update Error</h2>

            <p>{escape(str(e))}</p>

            <p>
                <a href="/admin">
                    Back to Admin
                </a>
            </p>
            """, 500


    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Edit Worker - Work.com</title>

        <style>

            body {{
                font-family:Arial;
                background:#f5f7fb;
                padding:20px;
                margin:0;
            }}

            .box {{
                max-width:600px;
                margin:30px auto;
                background:white;
                padding:25px;
                border-radius:15px;
                box-shadow:0 5px 20px rgba(16,24,40,.08);
            }}

            h1 {{
                color:#1769e0;
            }}

            label {{
                display:block;
                font-weight:bold;
                margin-top:15px;
                margin-bottom:6px;
            }}

            input,
            textarea {{
                width:100%;
                padding:13px;
                box-sizing:border-box;
                border:1px solid #d0d5dd;
                border-radius:8px;
                font-size:16px;
            }}

            textarea {{
                min-height:120px;
            }}

            button {{
                width:100%;
                padding:14px;
                margin-top:22px;
                background:#1769e0;
                color:white;
                border:none;
                border-radius:8px;
                font-size:16px;
                font-weight:bold;
            }}

            .back {{
                display:block;
                text-align:center;
                margin-top:18px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h1>Edit Worker</h1>

            <form method="POST">

                <label>Name</label>

                <input
                    type="text"
                    name="name"
                    value="{escape(worker.get("name") or "")}"
                    required
                >


                <label>Skill / Profession</label>

                <input
                    type="text"
                    name="skill"
                    value="{escape(worker.get("skill") or "")}"
                    required
                >


                <label>Phone</label>

                <input
                    type="text"
                    name="phone"
                    value="{escape(worker.get("phone") or "")}"
                    required
                >


                <label>Location</label>

                <input
                    type="text"
                    name="location"
                    value="{escape(worker.get("location") or "")}"
                    required
                >


                <label>Experience</label>

                <input
                    type="text"
                    name="experience"
                    value="{escape(worker.get("experience") or "")}"
                >


                <label>About Work</label>

                <textarea
                    name="description"
                >{escape(worker.get("description") or "")}</textarea>


                <button type="submit">
                    Save Changes
                </button>

            </form>


            <a class="back" href="/admin">
                ← Back to Admin
            </a>

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

        # Work photos
        photos = request.files.getlist("photos")

        if not name or not skill or not phone or not location:
            return """
            <h2 style="font-family:Arial;text-align:center;margin-top:60px;">
                Please fill all required fields.
            </h2>

            <p style="text-align:center;font-family:Arial;">
                <a href="/register">← Back to registration</a>
            </p>
            """, 400

        # Allow maximum 5 photos
        photos = [photo for photo in photos if photo and photo.filename]

        if len(photos) > 5:
            return """
            <div style="
                font-family:Arial;
                max-width:600px;
                margin:60px auto;
                padding:30px;
                text-align:center;
            ">
                <h2>Maximum 5 photos allowed.</h2>

                <p style="color:#667085;">
                    Please go back and select up to 5 work photos.
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
            """, 400

        try:

            # -------------------------
            # CREATE WORKER
            # -------------------------

            worker_result = supabase.table("workers").insert({
                "name": name,
                "skill": skill,
                "phone": phone,
                "location": location,
                "experience": experience,
                "description": description
            }).execute()

            if not worker_result.data:
                raise Exception("Worker was not created.")

            worker_id = str(worker_result.data[0]["id"])

            # -------------------------
            # UPLOAD WORK PHOTOS
            # -------------------------

            import uuid

            allowed_types = {
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "image/webp": ".webp"
            }

            for photo in photos:

                content_type = photo.content_type or ""

                if content_type not in allowed_types:
                    continue

                extension = allowed_types[content_type]

                filename = (
                    str(worker_id)
                    + "/"
                    + str(uuid.uuid4())
                    + extension
                )

                photo_data = photo.read()

                # Maximum 5 MB per photo
                if len(photo_data) > 5 * 1024 * 1024:
                    continue

                supabase.storage.from_("worker-photos").upload(
                    filename,
                    photo_data,
                    file_options={
                        "content-type": content_type,
                        "upsert": "false"
                    }
                )

                public_url = supabase.storage.from_(
                    "worker-photos"
                ).get_public_url(filename)

                # Save photo information
                supabase.table("worker_photos").insert({
                    "worker_id": worker_id,
                    "photo_url": public_url
                }).execute()

            # Important:
            # Redirect after successful POST.
            # This prevents the form from being submitted again
            # when the page is refreshed.

       session["pending_worker_id"] = worker_id

return redirect(url_for("registration_payment"))

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

.photo-box {
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    padding: 18px;
}

.photo-box input {
    background: white;
}

.photo-title {
    font-weight: 700;
    margin-bottom: 6px;
}

.photo-info {
    color: #667085;
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 12px;
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

        <form
            method="POST"
            action="/register"
            enctype="multipart/form-data">

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


            <div class="form-group">

                <label>
                    📷 Photos of Your Work
                </label>

                <div class="photo-box">

                    <div class="photo-title">
                        Show customers your previous work
                    </div>

                    <div class="photo-info">
                        Upload up to 5 photos. JPG, PNG or WebP.
                        Maximum 5 MB per photo.
                    </div>

                    <input
                        type="file"
                        name="photos"
                        accept="image/*"
                        multiple
                    >

                </div>

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
        phone = escape(worker.get("phone") or 
        "")

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

    📞 Call Worker

</a>

<a class="contact-btn"
   href="https://wa.me/{phone}"
   target="_blank">

    💬 WhatsApp

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

        worker_list = result.data or []

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


    # Load worker photos
    photo_map = {}

    try:

        photo_result = (
            supabase
            .table("worker_photos")
            .select("worker_id, photo_url")
            .order("created_at", desc=False)
            .execute()
        )

        for photo in (photo_result.data or []):

            worker_id = str(photo.get("worker_id") or "")
            photo_url = photo.get("photo_url")

            if worker_id and photo_url:

                photo_map.setdefault(
                    worker_id,
                    []
                ).append(photo_url)

    except Exception as e:

        print("Worker photos error:", e)


    cards = ""


    for worker in worker_list:

        worker_id = str(worker.get("id") or "")

        name = escape(worker.get("name") or "")
        skill = escape(worker.get("skill") or "")
        location = escape(worker.get("location") or "")
        experience = escape(worker.get("experience") or "")
        description = escape(worker.get("description") or "")
        phone = escape(worker.get("phone") or "")

        initial = escape(
            (worker.get("name") or "?")[:1].upper()
        )


        # Get photos for this worker
        worker_photo_list = photo_map.get(
            worker_id,
            []
        )


        photos_html = ""

        if worker_photo_list:

            photos_html = """
            <div class="worker-photos">
            """

            for photo_url in worker_photo_list[:5]:

                safe_photo_url = escape(
                    str(photo_url),
                    quote=True
                )

                photos_html += f"""
                <img
                    class="worker-photo"
                    src="{safe_photo_url}"
                    alt="Work photo of {name}"
                    loading="lazy"
                >
                """

            photos_html += """
            </div>
            """


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


            {photos_html}


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


            <a
                class="contact-btn"
                href="tel:{phone}"
            >
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

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

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

    box-shadow:
        0 5px 20px rgba(16,24,40,.06);
}}


.worker-top {{
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 18px;
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

    flex-shrink: 0;
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


/* Worker photos */

.worker-photos {{
    display: flex;
    gap: 10px;

    overflow-x: auto;

    margin-bottom: 18px;
    padding-bottom: 5px;
}}


.worker-photo {{
    width: 135px;
    height: 135px;

    object-fit: cover;

    border-radius: 12px;

    border: 1px solid #e5e9f0;

    flex: 0 0 auto;

    background: #f1f5f9;
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

    .worker-photo {{
        width: 115px;
        height: 115px;
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

    <a
        class="home-btn"
        href="/"
    >
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
# RAZORPAY TEST PAYMENT
# =========================================================

@app.route("/payment-test")
def payment_test():

    try:

        amount = 9900  # ₹99 in paise

        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": "workcom_test_99",
            "payment_capture": 1
        })

        return f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Work.com - Test Payment</title>

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    text-align: center;
    padding: 40px 20px;
}}

.payment-box {{
    background: white;
    max-width: 450px;
    margin: 40px auto;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 5px 25px rgba(0,0,0,.08);
}}

h1 {{
    color: #1769e0;
}}

.amount {{
    font-size: 32px;
    font-weight: 800;
    margin: 20px;
}}

button {{
    width: 100%;
    border: none;
    background: #1769e0;
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 700;
}}

</style>

</head>

<body>

<div class="payment-box">

    <h1>Work.com</h1>

    <h2>Registration Fee</h2>

    <div class="amount">₹99</div>

    <p>
        This is a TEST payment.
    </p>

    <br>

    <button onclick="startPayment()">
        Pay ₹99
    </button>

</div>


<script>

function startPayment() {{

    var options = {{

        "key": "{RAZORPAY_KEY_ID}",

        "amount": "9900",

        "currency": "INR",

        "name": "Work.com",

        "description": "Worker Registration Fee",

        "order_id": "{order['id']}",

        "handler": function (response) {{

            window.location.href =
                "/payment-success"
                + "?payment_id="
                + encodeURIComponent(response.razorpay_payment_id)
                + "&order_id="
                + encodeURIComponent(response.razorpay_order_id)
                + "&signature="
                + encodeURIComponent(response.razorpay_signature);

        }},

        "theme": {{

            "color": "#1769e0"

        }}

    }};


    var rzp = new Razorpay(options);

    rzp.open();

}}

</script>

</body>

</html>
"""

    except Exception as e:

        print("Payment order error:", e)

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Unable to create payment order.
        </h2>
        """, 500


@app.route("/payment-success")
def payment_success():

    payment_id = request.args.get("payment_id")
    order_id = request.args.get("order_id")
    signature = request.args.get("signature")

    if not payment_id or not order_id or not signature:

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Payment information is incomplete.
        </h2>
        """, 400


    try:

        razorpay_client.utility.verify_payment_signature({

            "razorpay_order_id": order_id,

            "razorpay_payment_id": payment_id,

            "razorpay_signature": signature

        })

        return """
        <!DOCTYPE html>

        <html>

        <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Payment Successful</title>

        </head>

        <body style="
            font-family:Arial;
            text-align:center;
            padding:50px 20px;
            background:#f5f7fb;
        ">

        <div style="
            background:white;
            max-width:500px;
            margin:auto;
            padding:35px;
            border-radius:18px;
        ">

            <div style="font-size:55px;">
                ✅
            </div>

            <h1>Payment Successful</h1>

            <p>
                Your ₹99 Work.com test payment was verified successfully.
            </p>

            <br>

            <a href="/" style="
                display:inline-block;
                background:#1769e0;
                color:white;
                padding:13px 22px;
                border-radius:9px;
                text-decoration:none;
                font-weight:700;
            ">
                Back to Work.com
            </a>

        </div>

        </body>

        </html>
        """

    except Exception as e:

        print("Payment verification error:", e)

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Payment verification failed.
        </h2>
        """, 400
        # =========================================================
# WORKER REGISTRATION PAYMENT
# =========================================================

@app.route("/registration-payment")
def registration_payment():

    worker_id = session.get("pending_worker_id")

    if not worker_id:

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            No pending worker registration found.
        </h2>
        """, 400


    try:

        amount = 9900  # ₹99

        order = razorpay_client.order.create({

            "amount": amount,

            "currency": "INR",

            "receipt": "workcom_" + str(worker_id),

            "payment_capture": 1

        })


        return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Work.com - Registration Payment</title>

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    text-align: center;
    padding: 40px 20px;
}}

.payment-box {{
    background: white;
    max-width: 450px;
    margin: 40px auto;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 5px 25px rgba(0,0,0,.08);
}}

h1 {{
    color: #1769e0;
}}

.amount {{
    font-size: 32px;
    font-weight: 800;
    margin: 20px;
}}

button {{
    width: 100%;
    border: none;
    background: #1769e0;
    color: white;
    padding: 15px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 700;
}}

</style>

</head>

<body>

<div class="payment-box">

    <h1>Work.com</h1>

    <h2>Worker Registration</h2>

    <div class="amount">₹99</div>

    <p>
        Registration fee
    </p>

    <br>

    <button onclick="startPayment()">
        Pay ₹99
    </button>

</div>


<script>

function startPayment() {{

    var options = {{

        "key": "{RAZORPAY_KEY_ID}",

        "amount": "9900",

        "currency": "INR",

        "name": "Work.com",

        "description": "Worker Registration Fee",

        "order_id": "{order['id']}",

        "handler": function(response) {{

            window.location.href =
                "/registration-payment-success"
                + "?payment_id="
                + encodeURIComponent(
                    response.razorpay_payment_id
                )
                + "&order_id="
                + encodeURIComponent(
                    response.razorpay_order_id
                )
                + "&signature="
                + encodeURIComponent(
                    response.razorpay_signature
                );

        }},

        "theme": {{

            "color": "#1769e0"

        }}

    }};


    var rzp = new Razorpay(options);

    rzp.open();

}}

</script>

</body>

</html>
"""


    except Exception as e:

        print("Registration payment error:", e)

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Unable to create payment order.
        </h2>
        """, 500



@app.route("/registration-payment-success")
def registration_payment_success():

    worker_id = session.get("pending_worker_id")

    payment_id = request.args.get("payment_id")

    order_id = request.args.get("order_id")

    signature = request.args.get("signature")


    if not worker_id:

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Worker registration session not found.
        </h2>
        """, 400


    if not payment_id or not order_id or not signature:

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Payment information is incomplete.
        </h2>
        """, 400


    try:

        razorpay_client.utility.verify_payment_signature({

            "razorpay_order_id": order_id,

            "razorpay_payment_id": payment_id,

            "razorpay_signature": signature

        })


        # Mark worker as paid
        supabase.table("workers").update({

            "payment_status": "paid"

        }).eq(
            "id",
            worker_id
        ).execute()


        # Clear pending worker
        session.pop("pending_worker_id", None)


        return """
<!DOCTYPE html>

<html>

<head>

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Work.com - Registration Complete</title>

</head>

<body style="
    font-family:Arial;
    text-align:center;
    padding:50px 20px;
    background:#f5f7fb;
">

<div style="
    background:white;
    max-width:500px;
    margin:auto;
    padding:35px;
    border-radius:18px;
">

    <div style="font-size:55px;">
        ✅
    </div>

    <h1>Registration Complete!</h1>

    <p>
        Your ₹99 payment was verified successfully.
    </p>

    <p>
        Your Work.com worker profile is now active.
    </p>

    <br>

    <a
        href="/workers"
        style="
            display:inline-block;
            background:#1769e0;
            color:white;
            padding:13px 22px;
            border-radius:9px;
            text-decoration:none;
            font-weight:700;
        "
    >
        View Workers
    </a>

</div>

</body>

</html>
"""


    except Exception as e:

        print("Registration payment verification error:", e)

        return """
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Payment verification failed.
        </h2>
        """, 400
# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":
    app.run()
