import os
import uuid
import datetime
import pytz

import boto3

from bs4 import BeautifulSoup

from jinja2 import Environment, FileSystemLoader, select_autoescape


def upload_and_invalidate(file_path, file_name, content_type):
    bucket_name = 'translatetribune.com'
    s3_key = file_name
    s3_client = boto3.client('s3')

    extra_args = {
        'ContentType': content_type,
    }
    s3_client.upload_file(file_path, bucket_name, s3_key, ExtraArgs=extra_args)

    distribution_id = 'E12FININDDZ0ME'
    paths = [f'/{file_name}']
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


def deploy_website(article_html, html_filename, article_rss, rss_filename, lang_config, section_key):

    template_dir = '/usr/src/app/static/'

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )


    current_utc_datetime = datetime.datetime.utcnow()
    current_utc_datetime = current_utc_datetime.replace(tzinfo=pytz.utc)
    eastern_time = current_utc_datetime.astimezone(pytz.timezone(lang_config["publishing_timezone"]))
    date_string = eastern_time.strftime("%Y-%m-%d • %H:%M %Z")

    template = env.get_template('template.html')
    rendered_html = template.render(**locals())
    rendered_html = BeautifulSoup(rendered_html, 'html.parser').prettify()

    output_path_html = os.path.join('/usr/src/app/debug', html_filename)
    with open(output_path_html, 'w') as file:
        file.write(rendered_html)
    
    rss_template = env.get_template('template.xml')
    rendered_rss = rss_template.render(**locals())
    rendered_rss = BeautifulSoup(rendered_rss, 'xml').prettify()

    output_path_rss = os.path.join('/usr/src/app/debug', rss_filename)
    with open(output_path_rss, 'w') as file:
        file.write(rendered_rss)

    debug = os.environ.get('DEBUG', False)
    if not debug:
        upload_and_invalidate(output_path_html, html_filename, 'text/html')
        upload_and_invalidate(output_path_rss, rss_filename, 'application/rss+xml')

    return rendered_html
