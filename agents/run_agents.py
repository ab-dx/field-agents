import asyncio
import threading
from state.state import AppState
from agents.agent import create_agents
from entities.customer_reviews import CustomerReviewReport
from entities.employee_reviews import EmployeeReviewReport


async def run_agents():
    state = AppState.instance()
    agents = create_agents()
    for src, agent in agents:
        handler = agent.run()

        async for event in handler.stream_events():
            print(event)
            if(hasattr(event, 'response')):
                state.add_event(str(event.response))

        result = await handler
        print(result)

        structured_output = getattr(result, "structured_output", result)
    

        if src in ["PlayStore", "Reddit", "X"]:
            report = CustomerReviewReport(reviews=structured_output.reviews)
            print(report.model_dump_json(indent=2))
            state.add_report(report.model_dump_json())
            if hasattr(structured_output, "avg_star_rating"):
                state.update_kpi(f"{src} Average star ratings:", structured_output.avg_star_rating)

            if hasattr(structured_output, "no_of_reviews"):
                state.update_kpi(f"{src} Total Reviews:", structured_output.no_of_reviews)

            if hasattr(structured_output, "no_of_downloads"):
                state.update_kpi(f"{src} Total Downloads:", structured_output.no_of_downloads)

            state.update_kpi(f"{src} Sentiment Score", report.sentiment_score)
            state.update_kpi(f"{src} Customer Satisfaction", report.avg_csat)
            state.update_kpi(f"{src} Average NPS Rating", report.avg_nps_rating)
            state.update_kpi(f"{src} NPS", report.nps)
            state.update_kpi(f"{src} Data Quality", report.data_quality)
        
            #EMPLOYEE REALM
        else:
            all_employee_reviews = [
                structured_output.reviews +
                structured_output.salaries +
                structured_output.benifits
            ]
            report = EmployeeReviewReport(
                comp_name=structured_output.comp_name,
                overall_star_rating=structured_output.overall_star_rating,
                recommend_to_friend_pct=structured_output.recommend_to_friend_pct,
                ceo_approval_pct=structured_output.ceo_approval_pct,
                no_of_reviews=len(all_employee_reviews),
                reviews=all_employee_reviews
            )
            state.add_report(report.model_dump_json())
            state.update_kpi(f"{src} Sentiment Score", report.sentiment_score)
            state.update_kpi(f"{src} Employee Satisfaction", report.avg_esat)
            state.update_kpi(f"{src} Average ENPS Rating", report.avg_enps_rating)
            state.update_kpi(f"{src} True ENPS(Relative)", report.true_enps_score)
            state.update_kpi(f"{src} Review Stars", report.avg_review_star)
            state.update_kpi(f"{src} Salary Stars", report.avg_salary_star)
            state.update_kpi(f"{src} Benifit Stars", report.avg_benifit_star)
            state.update_kpi(f"{src} Overall Stars", report.avg_glassdoor_star)
            state.update_kpi(f"{src} Data Quality", report.data_quality)

def launch_agents(query):
    if len(query) == 0:
        return
    AppState.instance().set_target(query)
    agent_thread = threading.Thread(target=lambda: asyncio.run(run_agents()), daemon=True)
    agent_thread.start()

if __name__ == "__main__":
    launch_agents("Clash Royale")

