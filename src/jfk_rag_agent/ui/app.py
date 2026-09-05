import gradio as gr
from dotenv import load_dotenv

from jfk_rag_agent.ui.styles import CSS, JS, EXAMPLES, HEADER_HTML
from jfk_rag_agent.workflow import stream_jfk


load_dotenv(override=True)


async def run(question: str):
    if not question.strip():
        yield "Please enter a question about the JFK assassination files."
        return

    async for partial_answer in stream_jfk(question):
        yield partial_answer


with gr.Blocks(title="JFK Research") as ui:
    gr.HTML(HEADER_HTML)

    with gr.Row(elem_classes="dr-query-row"):
        query_textbox = gr.Textbox(
            placeholder="Ask a JFK research question...",
            show_label=False,
            container=False,
            autofocus=True,
            elem_id="dr-query",
            scale=5,
        )

        run_button = gr.Button(
            "Investigate",
            variant="primary",
            elem_id="dr-run",
            scale=1,
        )

    gr.HTML('<div class="dr-examples-label">Pick one</div>')

    gr.Examples(
        examples=EXAMPLES,
        inputs=query_textbox,
        elem_id="dr-examples",
    )

    report = gr.Markdown(
        elem_id="dr-report",
    )

    run_button.click(
        run,
        inputs=query_textbox,
        outputs=report,
    )

    query_textbox.submit(
        run,
        inputs=query_textbox,
        outputs=report,
    )


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
    )