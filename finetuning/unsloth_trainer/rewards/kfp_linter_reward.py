def kfp_linter_score(code):
    return 10.0 if "@dsl.pipeline" in code and "import kfp" in code else 0.0
