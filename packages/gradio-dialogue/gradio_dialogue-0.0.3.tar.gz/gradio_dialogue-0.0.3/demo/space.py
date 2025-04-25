
import gradio as gr
from app import demo as app
import os

_docs = {'Dialogue': {'description': 'Creates a textarea for user to enter string input or display string output.\n', 'members': {'__init__': {'speakers': {'type': 'list[str]', 'description': None}, 'formatter': {'type': 'typing.Optional[typing.Callable][Callable, None]', 'default': 'None', 'description': None}, 'emotions': {'type': 'list[str] | None', 'default': 'None', 'description': None}, 'value': {'type': 'str | None', 'default': 'None', 'description': 'text to show in textbox. If a function is provided, the function will be called each time the app loads to set the initial value of this component.'}, 'label': {'type': 'str | None', 'default': '"Dialogue"', 'description': 'the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.'}, 'info': {'type': 'str | None', 'default': '"Type : in the dialogue line to see the available emotion and intonation tags"', 'description': 'additional component description, appears below the label in smaller font. Supports markdown / HTML syntax.'}, 'placeholder': {'type': 'str | None', 'default': '"Enter dialogue here..."', 'description': 'placeholder hint to provide behind textarea.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display the label. If False, the copy button is hidden as well as well as the label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'if True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'autofocus': {'type': 'bool', 'default': 'False', 'description': 'If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.'}, 'autoscroll': {'type': 'bool', 'default': 'True', 'description': 'If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'show_copy_button': {'type': 'bool', 'default': 'False', 'description': 'If True, includes a copy button to copy the text in the textbox. Only applies if show_label is True.'}, 'max_lines': {'type': 'int | None', 'default': 'None', 'description': 'maximum number of line rows to provide in textarea. Must be at least `lines`. If not provided, the maximum number of lines is max(lines, 20) for "text" type, and 1 for "password" and "email" types.'}}, 'postprocess': {}, 'preprocess': {}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the Dialogue changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the Dialogue.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the Dialogue. Uses event data gradio.SelectData to carry `value` referring to the label of the Dialogue, and `selected` to refer to state of the Dialogue. See EventData documentation on how to use this event data'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the Dialogue is focused.'}, 'focus': {'type': None, 'default': None, 'description': 'This listener is triggered when the Dialogue is focused.'}, 'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the Dialogue is unfocused/blurred.'}, 'stop': {'type': None, 'default': None, 'description': 'This listener is triggered when the user reaches the end of the media playing in the Dialogue.'}, 'copy': {'type': None, 'default': None, 'description': 'This listener is triggered when the user copies content from the Dialogue. Uses event data gradio.CopyData to carry information about the copied content. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_dialogue`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_dialogue
```

## Usage

```python

import gradio as gr
from gradio_dialogue import Dialogue


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Dialogue Demo"):
            Dialogue(interactive=True, emotions=["laugh", "sigh"], speakers=["Speaker 1", "Speaker 2"])
        with gr.Tab("Component  Functions"):
            gr.Markdown("## Component Functions")
            dialogue = Dialogue(emotions=["laugh", "sigh"], speakers=["S1", "S2"])
            textbox = gr.Textbox(label="Textbox")
            with gr.Row():
                with gr.Column():
                    process = gr.Button("Process")
                    process.click(lambda x: x, dialogue, textbox)
                    dialogue.submit(lambda x: x, dialogue, textbox)
                with gr.Column():
                    process = gr.Button("Update")
                    process.click(lambda: [{"speaker": "S1", "text": "Updated!"}], None, dialogue)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Dialogue`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Dialogue"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Dialogue"]["events"], linkify=['Event'])







    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {};
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
