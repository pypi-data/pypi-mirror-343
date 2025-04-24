# doc_quality/suggestions.py
def suggest_improvements(metrics):
    suggestions = []

    # Conciseness
    if metrics['M1_Words'] > 600:
        suggestions.append("Too verbose. Consider removing redundant descriptions.")
    if metrics['M2_SentenceLength'] > 20:
        suggestions.append("Shorten sentence length for better conciseness.")

    # Readability
    if metrics['M3_FleschScore'] < 50:
        suggestions.append("Simplify wording to improve readability.")
    if metrics['M4_ReadingTime'] > 5:
        suggestions.append("Aim for a shorter reading time by being more concise.")
    if metrics['M5_DifficultWords'] > 40:
        suggestions.append("Replace or explain difficult words.")

    # Consistency
    if metrics['M6_NamedEntities'] < 3:
        suggestions.append("Add more contextual entities like class names or API names.")
    if metrics['M7_Patterns'] < 3:
        suggestions.append("Include relevant patterns or identifiers for clarity.")

    # Structuredness
    if metrics['M8_HeadingMatchRatio'] < 0.3:
        suggestions.append("Use standard headings like Installation, Usage, etc.")
    if metrics['M9_LogicalFlow'] < 0.5:
        suggestions.append("Improve logical progression of ideas.")
    if metrics['M10_ListCount'] < 2:
        suggestions.append("Add more bullet points or numbered lists for readability.")

    # Traceability
    if metrics['M11_RefDensity'] < 1:
        suggestions.append("Include links to issues, commits, or PRs.")
    if metrics['M12_IdentifierConsistency'] < 0.1:
        suggestions.append("Ensure consistent use of technical identifiers.")

    # Cohesion
    if metrics['M13_LexicalCohesion'] < 0.4:
        suggestions.append("Unify terminology and use more related words.")
    if metrics['M14_DiscourseMarkers'] < 2:
        suggestions.append("Add discourse markers like 'however', 'therefore' to improve flow.")

    return suggestions
