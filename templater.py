import os
import uuid
import datetime
import pytz

import boto3

from jinja2 import Environment, FileSystemLoader, select_autoescape


def deploy_website(article_html, template_filename, html_filename):
    template_dir = '/usr/src/app'

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_filename)

    current_utc_datetime = datetime.datetime.utcnow()
    current_utc_datetime = current_utc_datetime.replace(tzinfo=pytz.utc)
    eastern_time = current_utc_datetime.astimezone(pytz.timezone('US/Eastern'))
    date_string = eastern_time.strftime("%A, %d %b %Y at %I:%M %p %Z")

    # Render the template with your HTML list
    rendered_html = template.render(article_html=article_html,date_string=date_string)

    # Optionally, write the rendered HTML to a new file
    output_path = os.path.join(template_dir, html_filename)
    with open(output_path, 'w') as file:
        file.write(rendered_html)
    
    # deploy to s3
    bucket_name = 'translatetribune.com'
    s3_key=html_filename
    s3_client = boto3.client('s3')
    extra_args = {'ContentType': 'text/html'}
    s3_client.upload_file(output_path, bucket_name, s3_key, ExtraArgs=extra_args)

    #invalidate cloudfront cache
    distribution_id = 'E12FININDDZ0ME'

    # The path of the object to invalidate, e.g., '/index.html'
    # To invalidate the entire cache, you can use '/*'
    paths = [f'/{html_filename}']

    client = boto3.client('cloudfront')

    # Create an invalidation
    response = client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': len(paths),
                'Items': paths
            },
            'CallerReference': str(uuid.uuid4())  # Unique value for each invalidation request
        }
    )

    return rendered_html
