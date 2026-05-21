# Student Mental Health & the COVID Crisis
### SQL Data Pipeline & Longitudinal Analysis | 398,884 Students · 4 Years · Pre/During/Post COVID

[View Live Tableau Dashboard](https://public.tableau.com/app/profile/shweta.kataria/viz/StudentMentalHealththeCOVIDCrisis/Dashboard1)

---

## The Question

Universities scaled up mental health support during COVID. But did it actually help students academically?

This project analyzes 4 years of student mental health survey data — before, during, and after the pandemic — to find out.

---

## The Finding

**Mental health symptoms peaked in Early Recovery (2021-2022), not during COVID.**

Depression rates rose from 37% pre-COVID to 73% in early recovery — nearly double. Academic impairment stayed above 79% across all 4 years regardless of therapy access. Universities pulled back support (therapy access dropped from 55% to 29%) exactly when students needed it most.

The uncomfortable conclusion: universities were measuring the wrong thing. Tracking therapy access is not the same as tracking whether students are actually recovering academically.

---

## The Data

**Source:** Healthy Minds Study (HMS) — the largest longitudinal survey of college student mental health in the US.

| Year | Period | Students |
|---|---|---|
| 2019-2020 | Pre-COVID | 88,702 |
| 2020-2021 | During COVID | 137,916 |
| 2021-2022 | Early Recovery | 95,860 |
| 2022-2023 | Post-COVID | 76,406 |
| **Total** | **4 years** | **398,884** |

Each year's dataset had 900-1,600 columns with inconsistent naming, different scale types, and missing values across years.

---

## What I Built

### 1. SQL Data Pipeline
Loaded all 4 raw CSVs into a SQLite database using Python. Rather than cleaning in Excel, all standardization was done in SQL — preserving raw data and maintaining full data lineage.

Key challenges solved:
- Column names changed across years (`ther_cur` vs `ther_cur1`)
- Scale types changed (`depression` was 0-10 in 2021-2022 but 0/1 flag in other years)
- Text responses in 2020-2021 (`Yes/No` instead of `1/0`, `1-2 days` instead of numeric scale)
- Unified 4 inconsistent datasets into one 398,884-row master table

### 2. Analysis Queries
Five SQL queries answering the core research questions:
- Year-over-year trends across all indicators
- Therapy access vs academic impairment gap
- Does treatment actually reduce impairment?
- Who is most at risk by degree level?
- Who is most at risk by gender?

### 3. Tableau Dashboard
Interactive dashboard published to Tableau Public with 4 charts:
- The COVID Arc — depression, impairment, therapy across all 4 periods
- The Gap — therapy access vs academic impairment over time
- Risk by Gender — non-binary students show highest impairment (95%)
- Risk by Degree — undergraduates most affected

---

## Key Findings

**The COVID Arc**
- Depression: 37% → 41% → 73% → 40% (peaked in Early Recovery, not during COVID)
- Academic Impairment: 80% → 66% → 85% → 81% (never dropped below 66%)
- Therapy access: 14% → 55% → 55% → 29% (pulled back post-COVID)

**The Gap**
- Pre-COVID: 80% impaired, only 14% in therapy — 66 point gap
- During COVID: universities scaled up therapy, gap narrowed to 11 points
- Post-COVID: therapy dropped back, gap widened to 53 points

**Who Got Left Behind**
- Non-binary students: 84% depression rate, 95% academic impairment
- Undergraduates: highest depression (52%) and impairment (84%) by degree level
- Men: least likely to access therapy (30%) despite significant depression rates (51%)

**Does Treatment Help?**
- Students with no therapy and no medication: 77% academically impaired
- Students with both therapy and medication: 90% academically impaired
- This is not evidence treatment fails — sicker students seek more treatment. But it shows clinical access alone does not guarantee academic recovery.

---

## Recommendation

Universities need outcome-based mental health metrics, not just access metrics. Counting students in therapy is not the same as measuring whether students are functioning better academically. The data suggests a structural gap between mental health support and academic support that neither system is currently bridging.

---

## Technologies Used

- **Python** — data loading, orchestration, CSV export
- **SQLite / SQL** — database creation, data cleaning, all analysis queries
- **Pandas** — dataframe handling and export
- **Tableau Public** — interactive dashboard

---

## Files

- `mental_health.py` — full Python + SQL pipeline
- Raw data: [Healthy Minds Study](https://healthymindsnetwork.org/) (not included due to size)
