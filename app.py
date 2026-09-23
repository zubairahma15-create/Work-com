
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Work.com</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 0;
            }

            header {
                background: #2563eb;
                color: white;
                padding: 20px;
                text-align: center;
            }

            .container {
                max-width: 500px;
                margin: 40px auto;
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            input, textarea, button {
                width: 100%;
                padding: 12px;
                margin-top: 8px;
                margin-bottom: 15px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                background: #2563eb;
                color: white;
                border: none;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            h2 {
                color: #222;
            }
        </style>
    </head>

    <body>

        <header>
            <h1>Work.com</h1>
            <p>Find skilled workers near you</p>
        </header>

        <div class="container">
            <h2>Worker Registration</h2>

            <form method="POST" action="/register">

                <label>Full Name</label>
                <input type="text" name="name" placeholder="Enter your name" required>

                <label>Skill / Profession</label>
                <input type="text" name="skill" placeholder="e.g. Carpenter, Mechanic" required>

                <label>Phone Number</label>
                <input type="tel" name="phone" placeholder="Enter phone number" required>

                <label>Location</label>
                <input type="text" name="location" placeholder="Enter your location" required>

                <label>Experience</label>
                <input type="text" name="experience" placeholder="e.g. 5 years">

                <label>Description</label>
                <textarea name="description" rows="4"
                    placeholder="Tell customers about your work"></textarea>

                <button type="submit">Register as Worker</button>

            </form>
        </div>

    </body>
    </html>
    """


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    skill = request.form.get("skill")
    phone = request.form.get("phone")
    location = request.form.get("location")
    experience = request.form.get("experience")
    description = request.form.get("description")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registration Successful - Work.com</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="font-family: Arial; text-align: center; padding: 40px;">

        <h1>Work.com</h1>

        <h2>Worker Registered Successfully! 🎉</h2>

        <p><strong>Name:</strong> {name}</p>
        <p><strong>Skill:</strong> {skill}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Location:</strong> {location}</p>
        <p><strong>Experience:</strong> {experience}</p>
        <p><strong>Description:</strong> {description}</p>

        <br>

        <a href="/">
            <button style="padding: 12px 25px;">
                Register Another Worker
            </button>
        </a>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()
