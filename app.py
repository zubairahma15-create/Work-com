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

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

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

/* HEADER */

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
    gap: 25px;
}

nav a {
    text-decoration: none;
    color: #344054;
    font-weight: 600;
}

nav a:hover {
    color: #1769e0;
}

/* HERO */

.hero {
    background: #eef6ff;
    padding: 65px 7%;
}

.hero-content {
    max-width: 1100px;
    margin: auto;
}

.badge {
    display: inline-block;
    background: #e2efff;
    color: #1769e0;
    padding: 9px 16px;
    border-radius: 25px;
    font-weight: 700;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 48px;
    max-width: 650px;
    line-height: 1.1;
    margin-bottom: 18px;
}

.hero h1 span {
    color: #1769e0;
}

.hero p {
    color: #667085;
    font-size: 19px;
    line-height: 1.6;
    max-width: 600px;
    margin-bottom: 30px;
}

/* SEARCH */

.search-box {
    background: white;
    max-width: 750px;
    padding: 10px;
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(16,24,40,.08);
    display: flex;
    gap: 10px;
}

.search-box input {
    flex: 1;
    border: 1px solid #e4e7ec;
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
    padding: 0 25px;
    border-radius: 9px;
    font-weight: 700;
    font-size: 15px;
}

/* SECTIONS */

.container {
    max-width: 1100px;
    margin: auto;
    padding: 60px 20px;
}

.section-label {
    color: #1769e0;
    font-weight: 800;
    margin-bottom: 10px;
}

.section-title {
    font-size: 34px;
    margin-bottom: 10px;
}

.section-text {
    color: #667085;
    font-size: 17px;
    margin-bottom: 30px;
}

/* CATEGORY CARDS */

.category-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.category-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e5e9f0;
    box-shadow: 0 5px 20px rgba(16,24,40,.05);
    text-decoration: none;
    color: #172033;
    transition: .2s;
}

.category-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(16,24,40,.10);
}

.category-icon {
    width: 55px;
    height: 55px;
    background: #eaf3ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin-bottom: 18px;
}

.category-card h3 {
    margin-bottom: 8px;
    font-size: 20px;
}

.category-card p {
    color: #667085;
    font-size: 14px;
    line-height: 1.5;
}

/* HOW IT WORKS */

.how-box {
    background: #eef6ff;
    border-radius: 18px;
    padding: 40px;
}

.steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
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
    font-size: 27px;
    margin: 0 auto 15px;
}

.step h3 {
    margin-bottom: 8px;
}

.step p {
    color: #667085;
    font-size: 14px;
    line-height: 1.5;
}

/* CTA */

.cta {
    max-width: 1100px;
    margin: 0 auto 60px;
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

/* FOOTER */

footer {
    background: #101828;
    color: #cbd5e1;
    padding: 30px 7%;
    display: flex;
    justify-content: space-between;
}

footer strong {
    color: white;
    font-size: 20px;
}

/* MOBILE */

@media (max-width: 700px) {

    header {
        padding: 16px 5%;
    }

    nav {
        gap: 12px;
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
        gap: 25px;
        text-align: center;
    }

    footer {
        flex-direction: column;
        gap: 10px;
        text-align: center;
    }
}

</style>

</head>

<body>

<header>

    <div class="logo">
        Work.com
    </div>

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
        Connect with trusted local professionals
        for your home and business needs.
    </p>

    <form class="search-box"
          method="GET"
          action="/search">

        <input
            type="text"
            name="skill"
            placeholder="Skill (e.g. plumber, carpenter)"
        >

        <input
            type="text"
            name="location"
            placeholder="Location"
        >

        <button
            class="search-btn"
            type="submit">
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
        Find the right professional for your specific needs.
    </p>


    <div class="category-grid">

        <a class="category-card"
           href="/search?skill=Carpenter">

            <div class="category-icon">🔨</div>

            <h3>Carpenter</h3>

            <p>
                Furniture & woodwork
            </p>

        </a>


        <a class="category-card"
           href="/search?skill=Electrician">

            <div class="category-icon">⚡</div>

            <h3>Electrician</h3>

            <p>
                Electrical repair & installation
            </p>

        </a>


        <a class="category-card"
           href="/search?skill=Plumber">

            <div class="category-icon">🚰</div>

            <h3>Plumber</h3>

            <p>
                Water & pipe services
            </p>

        </a>


        <a class="category-card"
           href="/search?skill=Mechanic">

            <div class="category-icon">🔧</div>

            <h3>Mechanic</h3>

            <p>
                Vehicle repair & maintenance
            </p>

        </a>


        <a class="category-card"
           href="/search?skill=Painter">

            <div class="category-icon">🎨</div>

            <h3>Painter</h3>

            <p>
                Interior & exterior painting
            </p>

        </a>


        <a class="category-card"
           href="/search?skill=Mason">

            <div class="category-icon">🧱</div>

            <h3>Mason</h3>

            <p>
                Construction & brickwork
            </p>

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

                <div class="step-icon">
                    👤
                </div>

                <h3>1. Register</h3>

                <p>
                    Register as a skilled worker
                    in just a few minutes.
                </p>

            </div>


            <div class="step">

                <div class="step-icon">
                    🔍
                </div>

                <h3>2. Find Workers</h3>

                <p>
                    Search workers by skill
                    and location.
                </p>

            </div>


            <div class="step">

                <div class="step-icon">
                    ✓
                </div>

                <h3>3. Contact</h3>

                <p>
                    Contact the worker
                    directly.
                </p>

            </div>

        </div>

    </div>

</section>


<section class="cta">

    <div>

        <h2>
            Ready to get your work done?
        </h2>

        <p>
            Register your skills on Work.com today.
        </p>

    </div>

    <a href="/register">
        Register Now
    </a>

</section>


<footer>

    <strong>
        Work.com
    </strong>

    <span>
        © 2026 Work.com · Connecting customers
        with skilled workers
    </span>

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
        <h2 style="font-family:Arial;text-align:center;margin-top:50px;">
            Unable to load workers. Please try again.
        </h2>
        """

    cards = ""

    for worker in worker_list:

        name = escape(worker.get("name", ""))
        skill = escape(worker.get("skill", ""))
        location = escape(worker.get("location", ""))
        experience = escape(worker.get("experience", ""))
        description = escape(worker.get("description", ""))
        phone = escape(worker.get("phone", ""))

        cards += f"""
        <div class="worker-card">

            <div class="worker-top">

                <div class="worker-avatar">
                    {name[:1].upper()}
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
                        <strong>{experience or "Not specified"}</strong>
                    </div>
                </div>

            </div>

            <div class="description">
                {description or "Skilled professional available for work."}
            </div>

            <a class="contact-btn" href="tel:{phone}">
                📞 Contact Worker
            </a>

        </div>
        """

    if not cards:
        cards = """
        <div class="empty-box">
            <div style="font-size:45px;">👷</div>
            <h2>No workers registered yet</h2>
            <p>Worker profiles will appear here after registration.</p>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

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
    box-shadow: 0 5px 20px rgba(16, 24, 40, .06);
    transition: transform .2s, box-shadow .2s;
}}

.worker-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(16, 24, 40, .10);
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

.contact-btn:hover {{
    background: #1258bd;
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

if __name__ == "__main__":
    app.run()
