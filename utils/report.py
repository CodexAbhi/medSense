def format_report_for_streamlit(report_text):
    """Format the report text for display in Streamlit."""
    # The report is already in markdown format, so we just return it
    return report_text

def save_report_to_file(report_text, filename):
    """Save the report to a text file."""
    with open(filename, 'w') as f:
        f.write(report_text)
    return filename