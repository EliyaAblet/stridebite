# StrideBite – User Stories, Mis-User Stories, Mockups, and Architecture

This document outlines the planned behavior of the StrideBite fitness tracking app.  
It includes user stories, acceptance criteria, mis-user scenarios, mockups, and system diagrams.  
The purpose is to show how the app is expected to work from both normal and adversarial perspectives.

---

## User Stories (with Acceptance Criteria)

1. As a trainee, I want to log a workout (run, strength, or treadmill) so I can track my training volume over time.  
   Acceptance: From the dashboard, I can add a workout with type, duration, and distance/sets/reps. It appears in the daily summary and the list.

2. As a trainee, I want to record a meal with protein and calories so I can meet my daily nutrition goals.  
   Acceptance: I can add food entries with protein and calories. Totals for the day update and a 7-day chart reflects trends.

3. As a trainee, I want to log my weight so I can monitor my body-weight changes over time.  
   Acceptance: I can enter a weight for any date, and a weekly rolling line chart shows progress.

4. As a trainee, I want to upload a progress photo so I can visually compare changes.  
   Acceptance: I can upload an image that becomes a thumbnail on the daily view. Files are stored privately.

5. As a trainee, I want to log sleep hours so I can see how sleep affects my training quality.  
   Acceptance: I can enter hours slept per day, and a weekly bar chart appears on the dashboard.

6. As a user, I want to export my data so I can save or back up my logs.  
   Acceptance: I can download CSV or JSON files within a chosen date range.

7. As a user, I want to sign in securely so I can protect my account data.  
   Acceptance: The system requires email/password, password reset, and session expiration.

8. As a user, I want a clear daily summary so I can quickly see protein, calories, workout info, weight, and sleep at a glance.  
   Acceptance: The dashboard shows today’s totals and small charts for the last seven days.

---

## Mis-User Stories and Mitigation

1. As a malicious actor, I want to perform brute-force logins so I can access private data.  
   Mitigation: Rate limiting, account lockout, strong password rules, HTTPS, and CSRF protection.

2. As a malicious actor, I want to upload a poisoned image file so I can attempt code execution.  
   Mitigation: Validate MIME types, restrict file extensions, limit size, and store files outside the static root.

3. As a malicious actor, I want to scrape user data through automated requests.  
   Mitigation: API throttling, required authentication, and session rotation.

4. As a malicious actor, I want to inject SQL into form fields so I can access unauthorized records.  
   Mitigation: Use Django ORM parameterization and built-in validation.

5. As a malicious actor, I want to tamper with requests so I can impersonate other users.  
   Mitigation: Use session middleware, authentication checks, and server-side permission controls.

---

## Visual Mockups (Text-Based Approximation)

### Dashboard Layout (Concept)

```mermaid
flowchart TD
A[Navbar\nHome | Log | Export | Profile] --> B[Today Summary\nProtein/Calories/Workout/Weight/Sleep]
B --> C[Quick Add\nMeal | Workout | Weight | Sleep]
B --> D[Week Trends\nMini charts]
C --> E[Recent Entries List]
```

---

### One-Page Combined Overview (Dashboard + Log Meal + Log Workout + C4 Snapshot)

```mermaid
flowchart LR

subgraph UI[UI Flows]
  direction TB

  subgraph DASH[Dashboard (Today Summary)]
    D1[Open Dashboard]
    D2[Today Summary:\nProtein · Calories · Workout · Weight · Sleep]
    D3[Week Trends (mini-charts)]
    D4[Quick Add: Meal · Workout · Weight · Sleep]
    D1 --> D2 --> D3 --> D4
  end

  subgraph LM[Log Meal]
    LM1[Open 'Log Meal' form]
    LM2[Food name]
    LM3[Protein (g)]
    LM4[Calories]
    LM5[Time]
    LM6[(Save)]
    LM1 --> LM2 --> LM3 --> LM4 --> LM5 --> LM6
  end

  subgraph LW[Log Workout]
    LW1[Open 'Log Workout' form]
    LW2{Type?}
    LW2 -->|Run| LW3R[Distance]
    LW2 -->|Strength| LW3S[Sets & Reps]
    LW2 -->|Treadmill| LW3T[Duration/Incline]
    LW4[Duration]
    LW5[RPE (1–10)]
    LW6[(Save)]
    LW1 --> LW2
    LW3R --> LW4 --> LW5 --> LW6
    LW3S --> LW4
    LW3T --> LW4
  end
end

LM6 --> APP[StrideBite Web App]
LW6 --> APP
D4 --> APP

subgraph C4[Architecture Snapshot (C1/C2/C3)]
  direction TB

  subgraph C1[Context]
    U[User] --> APP
  end

  subgraph C2[Container]
    BROWSER[Browser] --> DJANGO[Django App (REST + Templates)]
    DJANGO --> DB[(Postgres/SQLite)]
    DJANGO --> MEDIA[(Media Storage)]
  end

  subgraph C3[Component]
    API[REST Views] --> SVC[Domain Services]
    SVC --> REPO[Repositories]
    REPO --> MODELS[Django Models]
  end
end

APP --> DJANGO
DJANGO -.persist.-> DB
DJANGO -.store.-> MEDIA
```
