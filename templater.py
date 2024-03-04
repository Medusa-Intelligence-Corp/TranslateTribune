from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

def deploy_website(article_html):
    template_dir = '/usr/src/app'

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Load your index.html template
    template = env.get_template('template.html')

    # Render the template with your HTML list
    rendered_html = template.render(article_html=article_html)

    # Optionally, write the rendered HTML to a new file
    output_path = os.path.join(template_dir, 'index.html')
    with open(output_path, 'w') as file:
        file.write(rendered_html)

    return rendered_html
