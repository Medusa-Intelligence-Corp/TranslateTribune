import os
import uuid
import datetime
import pytz

import boto3

from jinja2 import Environment, FileSystemLoader, select_autoescape


def deploy_website(article_html, template_filename, html_filename, **kwargs):

    locals().update(**kwargs)           

    template_dir = '/usr/src/app/static/'

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_filename)

    current_utc_datetime = datetime.datetime.utcnow()
    current_utc_datetime = current_utc_datetime.replace(tzinfo=pytz.utc)
    eastern_time = current_utc_datetime.astimezone(pytz.timezone(publishing_timezone))
    date_string = eastern_time.strftime("%Y-%m-%d %H:%M %Z")

    rendered_html = template.render(article_html=article_html,date_string=date_string)

    output_path = os.path.join('/usr/src/app/debug', html_filename)
    with open(output_path, 'w') as file:
        file.write(rendered_html)

    debug = os.environ.get('DEBUG', False)
    if debug:
        return rendered_html
    else:

        bucket_name = 'translatetribune.com'
        s3_key=html_filename
        s3_client = boto3.client('s3')
        extra_args = {'ContentType': 'text/html'}
        s3_client.upload_file(output_path, bucket_name, s3_key, ExtraArgs=extra_args)

        distribution_id = 'E12FININDDZ0ME'

        paths = [f'/{html_filename}']

        client = boto3.client('cloudfront')

        response = client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': str(uuid.uuid4()) 
            }
        )

        return rendered_html

def deploy_games(template_filename="template.html", html_filename="games.html"):
    with open("/usr/src/app/static/games.html", "r") as file:
        # Read the lines of the file
        html_lines = file.read()
    deploy_website(html_lines, template_filename, html_filename)
