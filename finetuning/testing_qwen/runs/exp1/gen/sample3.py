import sys
sys.path.append('/home/runner/work/kfp-tekton/kfp-tekton/components/legacy_exit_handler')

from kfp import dsl

@dsl.component(base_image='python:3.7')
def download_and_print():
    import os
    import sys
    import urllib.request

    # Download a file
    url = 'https://raw.githubusercontent.com/kubeflow/pipelines/master/samples/core/get_started/hello_world.py'
    urllib.request.urlretrieve(url, '/tmp/hello_world.py')

    # Print the downloaded file's content
    with open('/tmp/hello_world.py', 'r') as f:
        print(f.read())

@dsl.pipeline(
    name='download and print',
    description='A sample pipeline to demonstrate download and print functionality.'
)
def download_and_print_pipeline():
    download_and_print_op = download_and_print()