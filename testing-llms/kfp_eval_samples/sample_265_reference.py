#!/usr/bin/env python
# coding: utf-8

# In[3]:


import kfp
# Load the component by calling load_component_from_file or load_component_from_url
# To load the component, the pipeline author only needs to have access to the component.yaml file.
# The Kubernetes cluster executing the pipeline needs access to the container image specified in the component.
model_generation_op = kfp.components.load_component_from_file('component1.yaml') 
prediction_op = kfp.components.load_component_from_file('component2.yaml')
# dummy_op = kfp.components.load_component_from_url('http://....../component.yaml')

# dummy_op is now a "factory function" that accepts the arguments for the component's inputs
# and produces a task object (e.g. ContainerOp instance).
# Inspect the dummy_op function in Jupyter Notebook by typing "dummy_op(" and pressing Shift+Tab
# You can also get help by writing help(dummy_op) or dummy_op? or dummy_op??
# The signature of the dummy_op function corresponds to the inputs section of the component.
# Some tweaks are performed to make the signature valid and pythonic:
# 1) All inputs with default values will come after the inputs without default values
# 2) The input names are converted to pythonic names (spaces and symbols replaced
#    with underscores and letters lowercased).

# Define a pipeline and create a task from a component:
@kfp.dsl.pipeline(name='tensorflow image classification', description='demo pipeline')
def model_generation_new1():
    model_generation = model_generation_op( )
    prdediction_part = prediction_op( ).after(model_generation)
    # To access GCS, you must configure the container to have access to a
    # GCS secret that grants required access to the bucket.
    # The outputs of the dummy1_task can be referenced using the
    # dummy1_task.outputs dictionary.
    # ! The output names are converted to lowercased dashed names.

    # Pass the outputs of the dummy1_task to some other component
 
    # To access GCS, you must configure the container to have access to a
    # GCS secret that grants required access to the bucket.


# In[4]:


import kfp
from kfp import compiler
import kfp.compiler as compiler
import kfp.components as comp
import kfp.dsl as dsl
from kfp import gcp
pipeline_func = model_generation_new1
pipeline_filename = pipeline_func.__name__ + '.pipeline.zip'

compiler.Compiler().compile(model_generation_new1, 
                            pipeline_filename)







