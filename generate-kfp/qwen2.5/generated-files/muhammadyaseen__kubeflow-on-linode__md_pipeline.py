
from kfp import dsl

@dsl.pipeline(name="md-pipeline")
def md_pipeline():
    # Define the first component: write_simple_markdown_table
    write_simple_markdown_table = dsl.component(
        name="write_simple_markdown_table",
        description="Creates a Markdown file containing a simple table with animal names.",
        inputs={
            "animal_names": dsl.input("animal_names", type="string")
        },
        outputs={
            "markdown_artifact": dsl.output("markdown_artifact", type="string")
        }
    )

    # Define the second component: generate_markdown_table
    generate_markdown_table = dsl.component(
        name="generate_markdown_table",
        description="Generates a Markdown file containing animal names.",
        inputs={
            "animal_names": dsl.input("animal_names", type="string")
        },
        outputs={
            "markdown_artifact": dsl.output("markdown_artifact", type="string")
        }
    )

    # Define the third component: visualize_markdown_table
    visualize_markdown_table = dsl.component(
        name="visualize_markdown_table",
        description="Visualizes the generated Markdown file.",
        inputs={
            "markdown_artifact": dsl.input("markdown_artifact", type="string")
        },
        outputs={
            "visualization_artifact": dsl.output("visualization_artifact", type="string")
        }
    )

    # Define the fourth component: display_visualization
    display_visualization = dsl.component(
        name="display_visualization",
        description="Displays the visualization artifact.",
        inputs={
            "visualization_artifact": dsl.input("visualization_artifact", type="string")
        }
    )

    # Connect the components in the pipeline
    write_simple_markdown_table.outputs["markdown_artifact"].connect(generate_markdown_table.inputs["animal_names"])
    generate_markdown_table.outputs["markdown_artifact"].connect(visualize_markdown_table.inputs["markdown_artifact"])
    visualize_markdown_table.outputs["visualization_artifact"].connect(display_visualization.inputs["visualization_artifact"])

    return md_pipeline
