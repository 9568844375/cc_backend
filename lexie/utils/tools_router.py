# === FILE: utils/tools_router.py ===
from tools.resume_critic import analyze_resume
from tools.proposal_writer import help_with_proposal
from tools.event_bot import upcoming_events

async def route_query_to_tool(query, user_id, role):
    if "upload" in query or "document" in query:
        return "Please upload the file and I’ll answer your questions from it."
    if "resume" in query:
        return analyze_resume(query)
    if "proposal" in query:
        return help_with_proposal()
    if "event" in query:
        return upcoming_events()
    if "report" in query and role == "admin":
        return "Generating your admin report..."
    return None