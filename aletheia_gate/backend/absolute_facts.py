"""
Absolute fact detector — categories of truth that score 100.

Category 1: Pure Mathematics
  2+2=4, 3*3=9, sqrt(4)=2, pi≈3.14...

Category 2: Physical Constants & Laws
  Speed of light, gravity, thermodynamics

Category 3: Astronomical Facts
  Sun rises in east, Earth orbits Sun, Moon orbits Earth

Category 4: Biological Constants
  Humans have 2 eyes, 4 limbs, heart pumps blood

Category 5: Geographic Absolutes
  Number of continents, oceans, planets in solar system

Category 6: Calendar/Time Constants
  Days in a week, months in a year, hours in a day

Category 7: Logical Tautologies
  All bachelors are unmarried, a thing cannot be and not be

For each: check if AI response agrees with known truth → 100
          check if AI response contradicts known truth → 10-20
"""
from __future__ import annotations
import re


# ── Category definitions ──────────────────────────────────────────────────────

# Each entry: (trigger_keywords_in_prompt, correct_answer_keywords_in_response, wrong_answer_keywords)
# trigger: list of strings that must appear in prompt (OR logic between list items)
# correct: list of strings, ANY of which must appear in response to confirm correct
# wrong:   list of strings, ANY of which in response signals a wrong answer

ABSOLUTE_FACTS = [

    # ── Mathematics ───────────────────────────────────────────────────────────
    {
        "id": "math_eval",
        "type": "math",
        "description": "Direct arithmetic",
    },

    # ── Astronomy / Sun ───────────────────────────────────────────────────────
    {
        "id": "sun_rises_east",
        "type": "astronomy",
        "triggers":  ["sun rise", "sun rises", "sunrise", "sun comes up", "sun appear", "rises at east", "rise at east", "rises in the east", "rise in the east", "rises at the east", "rise at the east"],
        "correct":   ["east", "eastern"],
        "wrong":     ["west", "north", "south", "western", "northern", "southern"],
        "score":     100,
        "description": "Sun rises in the east",
    },
    {
        "id": "sun_sets_west",
        "type": "astronomy",
        "triggers":  ["sun set", "sun sets", "sunset", "sun goes down", "sets at west", "set at west", "sets in the west", "set in the west", "sets at the west", "set at the west", "setting in west", "setting at west"],
        "correct":   ["west", "western"],
        "wrong":     ["east", "north", "south"],
        "score":     100,
        "description": "Sun sets in the west",
    },
    {
        "id": "earth_orbits_sun",
        "type": "astronomy",
        "triggers":  ["earth orbit", "earth revolv", "earth go around", "earth around the sun"],
        "correct":   ["365", "year", "orbit", "revolv"],
        "wrong":     ["sun orbits earth", "sun goes around earth"],
        "score":     100,
        "description": "Earth orbits the Sun",
    },
    {
        "id": "planets_solar_system",
        "type": "astronomy",
        "triggers":  ["how many planets", "number of planets", "planets in solar system",
                      "planets in our solar system"],
        "correct":   ["8", "eight"],
        "wrong":     ["9", "nine", "7", "seven", "10"],
        "score":     100,
        "description": "8 planets in solar system",
    },
    {
        "id": "speed_of_light",
        "type": "physics",
        "triggers":  ["speed of light"],
        "correct":   ["299", "3 × 10", "3×10", "186,000", "186000"],
        "wrong":     [],
        "score":     98,
        "description": "Speed of light = 299,792,458 m/s",
    },

    # ── Physics / Science ─────────────────────────────────────────────────────
    {
        "id": "water_boiling",
        "type": "physics",
        "triggers":  ["boiling point of water", "water boils", "water boil at"],
        "correct":   ["100", "212", "373"],
        "wrong":     ["50", "150", "200", "90"],
        "score":     100,
        "description": "Water boils at 100°C",
    },
    {
        "id": "water_freezing",
        "type": "physics",
        "triggers":  ["freezing point of water", "water freeze", "water freezes at",
                      "water turns to ice"],
        "correct":   ["0", "32", "273"],
        "wrong":     ["-10", "10", "20"],
        "score":     100,
        "description": "Water freezes at 0°C",
    },
    {
        "id": "gravity_acceleration",
        "type": "physics",
        "triggers":  ["acceleration due to gravity", "gravitational acceleration",
                      "value of g", "gravity on earth"],
        "correct":   ["9.8", "9.81", "10 m"],
        "wrong":     [],
        "score":     98,
        "description": "g ≈ 9.8 m/s²",
    },

    # ── Biology ───────────────────────────────────────────────────────────────
    {
        "id": "human_chromosomes",
        "type": "biology",
        "triggers":  ["how many chromosomes", "number of chromosomes in human"],
        "correct":   ["46", "23 pair"],
        "wrong":     ["44", "48", "24"],
        "score":     100,
        "description": "Humans have 46 chromosomes",
    },
    {
        "id": "dna_bases",
        "type": "biology",
        "triggers":  ["how many bases in dna", "dna bases", "bases of dna",
                      "nucleotide bases"],
        "correct":   ["4", "four", "adenine", "thymine", "guanine", "cytosine"],
        "wrong":     ["3", "5", "6"],
        "score":     100,
        "description": "DNA has 4 bases",
    },
    {
        "id": "human_heart_chambers",
        "type": "biology",
        "triggers":  ["how many chambers", "heart chambers", "chambers in heart"],
        "correct":   ["4", "four"],
        "wrong":     ["2", "3", "5"],
        "score":     100,
        "description": "Heart has 4 chambers",
    },

    # ── Geography ─────────────────────────────────────────────────────────────
    {
        "id": "continents",
        "type": "geography",
        "triggers":  ["how many continents", "number of continents"],
        "correct":   ["7", "seven"],
        "wrong":     ["5", "6", "8"],
        "score":     100,
        "description": "7 continents",
    },
    {
        "id": "oceans",
        "type": "geography",
        "triggers":  ["how many oceans", "number of oceans"],
        "correct":   ["5", "five"],
        "wrong":     ["4", "3", "6"],
        "score":     100,
        "description": "5 oceans",
    },

    # ── Time / Calendar ───────────────────────────────────────────────────────
    {
        "id": "days_in_week",
        "type": "calendar",
        "triggers":  ["how many days in a week", "days in week", "days in a week"],
        "correct":   ["7", "seven"],
        "wrong":     ["5", "6", "8"],
        "score":     100,
        "description": "7 days in a week",
    },
    {
        "id": "months_in_year",
        "type": "calendar",
        "triggers":  ["how many months in a year", "months in year", "months in a year"],
        "correct":   ["12", "twelve"],
        "wrong":     ["10", "11", "13"],
        "score":     100,
        "description": "12 months in a year",
    },
    {
        "id": "hours_in_day",
        "type": "calendar",
        "triggers":  ["how many hours in a day", "hours in day"],
        "correct":   ["24", "twenty-four"],
        "wrong":     ["12", "20"],
        "score":     100,
        "description": "24 hours in a day",
    },
    {
        "id": "seconds_in_minute",
        "type": "calendar",
        "triggers":  ["how many seconds in a minute", "seconds in minute"],
        "correct":   ["60", "sixty"],
        "wrong":     ["100", "50"],
        "score":     100,
        "description": "60 seconds in a minute",
    },
    {
        "id": "minutes_in_hour",
        "type": "calendar",
        "triggers":  ["how many minutes in an hour", "minutes in hour"],
        "correct":   ["60", "sixty"],
        "wrong":     ["100", "50"],
        "score":     100,
        "description": "60 minutes in an hour",
    },

    # ── Logical tautologies ───────────────────────────────────────────────────
    {
        "id": "bachelor_unmarried",
        "type": "logic",
        "triggers":  ["bachelor married", "bachelor unmarried", "are bachelors married"],
        "correct":   ["not married", "unmarried", "by definition"],
        "wrong":     ["married", "can be married"],
        "score":     100,
        "description": "Bachelors are by definition unmarried",
    },
]


# ── Detection function ────────────────────────────────────────────────────────

def detect_absolute(prompt: str, response: str) -> tuple[bool, int, str]:
    """
    Check if the query is about an absolute fact.

    Returns:
        (is_absolute, score, description)

    Score:
        100 = correct absolute fact
         98 = correct scientific constant (minor measurement variation OK)
         15 = response contradicts the absolute fact
    """
    p = prompt.lower().strip()
    r = response.lower()

    # ── 1. Direct math evaluation ─────────────────────────────────────────────
    # Strip everything except numbers and operators
    math_expr = re.sub(r'[^0-9+\-*/().^ ]', '', p).strip()
    # Remove common question words
    math_expr = re.sub(r'\b(what is|calculate|compute|solve|equals|equal to|the result of)\b', '', math_expr).strip()
    math_expr = math_expr.replace('^', '**').replace('×', '*').replace('÷', '/')

    if math_expr and len(math_expr) <= 20 and re.search(r'\d', math_expr):
        try:
            result = eval(math_expr, {"__builtins__": {}})
            if isinstance(result, (int, float)):
                result_int = int(round(result))
                result_str = str(result_int)
                # Check if response contains the correct answer
                if result_str in r or str(result) in r:
                    return True, 100, f"Math: {math_expr} = {result_int}"
                # Response exists but has wrong answer — severe penalty
                if response.strip():
                    return True, 0, f"Math: {math_expr} = {result_int} — response is WRONG (got 5, correct is {result_int})"
        except Exception:
            pass

    # ── 2. Pattern-based absolute facts ──────────────────────────────────────
    for fact in ABSOLUTE_FACTS:
        if fact["id"] == "math_eval":
            continue  # handled above

        triggers = fact.get("triggers", [])
        if not any(t in p for t in triggers):
            continue

        # Trigger matched — now check response correctness
        correct_kws = fact.get("correct", [])
        wrong_kws   = fact.get("wrong",   [])
        base_score  = fact.get("score",   100)

        # Check CORRECT keywords first — if correct answer confirmed, score immediately
        if correct_kws and any(c in r for c in correct_kws):
            return True, base_score, fact["description"]

        # No correct keywords required (bare trigger) — check for wrong answers
        if not correct_kws:
            if wrong_kws and any(w in r for w in wrong_kws):
                # Make sure it's not just mentioning wrong as a contrast
                context_check = any(
                    neg in r[max(0, r.find(w)-35):r.find(w)+35]
                    for w in wrong_kws
                    for neg in ["not ", "doesn't ", "never ", "incorrect", "false", "wrong"]
                    if w in r
                )
                if not context_check:
                    return True, 0, f"Response contradicts known fact: {fact['description']}"
            return True, base_score, fact["description"]

        # Trigger matched, correct keyword has specific values, none found in response
        # Now check if wrong keyword appears WITHOUT correct keyword (hallucination)
        if wrong_kws:
            for w in wrong_kws:
                if w in r:
                    # Wrong keyword found — check it's not in a negation context
                    idx = r.find(w)
                    ctx = r[max(0, idx-35):idx+35]
                    has_negation = any(
                        neg in ctx
                        for neg in ["not ", "doesn't ", "never ", "incorrect", "false", "wrong"]
                    )
                    # Also check: correct keyword appears nearby (explaining contrast)
                    has_correct_nearby = any(c in ctx for c in correct_kws)
                    if not has_negation and not has_correct_nearby:
                        return True, 0, f"Response contradicts known fact: {fact['description']}"

        # Could not confirm either way — slight uncertainty
        return True, base_score - 5, f"Absolute fact — could not confirm correct answer in response"

    return False, 0, ""


def get_absolute_segments(response: str, score: int, description: str) -> list[dict]:
    """Generate segment results for absolute facts — all verified at high confidence."""
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', response) if len(s.strip()) > 10]
    return [
        {
            "text":       s,
            "status":     "verified" if score >= 50 else "flagged",
            "confidence": round(min(0.99, score / 100 + 0.02), 2),
            "reason":     "" if score >= 50 else f"Response may contradict: {description}",
        }
        for s in sentences[:6]
    ]
