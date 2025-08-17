from kfp import dsl
from kfp.v2.dsl import Artifact, Dataset, Input, Model, Output, ParallelFor, component

@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def split_ids(model_ids: str) -> list[str]:
    return model_ids.split(",")


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def create_file(content: str, file: Output[Artifact]):
    with open(file.path, "w") as f:
        f.write(content)


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def read_files(files: List[Artifact]) -> str:
    print("Reading files...")
    for file in files:
        with open(file.path, "r") as f:
            print(f"File content: {f.read()}")
    return "files read"


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def read_single_file(file: Input[Artifact]) -> str:
    with open(file.path, "r") as f:
        print(f"File content: {f.read()}")
    return file.uri


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def split_chars(model_chars: str) -> list[str]:
    return model_chars.split(",")


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def create_dataset(content: str, data: Output[Dataset]):
    with open(data.path, "w") as f:
        f.write(content)


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def read_datasets(data: List[Dataset]) -> str:
    print("Reading datasets...")
    for dataset in data:
        with open(dataset.path, "r") as f:
            print(f"Dataset content: {f.read()}")
    return "datasets read"


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def read_single_dataset_generate_model(
    data: Input[Dataset], id: str, results: Output[Model]
):
    with open(data.path, "r") as f:
        content = f.read()
    with open(results.path, "w") as f:
        f.write(content + id)
    results.metadata["model"] = "generated"
    results.metadata["model_name"] = "generated_model"


@component(
    base_image="python:3.10",
    packages_to_install=["pandas==2.0.2"],
)
def single_node_dag(char: str) -> Dataset:
    create_dataset_op = create_dataset(content=char, data=Output[Dataset]())
    create_dataset_op.set_caching_options(False)
    return create_dataset_op.outputs["data"]


@dsl.pipeline(name="collecting-artifacts")
def collecting_artifacts(model_ids: str = "", model_chars: str = ""):
    ids_split_op = split_ids(model_ids=model_ids)

    create_files_task = ParallelFor(ids_split_op.output, name="create_files_task")
    create_files_task.execution_options.caching_strategy.max_cache_staleness = "P0D"
    create_files_task.after(ids_split_op)

    read_files_op = read_files(
        files=dsl.Collected(create_files_task.outputs["my_file_"])
    )
    read_files_op.execution_options.caching_strategy.max_cache_staleness = "P0D"

    nested_loop_task = ParallelFor(ids_split_op.output, name="nested_loop_task")
    nested_loop_task.execution_options.caching_strategy.max_cache_staleness = "P0D"
    nested_loop_task.after(ids_split_op)

    inner_create_file_op = create_file(content=dsl.InputValuePlaceholder(), name="inner_create_file_op")
    inner_create_file_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    inner_create_file_op.after(nested_loop_task)

    inner_read_file_op = read_single_file(file=dsl.OutputValuePlaceholder(), name="inner_read_file_op")
    inner_read_file_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    inner_read_file_op.after(inner_create_file_op)

    chars_split_op = split_chars(model_chars=model_chars)
    chars_split_op.execution_options.caching_strategy.max_cache_staleness = "P0D"

    nested_dataset_loop_task = ParallelFor(ids_split_op.output, name="nested_dataset_loop_task")
    nested_dataset_loop_task.execution_options.caching_strategy.max_cache_staleness = "P0D"
    nested_dataset_loop_task.after(ids_split_op)

    inner_subdag_op = single_node_dag(char=dsl.InputValuePlaceholder())
    inner_subdag_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    inner_subdag_op.after(chars_split_op)

    create_model_from_dataset_op = read_single_dataset_generate_model(
        data=dsl.Collected(inner_subdag_op.outputs["dataset_from_subdag_"]),
        id=dsl.InputValuePlaceholder(),
        results=dsl.Output[Model](),
    )
    create_model_from_dataset_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    create_model_from_dataset_op.after(inner_subdag_op)

    read_models_op = read_models(
        models=dsl.Collected(nested_dataset_loop_task.outputs["model_from_dataset_"])