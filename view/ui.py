from agents.run_agents import launch_agents
from state.state import AppState
import gradio as gr


def load_ui():
    with gr.Blocks(title="Company KPI Monitor") as demo:
        gr.Markdown("# 📊 Real-Time Company KPI Dashboard")
        with gr.Row():
            with gr.Column(scale=4):
                query_input = gr.Textbox(label="Company Name", placeholder="")
            with gr.Column(scale=1):
                submit_btn = gr.Button("Launch Agents", variant="primary")
        # query_input.submit(fn=launch_agents, inputs=query_input)
        submit_btn.click(
            fn=launch_agents, 
            inputs=query_input,      # Pass textbox value
        )
        with gr.Row():
            with gr.Column(scale=1):
                    gr.Markdown("### 🔔 Live Agent Events")
                    events_out = gr.Markdown("\n")
                    events_timer = gr.Timer(value=1, active=True)
                    events_timer.tick(
                        fn=AppState.instance().get_events_md,
                        # inputs=events_out,         # previous value
                        outputs=events_out,        # updated value
                    )
            with gr.Column(scale=2):
                gr.Markdown("### 📈 Live KPIs")
                kpis_out = gr.Markdown("Loading KPIs...", max_height=400)
                kpi_timer = gr.Timer(3, active=True)  # Slower refresh
                kpi_timer.tick(fn=AppState.instance().get_kpis_md, outputs=kpis_out)
        

        demo.load(lambda: "", outputs=[events_out])
        demo.load(fn=AppState.instance().get_kpis_md, outputs=[kpis_out])
    demo.queue().launch()

