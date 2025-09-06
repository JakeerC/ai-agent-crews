from crewai.tools import BaseTool


class ReplaceJargonsTool(BaseTool):
    name: str = "Jargon replacement tool"
    description: str = "Replaces jargon with more specific terms. "

    def _run(self, email: str) -> str:
        replacements = {
            "PRX": "Project Phoenix (internal AI revamp project)",
            "TAS": "technical architecture stack",
            "DBX": "client database cluster",
            "SDS": "Smart Data Syncer",
            "SYNCBOT": "internal standup assistant bot",
            "WIP": "in progress",
            "POC": "proof of concept",
            "ping": "reach out",
        }

        suggestions = []
        email_lower = email.lower()
        for jargon, replacement in replacements.items():
            if jargon.lower() in email_lower:
                suggestions.append(
                    f"Consider replacing '{jargon}' with '{replacement}'"
                )

        return (
            "\n".join(suggestions)
            if suggestions
            else "No jargon or internal abbreviations detected."
        )
