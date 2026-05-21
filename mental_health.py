import pandas as pd
import sqlite3
import os

conn = sqlite3.connect('mental_health.db')

# ============================================================
# STEP 1 — LOAD RAW FILES (only needed columns)
# ============================================================

# Columns we need from each year
cols_2019 = ['responseid','age','yr_sch','degree_bach','degree_ma','degree_phd',
             'gender','dep_any','anx_any','aca_impa','dep_impa','gad7_impa',
             'sui_idea','suic_plan','suic_att','sib_any','ther_ever','ther_cur',
             'meds_any','tx_any','dx_any','dx_dep','dx_ax','mh_prior']

cols_2020 = ['responseid','age','yr_sch','degree_bach','degree_ma','degree_phd',
             'gender_male','gender_female','gender_nonbin','dep_any','anx_any',
             'aca_impa','dep_impa','gad7_impa','sui_idea','suic_plan','suic_att',
             'sib_any','ther_ever','ther_cur1','meds_any','tx_any','dx_any',
             'dx_dep','dx_anx','mh_prior']

cols_2021 = ['responseid','age','yr_sch','degree_bach','degree_ma','degree_phd',
             'gender_male','gender_female','gender_nonbin','depression','anxiety',
             'aca_impa','dep_impa','gad7_impa','sui_idea','sui_plan','sui_att',
             'sib_any','ther_ever','ther_cur','meds_any','tx_any','dx_any',
             'dx_dep','dx_anx','mh_prior']

cols_2022 = ['responseid','age','yr_sch','degree_bach','degree_ma','degree_phd',
             'gender_male','gender_female','gender_nonbin','dep_any','anx_any',
             'aca_impa','dep_impa','gad7_impa','sui_idea','sui_plan','sui_att',
             'sib_any','ther_ever','ther_cur','meds_any','tx_any','dx_any',
             'dx_dep','dx_anx','mh_prior_clim']

files = [
    ('raw_2019_2020', 'HMS_2019-2020.csv', cols_2019),
    ('raw_2020_2021', 'HMS_2020-2021.csv', cols_2020),
    ('raw_2021_2022', 'HMS_2021-2022.csv', cols_2021),
    ('raw_2022_2023', 'HMS_2022-2023.csv', cols_2022),
]

for table, filepath, usecols in files:
    df = pd.read_csv(filepath, usecols=usecols, low_memory=False)
    df.to_sql(table, conn, if_exists='replace', index=False)
    print(f"{table}: {len(df)} rows, {len(df.columns)} columns")

print("\nAll raw files loaded.")

# ============================================================
# STEP 2 — CLEAN EACH YEAR INDIVIDUALLY
# ============================================================

# ---------- 2019-2020 ----------
# dep_any and anx_any are already 0/1 flags
# gender is a single column with text values
# ther_cur = therapy current (0/1)
# suic_plan / suic_att (note: different spelling from later years)

clean_2019 = conn.execute("""
    SELECT
        responseid                              AS student_id,
        '2019-2020'                             AS academic_year,
        'Pre-COVID'                             AS covid_period,
        age,
        yr_sch                                  AS year_of_study,

        CASE
            WHEN degree_bach = 1 THEN 'Undergraduate'
            WHEN degree_ma   = 1 THEN 'Graduate'
            WHEN degree_phd  = 1 THEN 'PhD'
            ELSE 'Other'
        END AS degree_level,

        CASE
            WHEN LOWER(gender) LIKE '%woman%'   THEN 'Woman'
            WHEN LOWER(gender) LIKE '%man%'     THEN 'Man'
            WHEN LOWER(gender) LIKE '%non%'     THEN 'Non-binary'
            WHEN LOWER(gender) LIKE '%trans%'   THEN 'Non-binary'
            ELSE 'Other/Not reported'
        END AS gender,

        dep_any                                 AS depression,
        anx_any                                 AS anxiety,

        CASE WHEN aca_impa >= 2 THEN 1
             WHEN aca_impa =  1 THEN 0
             ELSE NULL END                      AS academic_impairment,

        CASE WHEN dep_impa >= 2 THEN 1
             WHEN dep_impa =  1 THEN 0
             ELSE NULL END                      AS depression_impairment,

        CASE WHEN gad7_impa >= 2 THEN 1
             WHEN gad7_impa =  1 THEN 0
             ELSE NULL END                      AS anxiety_impairment,

        sui_idea                                AS suicidal_ideation,
        suic_plan                               AS suicidal_plan,
        suic_att                                AS suicide_attempt,
        sib_any                                 AS self_harm_any,

        CASE WHEN ther_ever >= 1 THEN 1
             ELSE NULL END                      AS therapy_ever,
        ther_cur                                AS therapy_current,
        meds_any                                AS medication_any,
        tx_any                                  AS treatment_any,
        dx_any                                  AS diagnosis_any,
        dx_dep                                  AS dx_depression,
        dx_ax                                   AS dx_anxiety,
        mh_prior                                AS mh_prior

    FROM raw_2019_2020
    WHERE responseid IS NOT NULL
""").fetchall()

print(f"Clean 2019-2020: {len(clean_2019)} rows")

# ---------- 2020-2021 ----------
# gender splits into gender_male, gender_female etc
# ther_cur1 (note the 1 at the end)
# suic_plan / suic_att (same spelling as 2019)
# dep_any and anx_any are 0/1 flags

clean_2020 = conn.execute("""
    SELECT
        responseid                              AS student_id,
        '2020-2021'                             AS academic_year,
        'During COVID'                          AS covid_period,
        age,
        yr_sch                                  AS year_of_study,

        CASE
            WHEN degree_bach = 1 THEN 'Undergraduate'
            WHEN degree_ma   = 1 THEN 'Graduate'
            WHEN degree_phd  = 1 THEN 'PhD'
            ELSE 'Other'
        END AS degree_level,

        CASE
            WHEN gender_male   = 1 THEN 'Man'
            WHEN gender_female = 1 THEN 'Woman'
            WHEN gender_nonbin = 1 THEN 'Non-binary'
            ELSE 'Other/Not reported'
        END AS gender,

        dep_any                                 AS depression,
        anx_any                                 AS anxiety,

        CASE WHEN aca_impa IN ('3-5 days','6 or more days') THEN 1
             WHEN aca_impa = '1-2 days' THEN 0
             ELSE NULL END                      AS academic_impairment,

        CASE WHEN dep_impa >= 2 THEN 1
             WHEN dep_impa =  1 THEN 0
             ELSE NULL END                      AS depression_impairment,

        CASE WHEN gad7_impa >= 2 THEN 1
             WHEN gad7_impa =  1 THEN 0
             ELSE NULL END                      AS anxiety_impairment,

        CASE WHEN sui_idea  = 'Yes' THEN 1 WHEN sui_idea  = 'No' THEN 0 ELSE NULL END AS suicidal_ideation,
        CASE WHEN suic_plan = 'Yes' THEN 1 WHEN suic_plan = 'No' THEN 0 ELSE NULL END AS suicidal_plan,
        CASE WHEN suic_att  = 'Yes' THEN 1 WHEN suic_att  = 'No' THEN 0 ELSE NULL END AS suicide_attempt,
        sib_any                                 AS self_harm_any,

        CASE WHEN ther_ever >= 1 THEN 1
             ELSE NULL END                      AS therapy_ever,
        CASE WHEN ther_cur1 = 'Yes' THEN 1
             WHEN ther_cur1 = 'No'  THEN 0
             ELSE NULL END                      AS therapy_current,
        meds_any                                AS medication_any,
        tx_any                                  AS treatment_any,
        dx_any                                  AS diagnosis_any,
        dx_dep                                  AS dx_depression,
        dx_anx                                  AS dx_anxiety,
        mh_prior                                AS mh_prior

    FROM raw_2020_2021
    WHERE responseid IS NOT NULL
""").fetchall()

print(f"Clean 2020-2021: {len(clean_2020)} rows")

# ---------- 2021-2022 ----------
# depression is a 0-10 score — convert to flag at >= 5
# anxiety is a 0-10 score — convert to flag at >= 5
# ther_cur is 0/1

clean_2021 = conn.execute("""
    SELECT
        responseid                              AS student_id,
        '2021-2022'                             AS academic_year,
        'Early Recovery'                        AS covid_period,
        age,
        yr_sch                                  AS year_of_study,

        CASE
            WHEN degree_bach = 1 THEN 'Undergraduate'
            WHEN degree_ma   = 1 THEN 'Graduate'
            WHEN degree_phd  = 1 THEN 'PhD'
            ELSE 'Other'
        END AS degree_level,

        CASE
            WHEN gender_male   = 1 THEN 'Man'
            WHEN gender_female = 1 THEN 'Woman'
            WHEN gender_nonbin = 1 THEN 'Non-binary'
            ELSE 'Other/Not reported'
        END AS gender,

        CASE WHEN depression >= 5 THEN 1
             WHEN depression <  5 THEN 0
             ELSE NULL END                      AS depression,

        CASE WHEN anxiety >= 5 THEN 1
             WHEN anxiety <  5 THEN 0
             ELSE NULL END                      AS anxiety,

        CASE WHEN aca_impa >= 2 THEN 1
             WHEN aca_impa =  1 THEN 0
             ELSE NULL END                      AS academic_impairment,

        CASE WHEN dep_impa >= 2 THEN 1
             WHEN dep_impa =  1 THEN 0
             ELSE NULL END                      AS depression_impairment,

        CASE WHEN gad7_impa >= 2 THEN 1
             WHEN gad7_impa =  1 THEN 0
             ELSE NULL END                      AS anxiety_impairment,

        sui_idea                                AS suicidal_ideation,
        sui_plan                                AS suicidal_plan,
        sui_att                                 AS suicide_attempt,
        sib_any                                 AS self_harm_any,

        CASE WHEN ther_ever >= 1 THEN 1
             ELSE NULL END                      AS therapy_ever,
        ther_cur                                AS therapy_current,
        meds_any                                AS medication_any,
        tx_any                                  AS treatment_any,
        dx_any                                  AS diagnosis_any,
        dx_dep                                  AS dx_depression,
        dx_anx                                  AS dx_anxiety,
        mh_prior                                AS mh_prior

    FROM raw_2021_2022
    WHERE responseid IS NOT NULL
""").fetchall()

print(f"Clean 2021-2022: {len(clean_2021)} rows")

# ---------- 2022-2023 ----------
# dep_any and anx_any are 0/1 flags
# ther_cur is 0/1
# mh_prior_clim replaces mh_prior

clean_2022 = conn.execute("""
    SELECT
        responseid                              AS student_id,
        '2022-2023'                             AS academic_year,
        'Post-COVID'                            AS covid_period,
        age,
        yr_sch                                  AS year_of_study,

        CASE
            WHEN degree_bach = 1 THEN 'Undergraduate'
            WHEN degree_ma   = 1 THEN 'Graduate'
            WHEN degree_phd  = 1 THEN 'PhD'
            ELSE 'Other'
        END AS degree_level,

        CASE
            WHEN gender_male   = 1 THEN 'Man'
            WHEN gender_female = 1 THEN 'Woman'
            WHEN gender_nonbin = 1 THEN 'Non-binary'
            ELSE 'Other/Not reported'
        END AS gender,

        dep_any                                 AS depression,
        anx_any                                 AS anxiety,

        CASE WHEN aca_impa >= 2 THEN 1
             WHEN aca_impa =  1 THEN 0
             ELSE NULL END                      AS academic_impairment,

        CASE WHEN dep_impa >= 2 THEN 1
             WHEN dep_impa =  1 THEN 0
             ELSE NULL END                      AS depression_impairment,

        CASE WHEN gad7_impa >= 2 THEN 1
             WHEN gad7_impa =  1 THEN 0
             ELSE NULL END                      AS anxiety_impairment,

        sui_idea                                AS suicidal_ideation,
        sui_plan                                AS suicidal_plan,
        sui_att                                 AS suicide_attempt,
        sib_any                                 AS self_harm_any,

        CASE WHEN ther_ever >= 1 THEN 1
             ELSE NULL END                      AS therapy_ever,
        ther_cur                                AS therapy_current,
        meds_any                                AS medication_any,
        tx_any                                  AS treatment_any,
        dx_any                                  AS diagnosis_any,
        dx_dep                                  AS dx_depression,
        dx_anx                                  AS dx_anxiety,
        mh_prior_clim                           AS mh_prior

    FROM raw_2022_2023
    WHERE responseid IS NOT NULL
""").fetchall()

print(f"Clean 2022-2023: {len(clean_2022)} rows")

# ============================================================
# STEP 3 — COMBINE ALL 4 YEARS INTO MASTER TABLE
# ============================================================

cols = [
    'student_id', 'academic_year', 'covid_period', 'age', 'year_of_study',
    'degree_level', 'gender',
    'depression', 'anxiety', 'academic_impairment',
    'depression_impairment', 'anxiety_impairment',
    'suicidal_ideation', 'suicidal_plan', 'suicide_attempt',
    'self_harm_any',
    'therapy_ever', 'therapy_current', 'medication_any', 'treatment_any',
    'diagnosis_any', 'dx_depression', 'dx_anxiety',
    'mh_prior'
]

master = pd.DataFrame(
    clean_2019 + clean_2020 + clean_2021 + clean_2022,
    columns=cols
)

master.to_sql('mental_health_master', conn, if_exists='replace', index=False)

print(f"\nMaster table: {len(master)} total rows")
print("\nNull counts:")
print(master.isnull().sum())

# ============================================================
# STEP 4 — ANALYSIS QUERIES
# ============================================================

print("\n\n=== Q1: Core trends across all 4 years (COVID arc) ===")
q1 = pd.read_sql("""
    SELECT
        academic_year,
        covid_period,
        COUNT(*)                                        AS total_students,
        ROUND(AVG(depression) * 100, 1)                AS depression_pct,
        ROUND(AVG(anxiety) * 100, 1)                   AS anxiety_pct,
        ROUND(AVG(academic_impairment) * 100, 1)       AS impairment_pct,
        ROUND(AVG(therapy_current) * 100, 1)           AS therapy_current_pct,
        ROUND(AVG(medication_any) * 100, 1)            AS medication_pct,
        ROUND(AVG(suicidal_ideation) * 100, 1)         AS suicidal_ideation_pct
    FROM mental_health_master
    GROUP BY academic_year, covid_period
    ORDER BY academic_year
""", conn)
print(q1.to_string())

print("\n\n=== Q2: The gap — therapy access vs academic impairment ===")
q2 = pd.read_sql("""
    SELECT
        academic_year,
        covid_period,
        ROUND(AVG(therapy_current) * 100, 1)           AS in_therapy_pct,
        ROUND(AVG(academic_impairment) * 100, 1)       AS still_impaired_pct,
        ROUND((AVG(academic_impairment) -
               AVG(therapy_current)) * 100, 1)         AS gap
    FROM mental_health_master
    GROUP BY academic_year, covid_period
    ORDER BY academic_year
""", conn)
print(q2.to_string())

print("\n\n=== Q3: Does treatment reduce impairment? ===")
q3 = pd.read_sql("""
    SELECT
        therapy_current,
        medication_any,
        COUNT(*)                                        AS students,
        ROUND(AVG(academic_impairment) * 100, 1)       AS impairment_pct,
        ROUND(AVG(depression) * 100, 1)                AS depression_pct
    FROM mental_health_master
    WHERE therapy_current IS NOT NULL
      AND medication_any  IS NOT NULL
    GROUP BY therapy_current, medication_any
    ORDER BY therapy_current, medication_any
""", conn)
print(q3.to_string())

print("\n\n=== Q4: Who is most at risk — degree level ===")
q4 = pd.read_sql("""
    SELECT
        degree_level,
        COUNT(*)                                        AS students,
        ROUND(AVG(depression) * 100, 1)                AS depression_pct,
        ROUND(AVG(anxiety) * 100, 1)                   AS anxiety_pct,
        ROUND(AVG(academic_impairment) * 100, 1)       AS impairment_pct,
        ROUND(AVG(suicidal_ideation) * 100, 1)         AS suicidal_ideation_pct
    FROM mental_health_master
    WHERE degree_level IS NOT NULL
    GROUP BY degree_level
    ORDER BY depression_pct DESC
""", conn)
print(q4.to_string())

print("\n\n=== Q5: Gender breakdown ===")
q5 = pd.read_sql("""
    SELECT
        gender,
        COUNT(*)                                        AS students,
        ROUND(AVG(depression) * 100, 1)                AS depression_pct,
        ROUND(AVG(anxiety) * 100, 1)                   AS anxiety_pct,
        ROUND(AVG(academic_impairment) * 100, 1)       AS impairment_pct,
        ROUND(AVG(therapy_current) * 100, 1)           AS in_therapy_pct
    FROM mental_health_master
    WHERE gender IS NOT NULL
    GROUP BY gender
    ORDER BY depression_pct DESC
""", conn)
print(q5.to_string())

print("\n\n=== Q6: COVID period — did impairment peak during or after? ===")
q6 = pd.read_sql("""
    SELECT
        covid_period,
        ROUND(AVG(depression) * 100, 1)                AS depression_pct,
        ROUND(AVG(anxiety) * 100, 1)                   AS anxiety_pct,
        ROUND(AVG(academic_impairment) * 100, 1)       AS impairment_pct,
        ROUND(AVG(therapy_current) * 100, 1)           AS therapy_pct,
        ROUND(AVG(suicidal_ideation) * 100, 1)         AS suicidal_ideation_pct,
        COUNT(*)                                        AS students
    FROM mental_health_master
    GROUP BY covid_period
    ORDER BY
        CASE covid_period
            WHEN 'Pre-COVID'     THEN 1
            WHEN 'During COVID'  THEN 2
            WHEN 'Early Recovery' THEN 3
            WHEN 'Post-COVID'    THEN 4
        END
""", conn)
print(q6.to_string())

# ============================================================
# STEP 5 — EXPORT FOR TABLEAU
# ============================================================

os.makedirs('exports', exist_ok=True)

exports = {
    'trends': q1,
    'therapy_vs_impairment': q2,
    'treatment_impact': q3,
    'risk_by_degree': q4,
    'risk_by_gender': q5,
    'covid_arc': q6,
}

for name, df in exports.items():
    df.to_csv(f'exports/{name}.csv', index=False)
    print(f"Saved {name}.csv")

print("\nDone.")
conn.close()