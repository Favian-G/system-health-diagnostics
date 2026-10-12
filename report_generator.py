from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
import webbrowser

def create_html_report(system_data, output_file='system_report.html'):
    try:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('report_template.html')
        
        render_data = {
            'Timestamp': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'System': system_data['System'],
            'CPU': system_data['CPU'],
            'Memory': system_data['Memory'],
            'Disk': system_data['Disk'],
            'Network': system_data['Network'],  # This now contains your Internet status and adapters
            'Processes': system_data['Processes'][:10]
        }
        
        html_content = template.render(render_data)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated: {output_file}")
        file_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{file_path}')
        return output_file
        
    except Exception as e:
        print(f"Error while creating report: {e}")
        return None
