
# === FILE: tools/resume_critic.py ===
def analyze_resume(text):
    if "intern" in text.lower():
        return "Looks like you’re aiming for internships. Consider adding measurable achievements."
    return "Make sure your resume has clear section headings, skills, and results-oriented bullets." 