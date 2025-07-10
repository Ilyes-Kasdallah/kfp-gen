from kfp import dsl


@dsl.component
def comp() -> str:
    from datetime import datetime
    now = datetime.now()
    print(now)
    return now.isoformat()


@dsl.pipeline
def my_pipeline() -> str:
    return comp().output
