from __future__ import annotations

import json

from .config import Settings
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .rules import default_priority_bucket, default_recommendations, deterministic_analysis_text
from .schemas import EquipmentNarrative, PreAnalysisFacts


def build_fallback_narrative(facts: PreAnalysisFacts) -> EquipmentNarrative:
    fault_names = [item.fault_name for item in facts.fault_hypotheses]
    recommendations = default_recommendations(fault_names, facts.overall_level)

    return EquipmentNarrative(
        no=facts.no,
        tag_name=facts.tag_name,
        deskripsi=facts.deskripsi,
        titik_nilai_vibrasi_tertinggi=(
            f"{facts.top_vibration_value:.1f} mm/s "
            f"({facts.top_vibration_point} - {facts.top_vibration_metric.upper()})"
        ),
        overall_level=facts.overall_level,
        analysis=deterministic_analysis_text(facts),
        recommendations=recommendations,
        priority_bucket=default_priority_bucket(facts.overall_level),  # type: ignore[arg-type]
    )


def build_agent_narrative(facts: PreAnalysisFacts, settings: Settings) -> EquipmentNarrative:
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY belum diisi.")

    try:
        from langchain.agents import create_agent
        from langchain.agents.structured_output import ToolStrategy
        from langchain_openrouter import ChatOpenRouter
    except ImportError as exc:
        raise RuntimeError(
            "langchain atau langchain_openrouter belum terpasang. Jalankan pip install -r requirements.txt"
        ) from exc

    from .tools import get_fault_library, get_report_style_guide, get_threshold_reference

    model = ChatOpenRouter(
        model=settings.openrouter_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        reasoning={
            "effort": settings.reasoning_effort,
            "summary": settings.reasoning_summary,
        },
    )

    agent = create_agent(
        model=model,
        tools=[get_threshold_reference, get_fault_library, get_report_style_guide],
        system_prompt=SYSTEM_PROMPT,
        response_format=ToolStrategy(EquipmentNarrative),
    )

    facts_json = json.dumps(facts.model_dump(mode="json"), ensure_ascii=False, indent=2)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": build_user_prompt(facts_json),
                }
            ]
        }
    )

    structured = result.get("structured_response")
    if structured is None:
        raise RuntimeError("Agent tidak mengembalikan structured_response.")

    if isinstance(structured, EquipmentNarrative):
        return structured

    return EquipmentNarrative.model_validate(structured)


def analyze_equipment(
    facts: PreAnalysisFacts,
    settings: Settings,
    mode: str = "agent",
) -> EquipmentNarrative:
    if mode == "fallback":
        return build_fallback_narrative(facts)

    try:
        return build_agent_narrative(facts, settings)
    except Exception:
        return build_fallback_narrative(facts)