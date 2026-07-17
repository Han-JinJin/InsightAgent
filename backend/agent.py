from tools import (
    say_hello,
    who_are_you,
    capabilities,
    add_numbers,
    data_summary,
    total_sales,
    average_sales,
    max_single_sale,
    min_single_sale,
    best_region,
    worst_region,
    region_sales_summary,
)


def run_agent(question: str):
    try:
        if "你好" in question:
            answer = say_hello.invoke({})
            tool_used = "say_hello"

        elif "你是谁" in question:
            answer = who_are_you.invoke({})
            tool_used = "who_are_you"

        elif "你会什么" in question:
            answer = capabilities.invoke({})
            tool_used = "capabilities"

        elif "2+3" in question or "2 + 3" in question:
            answer = add_numbers.invoke({
                "a": 2,
                "b": 3
            })
            tool_used = "add_numbers"

        elif (
            "数据概览" in question
            or "查看数据" in question
            or "数据长什么样" in question
            or "有哪些字段" in question
        ):
            answer = data_summary.invoke({})
            tool_used = "data_summary"

        elif "总销售额" in question:
            answer = total_sales.invoke({})
            tool_used = "total_sales"

        elif "平均销售额" in question:
            answer = average_sales.invoke({})
            tool_used = "average_sales"

        elif "最大单笔" in question or "单笔最高" in question:
            answer = max_single_sale.invoke({})
            tool_used = "max_single_sale"

        elif "最小单笔" in question or "单笔最低" in question:
            answer = min_single_sale.invoke({})
            tool_used = "min_single_sale"

        elif (
            "最高销售额区域" in question
            or "哪个区域销售额最高" in question
            or "销售额最高的区域" in question
            or "销售额最高的区域是哪个" in question
        ):
            answer = best_region.invoke({})
            tool_used = "best_region"

        elif (
            "最低销售额区域" in question
            or "哪个区域销售额最低" in question
            or "销售额最低的区域" in question
            or "销售额最低的区域是哪个" in question
        ):
            answer = worst_region.invoke({})
            tool_used = "worst_region"

        elif (
            "按区域汇总" in question
            or "区域汇总" in question
            or "各区域销售额" in question
            or "每个区域销售额" in question
        ):
            answer = region_sales_summary.invoke({})
            tool_used = "region_sales_summary"

        else:
            answer = "这个问题我还不会。后面接入大模型后，我可以理解更多自然语言表达。"
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
