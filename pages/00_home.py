import solara


@solara.component
def Page():
    markdown = """
    ## Mapping Non-Floodplain Wetlands

    ### Introduction

    An interactive web app for mapping surface depressions.

    - Web App: <https://giswqs-nfw-app.hf.space>
    - GitHub: <https://github.com/giswqs/nfw-app>
    - Hugging Face: <https://huggingface.co/spaces/giswqs/nfw-app>

    """

    solara.Markdown(markdown)
