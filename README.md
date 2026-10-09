<div align="center">

# 💎 Smart Job Tracker & AI Insights

> **Dashboard 3D Glassmorphic alimentat de Google Gemini AI pentru managementul inteligent al carierei.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## 🎯 Funcționalități Principale

* 🧊 **Design 3D Glassmorphic:** Interfață modernă cu efecte de sticlă, blur dinamic și borduri luminoase construite cu Tailwind CSS.
* 🤖 **Copilot AI Gemini:** Analiză automată a aplicărilor, oferire de feedback instant și sugestii de optimizare a CV-ului.
* ⚡ **Experiență Fluentă (Async):** Actualizări în timp real fără reîncărcarea paginii (Fetch API + Modal AI).
* 🗄️ **Persistență Date:** Salvare locală structurată folosind Flask-SQLAlchemy și SQLite.

---

## 🏗️ Arhitectura Sistemului

```text
┌─────────────────────────┐       Async Fetch       ┌─────────────────────────┐
│  Frontend Glassmorphism │ ──────────────────────> │      Backend Flask      │
│   (Tailwind + JS DOM)   │ <────────────────────── │   (Routes / ORM Logic)  │
└─────────────────────────┘       JSON Response     └────────────┬────────────┘
                                                                     │
                                                   ┌─────────────────┴─────────────────┐
                                                   ▼                                   ▼
                                        ┌─────────────────────┐             ┌─────────────────────┐
                                        │  SQLite Database    │             │ Google Gemini AI    │
                                        │ (Job Applications)  │             │ (Career Insights)   │
                                        └─────────────────────┘             └─────────────────────┘
