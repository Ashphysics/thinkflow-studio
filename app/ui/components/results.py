"""
Results rendering component for Streamlit UI.
"""
import streamlit as st
import json
from app.orchestrator.context import WorkflowContext

def render_results(context: WorkflowContext):
    if not context or context.status != "completed":
        return

    st.markdown("## Analysis Results")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "💡 Idea Analysis", 
        "🔍 Critic Report", 
        "🧠 Framework", 
        "🗺️ Execution Roadmap"
    ])
    
    with tab1:
        if context.idea_analysis:
            st.header(context.idea_analysis.idea_title)
            st.info(context.idea_analysis.one_sentence_summary)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Category:** {context.idea_analysis.category}")
                st.markdown(f"**Domain:** {context.idea_analysis.domain}")
            with col2:
                st.markdown(f"**Primary Goal:** {context.idea_analysis.primary_goal}")
                st.markdown(f"**Confidence:** {context.idea_analysis.confidence_score}")
                
            with st.expander("Target Users & Assumptions"):
                st.write("**Users:**", ", ".join(context.idea_analysis.target_users))
                st.write("**Assumptions:**")
                for a in context.idea_analysis.assumptions:
                    st.markdown(f"- {a}")
                    
    with tab2:
        if context.critic_analysis:
            col1, col2 = st.columns(2)
            with col1:
                st.success("Strengths")
                for s in context.critic_analysis.strengths:
                    st.markdown(f"- {s}")
            with col2:
                st.error("Weaknesses & Risks")
                for w in context.critic_analysis.weaknesses:
                    st.markdown(f"- {w}")
                for r in context.critic_analysis.risks:
                    st.markdown(f"- {r}")
                    
            with st.expander("Validation Questions"):
                for q in context.critic_analysis.validation_questions:
                    st.markdown(f"- {q}")

    with tab3:
        if context.framework_selection:
            st.subheader(f"Selected: {context.framework_selection.selected_framework}")
            st.write(context.framework_selection.selection_reason)
            st.json(context.framework_selection.framework_template)

    with tab4:
        if context.execution_plan:
            st.header(context.execution_plan.project_title)
            st.write(context.execution_plan.project_summary)
            
            st.markdown(f"**Recommended Strategy:** {context.execution_plan.recommended_strategy}")
            st.markdown(f"**Next Best Action:** {context.execution_plan.next_best_action}")
            
            st.subheader("Execution Phases")
            for phase in context.execution_plan.execution_phases:
                with st.expander(f"{phase.phase_name}"):
                    st.write(phase.description)
                    
            if context.execution_plan.filled_framework:
                st.subheader("Filled Framework Output")
                st.json(context.execution_plan.filled_framework)
