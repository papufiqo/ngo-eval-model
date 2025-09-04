import weasyprint
from jinja2 import Template
import json

def generate_html_report(scores, audit, themes, data_path="data/sample_input.json"):
    with open(data_path) as f:
        data = json.load(f)

    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>W NGO Evaluation Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #fff; color: #000; }
            .section { margin: 30px 0; }
            h1, h2 { color: #005a9c; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
            .compliant { color: green; }
            .non-compliant { color: red; }
        </style>
    </head>
    <body>
        <h1>External Evaluation Report for (W)</h1>
        <p><strong>Date:</strong> {{ date }}</p>

        <div class="section">
            <h2>Performance Scores</h2>
            <table>
                <tr><th>Index</th><th>Score (/100)</th></tr>
                <tr><td>Goal Achievement Index (GAI)</td><td>{{ scores.GAI }}</td></tr>
                <tr><td>Work Capacity Index (WCI)</td><td>{{ scores.WCI }}</td></tr>
                <tr><td>Added Value Index (AVI)</td><td>{{ scores.AVI }}</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>Inclusiveness Audit</h2>
            <p>Status: <span class="{{ 'compliant' if audit.compliant else 'non-compliant' }}">
                {{ 'Compliant' if audit.compliant else 'Non-Compliant' }}</span></p>
            {% if audit.missing %}
            <p>Missing: {{ audit.missing|join(', ') }}</p>
            {% endif %}
        </div>

        <div class="section">
            <h2>Key Improvement Themes</h2>
            <ul>
            {% for theme, count in themes %}
                <li>{{ theme.capitalize() }} (mentioned {{ count }} times)</li>
            {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>Recommendations</h2>
            <ul>
                {% if 'accessible' in [t[0] for t in themes] %}
                <li>Improve accessibility of all communications and documents.</li>
                {% endif %}
                {% if 'youth' in [t[0] for t in themes] or 'involvement' in [t[0] for t in themes] %}
                <li>Strengthen Youth Network integration into governance.</li>
                {% endif %}
                {% if 'training' in [t[0] for t in themes] %}
                <li>Expand capacity-building programs for members.</li>
                {% endif %}
            </ul>
        </div>
    </body>
    </html>
    """

    template = Template(template_str)
    html_out = template.render(scores=scores, audit=audit, themes=themes, date="2025-11-28")

    with open("output/report.html", "w") as f:
        f.write(html_out)

    # Generate PDF
    weasyprint.HTML(string=html_out).write_pdf("output/report.pdf")
    print("✅ Reports generated: output/report.html and output/report.pdf")
