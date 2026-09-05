EXAMPLES = [
    "What did the CIA know about Lee Harvey Oswald?",
    "What concerns did the CIA have about David Phillips' manuscript?",
    "What documents discuss Jack Ruby?",
]


HEADER_HTML = """
<div class="dr-brand">
    <div class="dr-mark">
        <span class="dr-bar dr-bar-1"></span>
        <span class="dr-bar dr-bar-2"></span>
        <span class="dr-bar dr-bar-3"></span>
    </div>

    <div class="dr-titles">
        <h1>JFK<span class="dr-sep">/</span>Research</h1>
        <p>Arnaud Konan - Archival Intelligence Investigation</p>
    </div>
</div>
"""

CSS = """
.gradio-container {
    max-width: 980px !important;
    margin: 0 auto !important;
    padding: 2.5rem 2rem 4rem !important;
    background: #f7f6f2 !important;
    color: #111 !important;
    font-family: Arial, Helvetica, sans-serif !important;
}

/* HEADER */

.dr-brand {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 1.4rem;
    padding-bottom: 1.25rem;
    border-bottom: 3px solid #111;
    margin-bottom: 2.5rem;
}

.dr-mark {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 38px;
}

.dr-bar {
    height: 7px;
    display: block;
}

.dr-bar-1 {
    background: #f2b300;
    width: 100%;
}

.dr-bar-2 {
    background: #209dd7;
    width: 70%;
}

.dr-bar-3 {
    background: #753991;
    width: 45%;
}

.dr-titles h1 {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    margin: 0;
    line-height: 1;
    text-transform: uppercase;
    color: #111;
}

.dr-sep {
    color: #f2b300;
    font-weight: 300;
}

.dr-titles p {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin: 0.55rem 0 0;
    color: #6f6f72;
}

/* QUERY ROW */

.dr-query-row {
    gap: 0 !important;
    align-items: stretch !important;
}

#dr-query,
#dr-query > div,
#dr-query .wrap,
#dr-query .form,
#dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#dr-query textarea,
#dr-query input {
    background: white !important;
    color: #111 !important;
    border: 2px solid #111 !important;
    border-radius: 0 !important;
    padding: 1.05rem 1.2rem !important;
    font-size: 1.05rem !important;
    min-height: 60px !important;
    resize: none !important;
    box-shadow: none !important;
}

#dr-query textarea:focus,
#dr-query input:focus {
    outline: none !important;
    border-color: #209dd7 !important;
    box-shadow: 6px 6px 0 0 #209dd7 !important;
}

/* BUTTON */

#dr-run {
    background: #f2b300 !important;
    color: #111 !important;
    border: 2px solid #111 !important;
    border-left: none !important;
    border-radius: 0 !important;
    font-size: 0.85rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    min-height: 60px !important;
    min-width: 150px !important;
}

#dr-run:hover {
    background: #753991 !important;
    color: white !important;
}

/* EXAMPLES */

.dr-examples-label {
    font-family: ui-monospace, SFMono-Regular, monospace;
    font-size: 0.65rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    margin: 2rem 0 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    color: #6f6f72;
}

.dr-examples-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #d7d7d7;
}

#dr-examples {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ANSWER */

#dr-report {
    margin-top: 2.5rem !important;
    padding-top: 1.75rem !important;
    border-top: 1px solid #d7d7d7 !important;
    background: transparent !important;
    color: #111 !important;
}

#dr-report a {
    color: #209dd7;
    text-decoration: underline;
}

footer {
    display: none !important;
}

@media (max-width: 700px) {
    .gradio-container {
        padding: 1.5rem 1rem 3rem !important;
    }

    .dr-query-row {
        flex-direction: column !important;
    }

    #dr-run {
        border-left: 2px solid #111 !important;
        border-top: none !important;
        width: 100% !important;
    }
}
"""

JS = """
() => {
    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) {
            el.focus();
            return true;
        }
        return false;
    };

    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""