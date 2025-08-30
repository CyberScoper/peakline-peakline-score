# 🏆 PeakLine Score

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/CyberScoper/peakline-peakline-score/blob/main/LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-The_Peakline-brightgreen.svg)](https://www.thepeakline.com/)

Бэкенд-часть и шаблон для фичи **PeakLine Score (PLS)** — кастомной метрики производительности для проекта **The Peakline**. Этот код отвечает за всю математику и логику расчета рейтинга атлета на основе данных из Strava.

Статья на Хабр: https://habr.com/ru/articles/942444/

This repository contains the backend logic and frontend template for the **PeakLine Score (PLS)** feature, a custom performance metric for **The Peakline** project. This code handles all the math and logic for calculating an athlete's rating based on their Strava data.

---

<img width="1266" height="979" alt="Screenshot 2025-08-30 233204" src="https://github.com/user-attachments/assets/79f6fb1c-4ace-43b7-a2f1-d0944204ebfc" />

---

## ✨ Основная логика (Core Logic)

*   📈 **Расчет балла для одной активности** на основе сравнения фактического времени с "идеальным" временем гипотетического супер-атлета.
*   🥇 **Вычисление общего рейтинга пользователя** на основе среднего из 6 лучших результатов, что отсекает неудачные или восстановительные тренировки.
*   🏔️ **Автоматическая классификация рельефа** (равнина, холмы, горы) для корректного применения коэффициентов сложности.
*   🏅 **Определение уровня производительности** (от 'Needs Improvement' до 'Elite') для понятной интерпретации результата.
*   💡 **Генерация персонализированных советов** по улучшению в зависимости от текущего уровня пользователя.

## 💻 Технологический стек (Tech Stack)

*   **Backend:** Python
*   **Templating:** Jinja2
*   **Frontend (Template):** HTML5, CSS3

---

## 📜 **Важная информация о лицензии / Important License Information**

Исходный код в этом репозитории опубликован **только для ознакомительных и образовательных целей**. Он демонстрирует мои навыки и архитектурные решения.

> **Вам ЗАПРЕЩЕНО:**
> *   Копировать, изменять, распространять или переиспользовать этот код (или его части) в своих проектах (коммерческих или некоммерческих).
> *   Создавать производные работы (форки) с целью разработки.
> *   Продавать или сублицензировать данный код.
>
> Все права на данный код защищены. Подробности смотрите в файле `LICENSE.md`.

---

⚠️ **This is NOT an open-source project.** ⚠️

> **You are strictly PROHIBITED from:**
> *   Copying, modifying, distributing, or reusing this code (or any part of it) in your own projects (commercial or non-commercial).
> *   Creating derivative works (for development purposes).
> *   Selling or sublicensing this code.
>
> All rights are reserved. For more details, see the `LICENSE.md` file.

---

## 💬 Фидбэк и предложения (Feedback & Suggestions)

Несмотря на закрытую лицензию, я буду очень рад вашему фидбэку! Если вы ознакомились со статьей на Хабре и у вас есть идеи по улучшению алгоритма или вы нашли логическую ошибку, пожалуйста, создайте **[Issue](https://github.com/CyberScoper/peakline-peakline-score/issues)**.

*Обратите внимание: Pull Request'ы с кодом приниматься не будут.*

## 🌲 О проекте The Peakline

**PeakLine Score** — это лишь одна из фич большого проекта **[The Peakline](https://www.thepeakline.com/)**. Заходите на сайт, чтобы узнать больше!
