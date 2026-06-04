# 🌍 AI Travel Planner

An AI-powered travel planning web app built with **Streamlit** and **Groq (LLaMA 3.3)** that generates personalized day-by-day travel itineraries for destinations around the world.

---

## 🚀 Live Demo

[![Streamlit App](https://f47m86qxhgba3yqmchdtxh.streamlit.app/)

---

## ✨ Features

- 🗺️ **Pre-defined Countries** — Browse top tourist places with photos for 20+ countries
- ✏️ **Custom Trip Planner** — Enter any country and places to get a custom itinerary
- 🤖 **AI-Generated Itineraries** — Day-wise plans with hotels, transport, and tips
- 📸 **Place Cards** — Visual cards for each destination with images and descriptions
- ⚡ **Fast Responses** — Powered by Groq's ultra-fast LLaMA 3.3 70B model

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Streamlit | Web UI Framework |
| Groq API | AI Language Model |
| LLaMA 3.3 70B | Trip plan generation |
| Python | Backend logic |

---

## 📦 Installation (Local)

**1. Clone the repository**
```bash
git clone https://github.com/zohaawan35-glitch/-AI-Travel-Planner.git
cd -AI-Travel-Planner
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API Key**

Create a file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
```

> ⚠️ Never upload this file to GitHub — add it to `.gitignore`

**4. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → select your repo
4. Go to **Settings → Secrets** and add:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
```
5. Click **Deploy** ✅

---

## 🔑 Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Click **API Keys → Create API Key**
4. Copy and paste into Streamlit Secrets

---

## 📁 Project Structure

```
-AI-Travel-Planner/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .streamlit/
    └── secrets.toml    # API keys (do NOT push to GitHub)
```

---

## 🌐 Supported Countries

United States, Canada, United Kingdom, Germany, France, Spain, Italy, Turkey, UAE, Saudi Arabia, Japan, China, India, Pakistan, Thailand, Indonesia, Malaysia, Singapore, Australia, New Zealand, Brazil, Mexico, Argentina, Egypt

---

## 📋 Requirements

```
streamlit
groq
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Zohaawan** — [@zohaawan35-glitch](https://github.com/zohaawan35-glitch)
