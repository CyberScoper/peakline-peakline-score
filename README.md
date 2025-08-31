# 🏆 PeakLine Score

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/CyberScoper/peakline-peakline-score/blob/main/LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-The_Peakline-brightgreen.svg)](https://www.thepeakline.com/)

This repository contains the backend logic and frontend template for the **PeakLine Score (PLS)** feature, a custom performance metric for **The Peakline** project. This code handles all the math and logic for calculating an athlete's rating based on their Strava data.

Article on Habr: https://habr.com/ru/articles/942444/

---

<img width="1165" height="1264" alt="image" src="https://github.com/user-attachments/assets/4436a090-d021-4c81-9fb6-751775c31dfa" />

---

## ✨ Core Logic

*   📈 **Calculation of a score for a single activity** based on comparing the actual time with the "ideal" time of a hypothetical super-athlete.
*   🥇 **Calculation of the user's overall rating** based on the average of the 6 best results, which filters out unsuccessful or recovery workouts.
*   🏔️ **Automatic terrain classification** (flat, hills, mountains) for the correct application of difficulty coefficients.
*   🏅 **Determination of performance level** (from 'Needs Improvement' to 'Elite') for a clear interpretation of the result.
*   💡 **Generation of personalized improvement tips** depending on the user's current level.

## 💻 Tech Stack

*   **Backend:** Python
*   **Templating:** Jinja2
*   **Frontend (Template):** HTML5, CSS3

---

## 📜 Important License Information

The source code in this repository is published **for informational and educational purposes only**. It demonstrates my skills and architectural decisions.

> **You are PROHIBITED from:**
> *   Copying, modifying, distributing, or reusing this code (or its parts) in your own projects (commercial or non-commercial).
> *   Creating derivative works (forks) for development purposes.
> *   Selling or sublicensing this code.
>
> All rights to this code are reserved. For details, see the `LICENSE.md` file.

---

⚠️ **This is NOT an open-source project.** ⚠️

> **You are strictly PROHIBITED from:**
> *   Copying, modifying, distributing, or reusing this code (or any part of it) in your own projects (commercial or non-commercial).
> *   Creating derivative works (for development purposes).
> *   Selling or sublicensing this code.
>
> All rights are reserved. For more details, see the `LICENSE.md` file.

---

## 💬 Feedback & Suggestions

Despite the closed license, I would be very happy to receive your feedback! If you have read the article on Habr and have ideas for improving the algorithm or have found a logical error, please create an **[Issue](https://github.com/CyberScoper/peakline-peakline-score/issues)**.

*Please note: Pull requests with code will not be accepted.*

## 🌲 About The Peakline Project

**PeakLine Score** is just one feature of the larger **[The Peakline](https://www.thepeakline.com/)** project. Visit the website to learn more
