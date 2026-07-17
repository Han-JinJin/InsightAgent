import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from langchain.tools import tool


CURRENT_FILE_PATH = "uploads/current.csv"
REPORT_PATH = "reports/analysis_report.md"
CHART_DIR = "reports/charts"


def ensure_report_dirs():
    os.makedirs("reports", exist_ok=True)
    os.makedirs(CHART_DIR, exist_ok=True)


def setup_chinese_font():
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False

def format_number(value):
    try:
        return f"{float(value):,.2f}".rstrip("0").rstrip(".")
    except Exception:
        return str(value)


def markdown_table_from_dict(data: dict):
    if not isinstance(data, dict):
        return str(data)

    lines = [
        "| 指标 | 数值 |",
        "|---|---:|"
    ]

    label_map = {
        "sales_column": "销售额字段",
        "row_count": "数据行数",
        "total_sales": "总销售额",
        "average_sales": "平均销售额",
        "max_single_sale": "最大单笔销售额",
        "min_single_sale": "最小单笔销售额",
        "total_profit": "总利润",
        "profit_margin": "利润率",
        "rows": "数据行数",
        "columns": "字段数量",
        "duplicate_rows": "重复行数量",
        "missing_values": "缺失值情况",
        "lower_bound": "异常值下界",
        "upper_bound": "异常值上界",
        "outlier_count": "异常值数量",
    }

    for key, value in data.items():
        label = label_map.get(key, key)

        if isinstance(value, dict):
            value = str(value)
        elif isinstance(value, list):
            value = str(value)
        elif isinstance(value, int) or isinstance(value, float):
            value = format_number(value)

        lines.append(f"| {label} | {value} |")

    return "\n".join(lines)


def markdown_table_from_records(records: list):
    if not isinstance(records, list) or len(records) == 0:
        return "暂无数据。"

    if not isinstance(records[0], dict):
        return str(records)

    columns = list(records[0].keys())

    header = "| " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---" for _ in columns]) + "|"

    lines = [header, separator]

    for row in records:
        values = []

        for col in columns:
            value = row.get(col, "")

            if isinstance(value, int) or isinstance(value, float):
                value = format_number(value)

            values.append(str(value))

        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def get_top_record(records, value_key_candidates):
    if not isinstance(records, list) or len(records) == 0:
        return None

    if not isinstance(records[0], dict):
        return None

    value_key = None

    for candidate in value_key_candidates:
        if candidate in records[0]:
            value_key = candidate
        break

    if value_key is None:
        return None

    sorted_records = sorted(
        records,
        key=lambda x: float(x.get(value_key, 0)),
        reverse=True
    )

    return sorted_records[0]


def generate_business_insights(kpi, region, category, channel, trend, profit, outliers):
    insights = []

    if isinstance(kpi, dict):
        total_sales = kpi.get("total_sales")
        average_sales = kpi.get("average_sales")
        total_profit = kpi.get("total_profit")
        profit_margin = kpi.get("profit_margin")

        if total_sales is not None:
            insights.append(f"本次数据总销售额为 {format_number(total_sales)}。")

        if average_sales is not None:
            insights.append(f"平均单笔销售额为 {format_number(average_sales)}。")

        if total_profit is not None:
            insights.append(f"总利润为 {format_number(total_profit)}，整体利润率为 {profit_margin}。")

    if isinstance(region, list) and len(region) > 0:
        top_region = get_top_record(region, ["sales", "销售额", "amount", "revenue"])

        if top_region is not None:
            region_name = top_region.get("region") or top_region.get("区域") or top_region.get("地区")
            sales_value = top_region.get("sales") or top_region.get("销售额") or top_region.get("amount") or top_region.get("revenue")
            insights.append(f"区域维度中，{region_name} 的销售额最高，为 {format_number(sales_value)}。")

    if isinstance(category, list) and len(category) > 0:
        top_category = get_top_record(category, ["sales", "销售额", "amount", "revenue"])

        if top_category is not None:
            category_name = top_category.get("category") or top_category.get("品类") or top_category.get("类别")
            sales_value = top_category.get("sales") or top_category.get("销售额") or top_category.get("amount") or top_category.get("revenue")
            insights.append(f"品类维度中，{category_name} 是核心销售品类，销售额为 {format_number(sales_value)}。")

    if isinstance(channel, list) and len(channel) > 0:
        top_channel = get_top_record(channel, ["sales", "销售额", "amount", "revenue"])

        if top_channel is not None:
            channel_name = top_channel.get("channel") or top_channel.get("渠道")
            sales_value = top_channel.get("sales") or top_channel.get("销售额") or top_channel.get("amount") or top_channel.get("revenue")
            insights.append(f"渠道维度中，{channel_name} 渠道贡献最高，销售额为 {format_number(sales_value)}。")

    if isinstance(trend, list) and len(trend) > 0:
        top_month = get_top_record(trend, ["sales", "销售额", "amount", "revenue"])

        if top_month is not None:
            month = top_month.get("month")
            sales_value = top_month.get("sales") or top_month.get("销售额") or top_month.get("amount") or top_month.get("revenue")
            insights.append(f"月度趋势中，{month} 销售额最高，为 {format_number(sales_value)}。")

    if isinstance(outliers, dict):
        outlier_count = outliers.get("outlier_count")

        if outlier_count == 0:
            insights.append("异常检测结果显示，当前数据中没有明显销售额异常值。")
        elif outlier_count is not None:
            insights.append(f"异常检测发现 {outlier_count} 条疑似异常销售记录，建议进一步核查。")

    if len(insights) == 0:
        insights.append("当前数据字段有限，暂未生成明确业务洞察。")

    return insights


def generate_business_recommendations(kpi, region, category, channel, trend, profit, outliers):
    recommendations = []

    if isinstance(region, list) and len(region) >= 2:
        recommendations.append("建议重点关注排名靠后的区域，结合城市、渠道和产品结构进一步拆解销售差距。")

    if isinstance(category, list) and len(category) >= 2:
        recommendations.append("建议评估高销售品类的持续增长空间，同时分析低销售品类是否存在定价、库存或渠道问题。")

    if isinstance(channel, list) and len(channel) >= 2:
        recommendations.append("建议对高贡献渠道加大资源投入，同时优化低贡献渠道的转化效率。")

    if isinstance(trend, list) and len(trend) >= 3:
        recommendations.append("建议结合月度趋势中的高峰和低谷月份，进一步分析促销、季节性和供给因素的影响。")

    if isinstance(profit, dict):
        margin_text = profit.get("profit_margin")

        if margin_text is not None:
            recommendations.append(f"当前利润率为 {margin_text}，建议持续跟踪高销售产品与高利润产品是否一致。")

    if isinstance(outliers, dict):
        outlier_count = outliers.get("outlier_count")

        if outlier_count and outlier_count > 0:
            recommendations.append("建议优先核查异常销售记录，判断是否由大客户订单、录入错误或特殊活动造成。")

    if len(recommendations) == 0:
        recommendations.append("建议补充更多业务字段，例如客户类型、门店、销售人员和订单状态，以提升分析深度。")

    return recommendations


def load_current_data():
    if not os.path.exists(CURRENT_FILE_PATH):
        raise FileNotFoundError("还没有上传CSV文件，请先调用 /upload 上传文件。")

    df = pd.read_csv(CURRENT_FILE_PATH)

    if df.empty:
        raise ValueError("CSV文件是空的。")

    return df


def safe_number(value):
    try:
        return round(float(value), 2)
    except Exception:
        return value


def find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def get_sales_column(df):
    return find_column(df, ["sales", "销售额", "amount", "revenue"])


def get_region_column(df):
    return find_column(df, ["region", "区域", "地区"])


def get_product_column(df):
    return find_column(df, ["product", "产品", "sku"])


def get_category_column(df):
    return find_column(df, ["category", "品类", "类别"])


def get_channel_column(df):
    return find_column(df, ["channel", "渠道"])


def get_date_column(df):
    return find_column(df, ["date", "日期", "order_date", "订单日期"])


def get_profit_column(df):
    return find_column(df, ["profit", "利润"])


def get_cost_column(df):
    return find_column(df, ["cost", "成本"])


@tool
def data_summary():
    """查看当前上传数据的基础概览"""
    df = load_current_data()

    return {
        "rows": len(df),
        "columns_count": len(df.columns),
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records")
    }


@tool
def data_quality_report():
    """检查数据质量，包括缺失值、重复行、字段类型"""
    df = load_current_data()

    missing_values = df.isnull().sum()
    missing_result = {
        col: int(count)
        for col, count in missing_values.items()
        if count > 0
    }

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": missing_result,
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }


@tool
def kpi_summary():
    """生成核心KPI总览"""
    df = load_current_data()
    sales_col = get_sales_column(df)

    if sales_col is None:
        return "没有找到销售额字段。请确保CSV包含 sales、销售额、amount 或 revenue 字段。"

    total_sales = df[sales_col].sum()
    average_sales = df[sales_col].mean()
    max_sale = df[sales_col].max()
    min_sale = df[sales_col].min()

    result = {
        "sales_column": sales_col,
        "row_count": len(df),
        "total_sales": safe_number(total_sales),
        "average_sales": safe_number(average_sales),
        "max_single_sale": safe_number(max_sale),
        "min_single_sale": safe_number(min_sale)
    }

    profit_col = get_profit_column(df)
    if profit_col is not None:
        total_profit = df[profit_col].sum()
        result["total_profit"] = safe_number(total_profit)

        if total_sales != 0:
            result["profit_margin"] = str(round(float(total_profit / total_sales * 100), 2)) + "%"

    return result


@tool
def numeric_summary():
    """查看所有数值字段的统计摘要"""
    df = load_current_data()
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return "没有找到数值型字段。"

    summary = numeric_df.describe().round(2)

    return summary.to_dict()


@tool
def region_sales_summary():
    """按区域汇总销售额"""
    df = load_current_data()
    region_col = get_region_column(df)
    sales_col = get_sales_column(df)

    if region_col is None:
        return "没有找到区域字段。请确保CSV包含 region、区域 或 地区 字段。"

    if sales_col is None:
        return "没有找到销售额字段。请确保CSV包含 sales、销售额、amount 或 revenue 字段。"

    result = (
        df.groupby(region_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
    )

    result[sales_col] = result[sales_col].apply(safe_number)

    return result.to_dict(orient="records")


@tool
def best_region():
    """找出销售额最高的区域"""
    df = load_current_data()
    region_col = get_region_column(df)
    sales_col = get_sales_column(df)

    if region_col is None or sales_col is None:
        return "需要区域字段和销售额字段才能分析最高销售额区域。"

    result = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    best_name = result.index[0]
    best_value = result.iloc[0]

    return {
        "best_region": best_name,
        "sales": safe_number(best_value)
    }


@tool
def worst_region():
    """找出销售额最低的区域"""
    df = load_current_data()
    region_col = get_region_column(df)
    sales_col = get_sales_column(df)

    if region_col is None or sales_col is None:
        return "需要区域字段和销售额字段才能分析最低销售额区域。"

    result = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=True)
    )

    worst_name = result.index[0]
    worst_value = result.iloc[0]

    return {
        "worst_region": worst_name,
        "sales": safe_number(worst_value)
    }


@tool
def category_sales_summary():
    """按品类汇总销售额"""
    df = load_current_data()
    category_col = get_category_column(df)
    sales_col = get_sales_column(df)

    if category_col is None:
        return "没有找到品类字段。请确保CSV包含 category、品类 或 类别 字段。"

    if sales_col is None:
        return "没有找到销售额字段。"

    result = (
        df.groupby(category_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
    )

    result[sales_col] = result[sales_col].apply(safe_number)

    return result.to_dict(orient="records")


@tool
def top_products():
    """找出销售额最高的产品排名"""
    df = load_current_data()
    product_col = get_product_column(df)
    sales_col = get_sales_column(df)

    if product_col is None:
        return "没有找到产品字段。请确保CSV包含 product、产品 或 sku 字段。"

    if sales_col is None:
        return "没有找到销售额字段。"

    result = (
        df.groupby(product_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
        .head(5)
    )

    result[sales_col] = result[sales_col].apply(safe_number)

    return result.to_dict(orient="records")


@tool
def channel_sales_summary():
    """按渠道汇总销售额"""
    df = load_current_data()
    channel_col = get_channel_column(df)
    sales_col = get_sales_column(df)

    if channel_col is None:
        return "没有找到渠道字段。请确保CSV包含 channel 或 渠道 字段。"

    if sales_col is None:
        return "没有找到销售额字段。"

    result = (
        df.groupby(channel_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
    )

    result[sales_col] = result[sales_col].apply(safe_number)

    return result.to_dict(orient="records")


@tool
def monthly_sales_trend():
    """按月份分析销售趋势"""
    df = load_current_data()
    date_col = get_date_column(df)
    sales_col = get_sales_column(df)

    if date_col is None:
        return "没有找到日期字段。请确保CSV包含 date、日期、order_date 或 订单日期 字段。"

    if sales_col is None:
        return "没有找到销售额字段。"

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    if df.empty:
        return "日期字段无法解析，请检查日期格式。"

    df["month"] = df[date_col].dt.to_period("M").astype(str)

    result = (
        df.groupby("month")[sales_col]
        .sum()
        .reset_index()
        .sort_values("month")
    )

    result[sales_col] = result[sales_col].apply(safe_number)

    return result.to_dict(orient="records")


@tool
def profit_analysis():
    """分析利润和利润率"""
    df = load_current_data()
    sales_col = get_sales_column(df)
    profit_col = get_profit_column(df)
    cost_col = get_cost_column(df)

    if sales_col is None:
        return "没有找到销售额字段。"

    if profit_col is None and cost_col is None:
        return "没有找到利润或成本字段。请确保CSV包含 profit、利润、cost 或 成本 字段。"

    total_sales = df[sales_col].sum()

    if profit_col is not None:
        total_profit = df[profit_col].sum()
    else:
        total_cost = df[cost_col].sum()
        total_profit = total_sales - total_cost

    margin = 0
    if total_sales != 0:
        margin = total_profit / total_sales * 100

    return {
        "total_sales": safe_number(total_sales),
        "total_profit": safe_number(total_profit),
        "profit_margin": str(round(float(margin), 2)) + "%"
    }


@tool
def detect_sales_outliers():
    """检测销售额异常值"""
    df = load_current_data()
    sales_col = get_sales_column(df)

    if sales_col is None:
        return "没有找到销售额字段。"

    q1 = df[sales_col].quantile(0.25)
    q3 = df[sales_col].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[
        (df[sales_col] < lower_bound) |
        (df[sales_col] > upper_bound)
    ]

    return {
        "lower_bound": safe_number(lower_bound),
        "upper_bound": safe_number(upper_bound),
        "outlier_count": len(outliers),
        "outliers_preview": outliers.head(10).to_dict(orient="records")
    }


@tool
def create_region_sales_chart():
    """生成区域销售额柱状图"""
    ensure_report_dirs()
    setup_chinese_font()

    df = load_current_data()
    region_col = get_region_column(df)
    sales_col = get_sales_column(df)

    if region_col is None or sales_col is None:
        return "需要区域字段和销售额字段才能生成区域销售图。"

    result = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    chart_path = f"{CHART_DIR}/region_sales.png"

    plt.figure(figsize=(8, 5))
    result.plot(kind="bar")
    plt.title("区域销售额汇总")
    plt.xlabel("区域")
    plt.ylabel("销售额")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return {
        "message": "区域销售额柱状图已生成。",
        "chart_path": chart_path
    }


@tool
def create_category_sales_chart():
    """生成品类销售额柱状图"""
    ensure_report_dirs()
    setup_chinese_font()

    df = load_current_data()
    category_col = get_category_column(df)
    sales_col = get_sales_column(df)

    if category_col is None or sales_col is None:
        return "需要品类字段和销售额字段才能生成品类销售图。"

    result = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    chart_path = f"{CHART_DIR}/category_sales.png"

    plt.figure(figsize=(8, 5))
    result.plot(kind="bar")
    plt.title("品类销售额汇总")
    plt.xlabel("品类")
    plt.ylabel("销售额")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return {
        "message": "品类销售额柱状图已生成。",
        "chart_path": chart_path
    }


@tool
def create_channel_sales_chart():
    """生成渠道销售额柱状图"""
    ensure_report_dirs()
    setup_chinese_font()

    df = load_current_data()
    channel_col = get_channel_column(df)
    sales_col = get_sales_column(df)

    if channel_col is None or sales_col is None:
        return "需要渠道字段和销售额字段才能生成渠道销售图。"

    result = (
        df.groupby(channel_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    chart_path = f"{CHART_DIR}/channel_sales.png"

    plt.figure(figsize=(8, 5))
    result.plot(kind="bar")
    plt.title("渠道销售额汇总")
    plt.xlabel("渠道")
    plt.ylabel("销售额")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return {
        "message": "渠道销售额柱状图已生成。",
        "chart_path": chart_path
    }


@tool
def create_monthly_sales_trend_chart():
    """生成月度销售趋势折线图"""
    ensure_report_dirs()
    setup_chinese_font()

    df = load_current_data()
    date_col = get_date_column(df)
    sales_col = get_sales_column(df)

    if date_col is None or sales_col is None:
        return "需要日期字段和销售额字段才能生成月度趋势图。"

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    if df.empty:
        return "日期字段无法解析，无法生成月度趋势图。"

    df["month"] = df[date_col].dt.to_period("M").astype(str)

    result = (
        df.groupby("month")[sales_col]
        .sum()
        .sort_index()
    )

    chart_path = f"{CHART_DIR}/monthly_sales_trend.png"

    plt.figure(figsize=(9, 5))
    result.plot(kind="line", marker="o")
    plt.title("月度销售趋势")
    plt.xlabel("月份")
    plt.ylabel("销售额")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return {
        "message": "月度销售趋势图已生成。",
        "chart_path": chart_path
    }


@tool
def create_all_charts():
    """一次性生成所有可用图表"""
    results = []

    results.append(create_region_sales_chart.invoke({}))
    results.append(create_category_sales_chart.invoke({}))
    results.append(create_channel_sales_chart.invoke({}))
    results.append(create_monthly_sales_trend_chart.invoke({}))

    return results

@tool
def generate_markdown_report():
    """生成专业Markdown格式的数据分析报告，并自动生成图表和业务洞察"""
    ensure_report_dirs()

    kpi = kpi_summary.invoke({})
    quality = data_quality_report.invoke({})
    numeric = numeric_summary.invoke({})
    region = region_sales_summary.invoke({})
    category = category_sales_summary.invoke({})
    channel = channel_sales_summary.invoke({})
    trend = monthly_sales_trend.invoke({})
    profit = profit_analysis.invoke({})
    outliers = detect_sales_outliers.invoke({})
    charts = create_all_charts.invoke({})

    insights = generate_business_insights(
        kpi=kpi,
        region=region,
        category=category,
        channel=channel,
        trend=trend,
        profit=profit,
        outliers=outliers
    )

    recommendations = generate_business_recommendations(
        kpi=kpi,
        region=region,
        category=category,
        channel=channel,
        trend=trend,
        profit=profit,
        outliers=outliers
    )

    kpi_table = markdown_table_from_dict(kpi)
    quality_table = markdown_table_from_dict(quality)
    region_table = markdown_table_from_records(region)
    category_table = markdown_table_from_records(category)
    channel_table = markdown_table_from_records(channel)
    trend_table = markdown_table_from_records(trend)
    profit_table = markdown_table_from_dict(profit)
    outlier_table = markdown_table_from_dict(outliers)
    charts_table = markdown_table_from_records(charts)

    insight_text = "\n".join([f"- {item}" for item in insights])
    recommendation_text = "\n".join([f"- {item}" for item in recommendations])

    content_parts = []

    content_parts.append("# InsightAgent 数据分析报告")
    content_parts.append("")
    content_parts.append("## 一、执行摘要")
    content_parts.append("")
    content_parts.append(
        "本报告基于用户上传的 CSV 数据自动生成，覆盖核心 KPI、数据质量、区域表现、品类表现、渠道表现、月度趋势、利润表现和异常检测等分析维度。"
    )
    content_parts.append("")
    content_parts.append("### 关键业务洞察")
    content_parts.append("")
    content_parts.append(insight_text)
    content_parts.append("")
    content_parts.append("### 初步业务建议")
    content_parts.append("")
    content_parts.append(recommendation_text)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 二、核心 KPI")
    content_parts.append("")
    content_parts.append(kpi_table)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 三、数据质量检查")
    content_parts.append("")
    content_parts.append(quality_table)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 四、数值字段统计摘要")
    content_parts.append("")
    content_parts.append("以下为所有数值字段的统计摘要，包括 count、mean、std、min、max 等指标。")
    content_parts.append("")
    content_parts.append("```text")
    content_parts.append(str(numeric))
    content_parts.append("```")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 五、区域销售分析")
    content_parts.append("")
    content_parts.append(region_table)
    content_parts.append("")
    content_parts.append("图表路径：reports/charts/region_sales.png")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 六、品类销售分析")
    content_parts.append("")
    content_parts.append(category_table)
    content_parts.append("")
    content_parts.append("图表路径：reports/charts/category_sales.png")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 七、渠道销售分析")
    content_parts.append("")
    content_parts.append(channel_table)
    content_parts.append("")
    content_parts.append("图表路径：reports/charts/channel_sales.png")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 八、月度销售趋势")
    content_parts.append("")
    content_parts.append(trend_table)
    content_parts.append("")
    content_parts.append("图表路径：reports/charts/monthly_sales_trend.png")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 九、利润分析")
    content_parts.append("")
    content_parts.append(profit_table)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 十、异常销售额检测")
    content_parts.append("")
    content_parts.append(outlier_table)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 十一、图表文件")
    content_parts.append("")
    content_parts.append(charts_table)
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content_parts.append("## 十二、结论")
    content_parts.append("")
    content_parts.append(
        "本次分析显示，当前数据已经具备基础经营分析价值。InsightAgent 已完成从数据读取、指标计算、趋势分析、异常检测到报告生成的自动化流程。"
    )
    content_parts.append("")
    content_parts.append("后续可继续扩展：")
    content_parts.append("")
    content_parts.append("- 接入大模型进行自然语言意图识别；")
    content_parts.append("- 接入 Blazor 前端，实现上传、提问、图表预览和报告下载；")
    content_parts.append("- 支持 Excel 文件；")
    content_parts.append("- 增加客户、门店、销售人员等更细粒度分析；")
    content_parts.append("- 增加 PDF 报告导出能力。")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")
    content_parts.append("报告由 InsightAgent 自动生成。")

    content = "\n".join(content_parts)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(content)

    return {
        "message": "专业分析报告和图表已生成。",
        "report_path": REPORT_PATH,
        "chart_dir": CHART_DIR
    }