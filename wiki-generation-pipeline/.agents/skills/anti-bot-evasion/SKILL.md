---
name: anti-bot-evasion
description: Core theory and mechanical explanation of LinkedIn's anti-bot defense systems. Trigger this skill when debugging bans, designing scraping architectures, or when the user proposes bypassing security with dummy accounts or automated logins.
---

# LinkedIn Anti-Bot Evasion Theory

## The Core Principle
LinkedIn employs one of the most aggressive anti-bot defense systems on the internet. It does not just look for "bots"—it looks for the **absence of human imperfection**. Naive automation scripts (like raw Selenium or Playwright) will result in immediate CAPTCHAs or permanent account restrictions.

You must treat LinkedIn scraping as an adversarial evasion task, not a standard DOM parsing task.

---

## 1. Velocity and Consistency (The "Too Fast, Too Perfect" Ban)
* **Fixed Timers:** If your script clicks a profile, waits exactly 3.00 seconds, and clicks the next, you will be caught. Humans are erratic. They take 4.1s, then 8.3s, then 2.1s. All delays MUST be randomized.
* **Volume Constraints:** Viewing 200 profiles in 5 minutes is physically impossible for a human. If you spike your profile views, LinkedIn's rate limiters trigger an automatic restriction. The absolute maximum safe limit is 30-50 profiles per day, spread out.
* **Direct Navigation Anomalies:** Using `page.goto("linkedin.com/in/john-doe")` 200 times sequentially without returning to the feed, running a search, or scrolling triggers detection. Humans click through the UI; they don't teleport to URLs.

## 2. Browser Fingerprinting (The "Headless Ghost" Ban)
* **Headless Mode:** Running Playwright or Selenium in `headless=True` leaves a massive forensic footprint. LinkedIn checks for missing browser plugins, screen resolution anomalies, WebGL rendering discrepancies, and navigator properties. It knows instantly if the browser is headless. **Always use `headless=False`.**
* **Missing User Input / Ghost Clicks:** LinkedIn tracks mouse movements and keystrokes. If elements are being "clicked" via JavaScript (`element.click()`) but the mouse cursor never physically moved across the screen to that coordinate, it's a dead giveaway.

## 3. Authentication Anomalies (The "Injection" Ban)
* **Raw Cookie Injection:** Injecting an `li_at` cookie into a fresh automated browser session without the surrounding context of a real login event (which generates `JSESSIONID`, fingerprinting hashes, and session history) makes the session look forged.
* **Automated Login Forms:** When a script types a password using `.fill()`, it types it at machine speed with zero typos or pauses. LinkedIn detects this keystroke cadence and blocks it. **NEVER automate the login form.**

---

## The Dummy Account Fallacy
A common mistake is attempting to bypass these risks by creating a "dummy" or "test" account. This is structurally flawed and makes the problem worse:

1. **The "Zero Trust" Penalty:** A brand new dummy account has a trust score of absolute zero. The moment a Playwright script touches a fresh account, LinkedIn will instantly throw a CAPTCHA, demand an SMS verification, or restrict it.
2. **The 3rd-Degree Connection Blocker:** A dummy account has 0 connections. LinkedIn aggressively restricts what you can see on profiles outside of your immediate network. To a 0-connection account, target profiles will just show as "LinkedIn Member" with their details hidden. You need a mature account with a populated network to scrape effectively.

---

## The Required Architecture: Manual `storage_state`
To bypass the most dangerous checkpoint (Authentication), you must decouple the login from the scraper:

1. **Manual Session Creation:** A script opens a visible browser and waits for the human operator to type their credentials and solve any 2FA/CAPTCHAs.
2. **State Persistence:** The entire browser state (all cookies, local storage, session IDs) is saved to a `session.json` file.
3. **Automated Scraping:** The actual scraper loads that `session.json` into a visible (`headless=False`), artificially slowed (`slow_mo=150`) browser. By inheriting the full state of a legitimate human login, it inherits that "human" trust score.
