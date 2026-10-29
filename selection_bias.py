
import sqlite3
from contextlib import redirect_stdout

conn = sqlite3.connect("agent_skills_sample.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        location_class,
        COUNT(*) AS total,
        SUM(CASE WHEN history_fetched = 1 THEN 1 ELSE 0 END)
            AS histories,
        ROUND(
            100.0 * SUM(
                CASE WHEN history_fetched = 1 THEN 1 ELSE 0 END
            ) / COUNT(*),
            2
        ) AS percentage
    FROM artifacts
    GROUP BY location_class
    ORDER BY total DESC
""")

print("HISTORY COVERAGE BY SKILL LOCATION")
print("-" * 65)
print(f"{'Location':<20} {'Total':>10} {'Histories':>12} {'Coverage':>12}")

for location, total, histories, percentage in cursor.fetchall():
    print(
        f"{str(location):<20} "
        f"{total:>10,} "
        f"{histories:>12,} "
        f"{percentage:>11.2f}%"
    )

cursor.execute("""
    SELECT
        history_fetched,
        COUNT(*) AS total,
        ROUND(AVG(body_chars), 1) AS avg_length,
        ROUND(100.0 * AVG(has_scripts), 2) AS scripts_pct,
        ROUND(100.0 * AVG(has_references), 2) AS references_pct
    FROM artifacts
    GROUP BY history_fetched
    ORDER BY history_fetched DESC
""")

print("\nSKILL CHARACTERISTICS BY HISTORY AVAILABILITY")
print("-" * 65)

for history, total, length, scripts, references in cursor.fetchall():
    label = "History available" if history == 1 else "No history"
    print(f"\n{label}:")
    print(f"  Records: {total:,}")
    print(f"  Average document length: {length} characters")
    print(f"  Contains scripts: {scripts}%")
    print(f"  Contains references: {references}%")

conn.close()
