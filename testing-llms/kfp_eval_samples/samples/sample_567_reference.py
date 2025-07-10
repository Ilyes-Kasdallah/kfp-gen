# Copyright 2020 kubeflow.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp import dsl
from kfp import components

def deploy_ray_cluster():
    print("lauching a Ray cluster when this KFP operator is deployed")
    from test import launch_ray
    launch_ray()


deploy_ray_cluster_op = components.create_component_from_func(
    deploy_ray_cluster,
    base_image='us.icr.io/cil15-shared-registry/preprocessing-pipelines/kfp/kfp-codeflare:0')

@dsl.pipeline(
    name='test_KFP_deploy_ray_cluster',
    description='Testing how to use KFP pipeline to deploy a Ray cluster.'
)
def kfp_ray_deployment_pipeline():
    deploy_ray_cluster_op()


if __name__ == '__main__':
    from kfp_tekton.compiler import TektonCompiler
    TektonCompiler().compile(kfp_ray_deployment_pipeline, __file__.replace('.py', '.yaml'))
