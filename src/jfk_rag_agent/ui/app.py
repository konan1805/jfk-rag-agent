import gradio as gr
from dotenv import load_dotenv

from jfk_rag_agent.workflow import ask_jfk


load_dotenv()


def respond(question: str) -> str:
    if not question.strip():
        return "Please enter a question about the JFK assassination files."

    return ask_jfk(question)


custom_css = """
.gradio-container {
    max-width: 980px !important;
    margin: 0 auto !important;
    background: #f7f6f2 !important;
    font-family: Arial, Helvetica, sans-serif;
}

#header-row {
    margin-top: 28px;
    margin-bottom: 10px;
}

#brand-title {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

#brand-subtitle {
    font-size: 10px;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-left: 2px;
}

#top-divider {
    border-top: 3px solid #111;
    margin-top: 24px;
    margin-bottom: 26px;
}

#question-box textarea {
    font-size: 17px !important;
    border: 2px solid #111 !important;
    border-radius: 0 !important;
    min-height: 60px !important;
    background: white !important;
}

#investigate-btn {
    background: #f2b300 !important;
    color: #111 !important;
    border: 2px solid #111 !important;
    border-radius: 0 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    min-height: 60px;
}

#investigate-btn:hover {
    background: #dca400 !important;
}

.section-label {
    font-size: 10px;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-top: 24px;
    margin-bottom: 12px;
}

.example-btn {
    border-radius: 0 !important;
    border: 1px solid #d7d7d7 !important;
    background: white !important;
    color: #111 !important;
    text-align: left !important;
    min-height: 54px;
}

#answer-panel {
    margin-top: 26px;
    padding: 22px;
    border-top: 1px solid #d7d7d7;
    background: transparent;
}

footer {
    display: none !important;
}
"""


with gr.Blocks(
    title="JFK Research",
    css=custom_css,
) as demo:

    with gr.Column(elem_id="header-row"):
        gr.HTML(
            """
            <div id="brand-title">JFK / RESEARCH</div>
            <div id="brand-subtitle">
                ARCHIVAL INTELLIGENCE INVESTIGATION
            </div>
            <div id="top-divider"></div>
            """
        )

    with gr.Row(equal_height=True):
        question = gr.Textbox(
            placeholder="Ask a JFK research question...",
            show_label=False,
            lines=1,
            elem_id="question-box",
            scale=4,
        )

        investigate_button = gr.Button(
            "INVESTIGATE",
            elem_id="investigate-btn",
            scale=1,
        )

    gr.HTML(
        """
        <div class="section-label">
            PICK ONE
        </div>
        """
    )

    gr.Markdown("⌁ Examples")

    with gr.Row():
        example_1 = gr.Button(
            "What did the CIA know about Lee Harvey Oswald?",
            elem_classes=["example-btn"],
        )

        example_2 = gr.Button(
            "What concerns did the CIA have about David Phillips' manuscript?",
            elem_classes=["example-btn"],
        )

    with gr.Row():
        example_3 = gr.Button(
            "What documents discuss Jack Ruby?",
            elem_classes=["example-btn"],
        )

    answer = gr.Markdown(
        elem_id="answer-panel",
    )

    investigate_button.click(
        fn=respond,
        inputs=question,
        outputs=answer,
    )

    question.submit(
        fn=respond,
        inputs=question,
        outputs=answer,
    )

    example_1.click(
        fn=lambda: "What did the CIA know about Lee Harvey Oswald?",
        outputs=question,
    )

    example_2.click(
        fn=lambda: "What concerns did the CIA have about David Phillips' manuscript?",
        outputs=question,
    )

    example_3.click(
        fn=lambda: "What documents discuss Jack Ruby?",
        outputs=question,
    )


def main() -> None:
    demo.launch()


if __name__ == "__main__":
    main()