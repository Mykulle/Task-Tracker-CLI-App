# Task-Tracker-CLI-App
📌 Project Overview

This is a Command Line Interface (CLI) Task Tracker built with Python. It allows users to add, update, delete, and manage tasks while storing data in an SQLite database and syncing with a JSON file for easy access and persistence.

This application is built using Typer for CLI interactions and Rich for colorful and structured output.

✨ Features

✅ Add Tasks with category

🔄 Update Tasks (name, category, status)

🗑️ Delete Tasks by position

⏳ Mark Tasks as In-Progress

✅ Mark Tasks as Done

📋 View Tasks with filtering options:

- List all tasks

- List completed tasks

- List in-progress tasks

- List not done tasks

📦 Sync Tasks to JSON for easy data storage

🔄 Reset Database to start fresh

🚀 Technologies Used

Python 🐍

- SQLite (Database Storage)

- JSON (Data Syncing)

- Typer (CLI Framework)

- Rich (Beautiful CLI Output)

🔧 Installation

1️⃣ Clone the Repository

git clone https://github.com/Mykulle/Task-Tracker-CLI-App.git
cd Task-Tracker-CLI-App

2️⃣ Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate    # Windows

3️⃣ Install Required Dependencies

pip install -r requirements.txt

📜 Usage

✅ Add a Task

python cli.py add "Learn Python" "Study"

📋 List All Tasks

python cli.py show

✅ List Only Completed Tasks

python cli.py show --listtype done

🔄 Update a Task

python cli.py update 1 --task "Learn Advanced Python" --category "Programming"

🗑️ Delete a Task

python cli.py delete 1

⏳ Mark a Task as In-Progress

python cli.py update 1 --status 2

✅ Mark a Task as Done

python cli.py complete 1

🔄 Reset Database

python cli.py reset_db

📂 Project Structure

Task-Tracker-CLI-App/
│── cli.py               # Main CLI application
│── database.py          # Database & JSON sync functions
│── model.py             # Task model
│── tasks.json           # JSON storage for tasks
│── todos.db             # SQLite database
│── requirements.txt     # Dependencies
│── README.md            # Project documentation

⚠️ Known Issues

Currently, no due date/reminder feature (planned for future release!)

Better error handling needed for invalid inputs

🔥 Future Enhancements

⏰ Task Reminders & Due Dates

📊 Statistics on Completed & Pending Tasks

🌍 Cloud Sync Support

📦 Package as a pip install CLI tool

🎯 Contributing

Want to contribute? 🚀 Feel free to fork the repo and submit a pull request!

Fork the repo

Create a feature branch

Commit your changes

Push to your fork & create a PR

📜 License

This project is licensed under the MIT License.

🤝 Acknowledgments

Special thanks to Typer & Rich for making CLI development awesome!

📞 Contact

For any questions, feel free to reach out:

GitHub: Mykulle

Email: C230183@e.ntu.edu.sg


