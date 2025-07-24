# ✏️ Pencil — The Journal for Builders

Pencil is a collaboration-first journaling platform built for developers, designers, researchers, and anyone building something from scratch.

Whether you're documenting a solo project or working in a team, Pencil gives you versioned journals, Markdown writing, real-time collaboration, and the ability to share or publish your work.

Live at: [https://pencil-909v.onrender.com](https://pencil-909v.onrender.com)

---

## 🧠 Why Pencil Exists

This is the first project I built using Django **without following any tutorial**.

I learned the basics from a Udemy course, then built this from scratch to figure out how Django and AWS work together in practice. It helped me explore user auth, file storage, collaborative permissions, and cloud deployment — the things you actually need to build useful software.

---

## 🚀 Features

- **Authentication**
  - Full user login, signup, and logout system using Django auth.
  
- **Journals & Entries**
  - Create multiple private journals.
  - Journals are versioned and entries are timestamped.
  - Add, edit, or delete entries.
  - Delete entire journals when needed.

- **Markdown + Export**
  - Entries are written in Markdown and rendered beautifully.
  - Export journals as `.md` files or downloadable PDFs.

- **Media Support**
  - Add images or other media to your entries.
  - All files are stored securely in an **AWS S3** bucket and accessible across users.

- **Sharing & Permissions**
  - Share any journal with another user.
  - Grant edit access or keep it read-only.

- **Public Journals**
  - Make journals public to showcase them on the global feed.

- **Frontend**
  - Built using Django Template Language (DTL) and Tailwind CSS.

---

## 🛠 Tech Stack

| Area        | Tech                   |
|-------------|------------------------|
| Backend     | Django (Python)        |
| Frontend    | Django Templates + Tailwind |
| Auth        | Django Authentication  |
| Database    | PostgreSQL             |
| File Upload | AWS S3                 |
| Export      | Markdown + PDF (ReportLab) |
| Hosting     | Render.com             |

---

## 🧪 Try It Out

Visit the live site:  
👉 [https://pencil-909v.onrender.com](https://pencil-909v.onrender.com)

You can sign up, create a private journal, and explore all the features — including Markdown writing, sharing, and media uploads. Everything just works, including AWS-backed file storage.

---

## 📦 Setup (Optional for Devs)

If you want to run Pencil locally:

```bash
# Clone the repo
git clone https://github.com/yourusername/pencil.git
cd pencil

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file required for AWS + Django secret)
# Run migrations
python manage.py migrate

# Run the development server
python manage.py runserver
 ```
---

## 🙌 Final Words

Pencil isn’t perfect — and that’s the point.

This project is a starting point I built from scratch to **understand how Django and AWS fit together** in a real-world app. It helped me learn authentication, file handling, permissions, Markdown rendering, and deploying to the cloud — all in one place.

More importantly, I built Pencil to be **useful**. I wanted a tool to track progress, write down ideas, and share work with collaborators — without bloated features or distractions.

If you're someone who builds things — solo or in a team — give Pencil a try.  
Start a journal. Share it. Build something.

**Feedback and contributions are welcome.**

---

## 🪪 License

This project is open-sourced under the MIT License.

---

## 🧑‍💻 Author

Built by [Your Name]  
Computer Engineering Graduate · Learning Django + AWS · [India]  

