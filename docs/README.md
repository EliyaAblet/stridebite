# StrideBite — User Stories, Mis-User Stories, Mockups, and Architecture

## User Stories (with Acceptance Criteria)

1. As a **trainee**, I want to **log a workout (run/strength/treadmill)** so I can **track training volume over time**.  
   **Acceptance:** From the dashboard I can add a workout with type, duration, and distance/sets-reps; it appears in Today Summary and the list.

2. As a **trainee**, I want to **record a meal with protein and calories** so I can **hit my daily protein goal**.  
   **Acceptance:** I can add food entries with protein (g) and calories; daily totals and a 7-day chart render.

3. As a **trainee**, I want to **log my weight** so I can **see body-weight trends**.  
   **Acceptance:** I can enter weight for any date; a line chart shows a 7-day rolling average.

4. As a **trainee**, I want to **upload a progress photo** so I can **visually compare changes**.  
   **Acceptance:** I can upload an image; a thumbnail appears on the day view; file stored privately.

5. As a **trainee**, I want to **log sleep hours** so I can **correlate sleep with workout quality**.  
   **Acceptance:** I can input hours slept per date; a weekly bar chart renders.

6. As a **user**, I want to **export my data** so I can **own/back up my logs**.  
   **Acceptance:** I can export CSV/JSON within a selected date range; file downloads.

7. As a **user**, I want to **sign in securely** so I can **protect my data**.  
   **Acceptance:** Email/password auth; password reset; logout; session expiry.

8. As a **user**, I want a **Today Summary** so I can **see protein, calories, workout, weight, and sleep at a glance**.  
   **Acceptance:** Dashboard shows today’s totals and last-7-day mini-charts.

---

## Mis-User Stories & Mitigation Criteria

1. As a **malicious actor**, I want to **brute-force logins** so I can **access private data**.  
   **Mitigation:** Rate-limit auth; lockout/backoff; password complexity; HTTPS only; CSRF protection.

2. As a **malicious actor**, I want to **upload a poisoned image** so I can **exploit file parsing**.  
   **Mitigation:** Validate MIME/extension; size limits; randomized filenames; store outside static root.

3. As a **malicious actor**, I want to **enumerate users** to **target accounts**.  
   **Mitigation:** Uniform login errors; no user-enumeration behavior.

4. As a **malicious actor**, I want to **inject script into fields** so I can **steal sessions**.  
   **Mitigation:** Auto-escape templates; sanitize user input; CSP headers.

5. As a **malicious actor**, I want to **export another user's data**.  
   **Mitigation:** Strict per-user access rules; rate limiting; session verification.

---

## Low-Fidelity UI Mockups (Mermaid)

### Dashboard (Today Summary)

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
