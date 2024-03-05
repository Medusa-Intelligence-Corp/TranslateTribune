import os
import uuid

import boto3

from jinja2 import Environment, FileSystemLoader, select_autoescape


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
    
    # deploy to s3
    bucket_name = 'translatetribune.com'
    s3_key='index.html'
    s3_client = boto3.client('s3')
    s3_client.upload_file(output_path, bucket_name, s3_key)

    #invalidate cloudfront cache
    distribution_id = 'E12FININDDZ0ME'

    # The path of the object to invalidate, e.g., '/index.html'
    # To invalidate the entire cache, you can use '/*'
    paths = ['/index.html']

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
