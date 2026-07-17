from typing import Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from tools import (
    data_summary,
    data_quality_report,
    kpi_summary,
    numeric_summary,
    region_sales_summary,
    best_region,
    worst_region,
    category_sales_summary,
    top_products,
    channel_sales_summary,
    monthly_sales_trend,
    profit_analysis,
    detect_sales_outliers,
    generate_markdown_report,
    create_region_sales_chart,
    create_category_sales_chart,
    create_channel_sales_chart,
    create_monthly_sales_trend_chart,
    create_all_charts,
)


class AgentState(TypedDict, total=False):
    question: str
    intent: str
    answer: Any
    tool_used: str
    final_response: dict


def classify_question(state: AgentState) -> AgentState:
    question = state["question"]

    if (
        "数据概览" in question
        or "查看数据" in question
        or "数据长什么样" in question
        or "有哪些字段" in question
    ):
        intent = "data_summary"

    elif (
        "数据质量" in question
        or "缺失值" in question
        or "重复行" in question
        or "字段类型" in question
    ):
        intent = "data_quality_report"

    elif (
        "kpi" in question.lower()
        or "核心指标" in question
        or "指标总览" in question
        or "经营概览" in question
        or "总览" in question
    ):
        intent = "kpi_summary"

    elif (
        "数值统计" in question
        or "统计摘要" in question
        or "describe" in question.lower()
    ):
        intent = "numeric_summary"

    elif (
        "最高销售额区域" in question
        or "哪个区域销售额最高" in question
        or "销售额最高的区域" in question
        or "销售额最高的区域是哪个" in question
        or "表现最好的区域" in question
    ):
        intent = "best_region"

    elif (
        "最低销售额区域" in question
        or "哪个区域销售额最低" in question
        or "销售额最低的区域" in question
        or "销售额最低的区域是哪个" in question
        or "表现最差的区域" in question
    ):
        intent = "worst_region"

    elif (
        "按区域汇总" in question
        or "区域汇总" in question
        or "各区域销售额" in question
        or "每个区域销售额" in question
    ):
        intent = "region_sales_summary"

    elif (
        "品类" in question
        or "类别" in question
        or "category" in question.lower()
    ):
        intent = "category_sales_summary"

    elif (
        "产品排名" in question
        or "top产品" in question.lower()
        or "最好的产品" in question
        or "销售最高的产品" in question
    ):
        intent = "top_products"

    elif (
        "渠道" in question
        or "channel" in question.lower()
    ):
        intent = "channel_sales_summary"

    elif (
        "趋势" in question
        or "月度" in question
        or "按月" in question
        or "每月" in question
    ):
        intent = "monthly_sales_trend"

    elif (
        "利润" in question
        or "利润率" in question
        or "毛利" in question
        or "profit" in question.lower()
        or "margin" in question.lower()
    ):
        intent = "profit_analysis"

    elif (
        "异常" in question
        or "离群" in question
        or "outlier" in question.lower()
    ):
        intent = "detect_sales_outliers"

    elif (
        "区域图" in question
        or "区域销售图" in question
        or "区域柱状图" in question
    ):
        intent = "create_region_sales_chart"

    elif (
        "品类图" in question
        or "品类销售图" in question
        or "品类柱状图" in question
    ):
        intent = "create_category_sales_chart"

    elif (
        "渠道图" in question
        or "渠道销售图" in question
        or "渠道柱状图" in question
    ):
        intent = "create_channel_sales_chart"

    elif (
        "趋势图" in question
        or "月度趋势图" in question
        or "折线图" in question
    ):
        intent = "create_monthly_sales_trend_chart"

    elif (
        "生成图表" in question
        or "所有图表" in question
        or "全部图表" in question
        or "可视化" in question
    ):
        intent = "create_all_charts"

    elif (
        "生成报告" in question
        or "分析报告" in question
        or "导出报告" in question
        or "report" in question.lower()
    ):
        intent = "generate_markdown_report"

    else:
        intent = "unknown"

    return {
        "intent": intent
    }


def execute_tool(state: AgentState) -> AgentState:
    intent = state["intent"]

    try:
        if intent == "data_summary":
            answer = data_summary.invoke({})
            tool_used = "data_summary"

        elif intent == "data_quality_report":
            answer = data_quality_report.invoke({})
            tool_used = "data_quality_report"

        elif intent == "kpi_summary":
            answer = kpi_summary.invoke({})
            tool_used = "kpi_summary"

        elif intent == "numeric_summary":
            answer = numeric_summary.invoke({})
            tool_used = "numeric_summary"

        elif intent == "region_sales_summary":
            answer = region_sales_summary.invoke({})
            tool_used = "region_sales_summary"

        elif intent == "best_region":
            answer = best_region.invoke({})
            tool_used = "best_region"

        elif intent == "worst_region":
            answer = worst_region.invoke({})
            tool_used = "worst_region"

        elif intent == "category_sales_summary":
            answer = category_sales_summary.invoke({})
            tool_used = "category_sales_summary"

        elif intent == "top_products":
            answer = top_products.invoke({})
            tool_used = "top_products"

        elif intent == "channel_sales_summary":
            answer = channel_sales_summary.invoke({})
            tool_used = "channel_sales_summary"

        elif intent == "monthly_sales_trend":
            answer = monthly_sales_trend.invoke({})
            tool_used = "monthly_sales_trend"

        elif intent == "profit_analysis":
            answer = profit_analysis.invoke({})
            tool_used = "profit_analysis"

        elif intent == "detect_sales_outliers":
            answer = detect_sales_outliers.invoke({})
            tool_used = "detect_sales_outliers"

        elif intent == "create_region_sales_chart":
            answer = create_region_sales_chart.invoke({})
            tool_used = "create_region_sales_chart"

        elif intent == "create_category_sales_chart":
            answer = create_category_sales_chart.invoke({})
            tool_used = "create_category_sales_chart"

        elif intent == "create_channel_sales_chart":
            answer = create_channel_sales_chart.invoke({})
            tool_used = "create_channel_sales_chart"

        elif intent == "create_monthly_sales_trend_chart":
            answer = create_monthly_sales_trend_chart.invoke({})
            tool_used = "create_monthly_sales_trend_chart"

        elif intent == "create_all_charts":
            answer = create_all_charts.invoke({})
            tool_used = "create_all_charts"
            
        elif intent == "generate_markdown_report":
            answer = generate_markdown_report.invoke({})
            tool_used = "generate_markdown_report"

        else:
            answer = (
                "这个问题我还不会。你可以试试：数据概览、核心指标、数据质量、"
                "区域汇总、品类分析、产品排名、渠道分析、月度趋势、利润分析、异常检测、生成报告。"
            )
            tool_used = "none"

        return {
            "answer": answer,
            "tool_used": tool_used
        }

    except Exception as error:
        return {
            "answer": str(error),
            "tool_used": "error"
        }


def format_response(state: AgentState) -> AgentState:
    return {
        "final_response": {
            "answer": state.get("answer"),
            "tool_used": state.get("tool_used"),
            "intent": state.get("intent")
        }
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node("classify_question", classify_question)
graph_builder.add_node("execute_tool", execute_tool)
graph_builder.add_node("format_response", format_response)

graph_builder.add_edge(START, "classify_question")
graph_builder.add_edge("classify_question", "execute_tool")
graph_builder.add_edge("execute_tool", "format_response")
graph_builder.add_edge("format_response", END)

graph = graph_builder.compile()


def run_graph_agent(question: str):
    result = graph.invoke({
        "question": question
    })

    return result["final_response"]