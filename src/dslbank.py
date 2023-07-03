def get_dsl(name: str):
    """Return the DSL by name."""
    # read data/name.tex file and return it, other wise return error message
    try:
        with open(f"data/{name}.tex", "r") as f:
            dsl = f.read()
            f.close()
            return {
                "dsl": dsl, 
                "domain": name,
                "format": "tex"
            }
    except:
        return {"message": "DSL not found."}