from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Insurance Tech Audit Analytics Lab",
    page_icon="🛡️",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
CURATED = ROOT / "data" / "curated"
REPORT_DATE = pd.Timestamp("2026-04-07")

COLOR_SEQ = [
    "#7FB3FF",
    "#4F8BFF",
    "#9CC8FF",
    "#6A5AE0",
    "#5CC8A1",
    "#F5A623",
    "#F87171",
]

px.defaults.template = "plotly_dark"


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 1.2rem;
        max-width: 1500px;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.8rem 1rem;
        border-radius: 0.9rem;
    }
    .section-box {
        background: rgba(91, 141, 239, 0.12);
        border: 1px solid rgba(91, 141, 239, 0.18);
        border-radius: 0.9rem;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
    }
    .small-note {
        color: #9CA3AF;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    path = CURATED / filename
    if not path.exists():
        st.error(f"Missing file: {path}")
        st.stop()
    return pd.read_csv(path)


def metric_row(items: list[dict]) -> None:
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            st.metric(item["label"], item["value"])
            if item.get("caption"):
                st.markdown(
                    f"<div class='small-note'>{item['caption']}</div>",
                    unsafe_allow_html=True,
                )


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def format_fig(fig, height=420):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
    )
    return fig


def empty_message(label: str) -> None:
    st.warning(f"No rows match the current filters for {label}.")


audit_overview = load_csv("audit_overview_summary.csv")
iam_summary = load_csv("iam_review_summary.csv")
iam_detail = load_csv("iam_detail.csv")
vulnerability_summary = load_csv("vulnerability_summary.csv")
vulnerability_detail = load_csv("vulnerability_detail.csv")
cloud_summary = load_csv("cloud_infra_posture_summary.csv")
cloud_detail = load_csv("cloud_infra_detail.csv")
resilience_detail = load_csv("resilience_detail.csv")


# -------------------- PREP --------------------
audit_overview["share_pct"] = (
    audit_overview["open_findings_count"] / audit_overview["open_findings_count"].sum() * 100
).round(1)

vulnerability_detail["sla_due_date"] = pd.to_datetime(
    vulnerability_detail["sla_due_date"], errors="coerce"
)
vulnerability_detail["overdue_days"] = (
    REPORT_DATE - vulnerability_detail["sla_due_date"]
).dt.days.clip(lower=0)

vulnerability_detail["aging_bucket"] = pd.cut(
    vulnerability_detail["overdue_days"],
    bins=[-1, 7, 30, 99999],
    labels=["0-7 days overdue", "8-30 days overdue", "31+ days overdue"],
)

if "department" in iam_detail.columns:
    iam_detail["department"] = iam_detail["department"].fillna("").astype(str)

if "severity" in iam_detail.columns:
    iam_detail["severity"] = iam_detail["severity"].fillna("Unknown")

if "severity" in cloud_detail.columns:
    cloud_detail["severity"] = cloud_detail["severity"].fillna("Unknown")


# -------------------- HEADER --------------------
st.title("Insurance Tech Audit Analytics Lab")
st.caption("Synthetic technology audit engagement for NorthStar Life Insurance")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select page",
        [
            "Audit Overview",
            "IAM Review",
            "Vulnerability Management",
            "Cloud & Infrastructure",
            "Resilience",
        ],
    )

    st.divider()
    st.markdown("**Dashboard notes**")
    st.write(
        "This dashboard is powered by curated CSV outputs generated from synthetic audit evidence, "
        "SQL control tests, and QA-checked reporting tables."
    )


# ==================== PAGE 1 ====================
if page == "Audit Overview":
    st.subheader("Technology Audit Overview")
    st.markdown(
        "<div class='section-box'>Executive summary of open control issues across the core technology risk domains.</div>",
        unsafe_allow_html=True,
    )

    total_open_findings = int(audit_overview["open_findings_count"].sum())
    domain_count = int(audit_overview["domain"].nunique())
    highest_risk_domain = audit_overview.sort_values(
        ["open_findings_count", "domain"], ascending=[False, True]
    ).iloc[0]["domain"]
    avg_findings = round(total_open_findings / domain_count, 2) if domain_count else 0

    metric_row(
        [
            {"label": "Total Open Findings", "value": total_open_findings, "caption": "Across all included control domains"},
            {"label": "Control Domains", "value": domain_count, "caption": "Domains represented in the current issue set"},
            {"label": "Highest-Risk Domain", "value": highest_risk_domain, "caption": "Domain with the largest issue volume"},
            {"label": "Average Findings / Domain", "value": avg_findings, "caption": "Average issue load across domains"},
        ]
    )

    left, right = st.columns([1.6, 1])

    with left:
        chart_df = audit_overview.sort_values("open_findings_count", ascending=True)
        fig = px.bar(
            chart_df,
            x="open_findings_count",
            y="domain",
            orientation="h",
            text="open_findings_count",
            color="domain",
            color_discrete_sequence=COLOR_SEQ,
            title="Open Findings by Domain",
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False, xaxis_title="Open Findings", yaxis_title="")
        st.plotly_chart(format_fig(fig, 500), use_container_width=True)

    with right:
        donut = px.pie(
            audit_overview,
            names="domain",
            values="open_findings_count",
            hole=0.55,
            color="domain",
            color_discrete_sequence=COLOR_SEQ,
            title="Domain Share of Open Findings",
        )
        donut.update_traces(textinfo="percent+label")
        st.plotly_chart(format_fig(donut, 500), use_container_width=True)

    st.markdown("**Overview Detail**")
    overview_display = audit_overview.sort_values("open_findings_count", ascending=False).reset_index(drop=True)
    st.dataframe(overview_display, use_container_width=True, hide_index=True)
    st.download_button(
        "Download overview CSV",
        data=csv_bytes(overview_display),
        file_name="audit_overview_summary.csv",
        mime="text/csv",
    )


# ==================== PAGE 2 ====================
elif page == "IAM Review":
    st.subheader("Identity & Access Management Review")
    st.markdown(
        "<div class='section-box'>Highlights MFA gaps, dormant privileged accounts, service-account ownership issues, and weak access-governance patterns.</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.divider()
        st.markdown("**IAM filters**")
        severity_options = ["All"] + sorted(iam_detail["severity"].dropna().unique().tolist())
        department_options = ["All"] + sorted(
            [x for x in iam_detail["department"].dropna().unique().tolist() if str(x).strip() != ""]
        )
        issue_type_options = ["All"] + sorted(iam_detail["issue_type"].dropna().unique().tolist())

        selected_severity = st.selectbox("Severity", severity_options, key="iam_severity")
        selected_department = st.selectbox("Department", department_options, key="iam_department")
        selected_issue_type = st.selectbox("Issue Type", issue_type_options, key="iam_issue_type")

    iam_filtered = iam_detail.copy()
    if selected_severity != "All":
        iam_filtered = iam_filtered[iam_filtered["severity"] == selected_severity]
    if selected_department != "All":
        iam_filtered = iam_filtered[iam_filtered["department"] == selected_department]
    if selected_issue_type != "All":
        iam_filtered = iam_filtered[iam_filtered["issue_type"] == selected_issue_type]

    metric_row(
        [
            {"label": "IAM Issue Rows", "value": int(len(iam_filtered)), "caption": "Filtered exception rows"},
            {"label": "High Severity Issues", "value": int((iam_filtered["severity"] == "High").sum()), "caption": "Rows currently rated High"},
            {"label": "Distinct Issue Types", "value": int(iam_filtered["issue_type"].nunique()) if not iam_filtered.empty else 0, "caption": "Unique IAM exception categories"},
            {"label": "Impacted Accounts", "value": int(iam_filtered["user_or_account"].nunique()) if not iam_filtered.empty else 0, "caption": "Distinct users or accounts impacted"},
        ]
    )

    left, right = st.columns([1.35, 1])

    with left:
        if iam_filtered.empty:
            empty_message("IAM")
        else:
            issue_counts = (
                iam_filtered.groupby(["issue_type", "severity"], as_index=False)
                .size()
                .rename(columns={"size": "issue_count"})
            )
            fig = px.bar(
                issue_counts,
                x="issue_count",
                y="issue_type",
                color="severity",
                orientation="h",
                barmode="stack",
                text="issue_count",
                color_discrete_sequence=COLOR_SEQ,
                title="IAM Exceptions by Issue Type and Severity",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(xaxis_title="Issue Count", yaxis_title="")
            st.plotly_chart(format_fig(fig, 440), use_container_width=True)

    with right:
        if iam_filtered.empty:
            empty_message("IAM heatmap")
        else:
            heatmap_df = iam_filtered.copy()
            heatmap_df = heatmap_df[heatmap_df["department"].astype(str).str.strip() != ""]
            if heatmap_df.empty:
                st.info("No department-level rows available for the current IAM filters.")
            else:
                pivot = pd.pivot_table(
                    heatmap_df,
                    index="department",
                    columns="issue_type",
                    values="user_or_account",
                    aggfunc="count",
                    fill_value=0,
                )
                heatmap = px.imshow(
                    pivot,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Blues",
                    title="Department × IAM Issue Type Heatmap",
                )
                st.plotly_chart(format_fig(heatmap, 440), use_container_width=True)

    lower_left, lower_right = st.columns([1.35, 1])

    with lower_left:
        st.markdown("**IAM Exception Detail**")
        iam_display = iam_filtered.sort_values(
            ["severity", "issue_type", "department", "user_or_account"],
            ascending=[True, True, True, True],
        ).reset_index(drop=True)
        st.dataframe(iam_display, use_container_width=True, hide_index=True)
        st.download_button(
            "Download IAM detail CSV",
            data=csv_bytes(iam_display),
            file_name="iam_detail_filtered.csv",
            mime="text/csv",
        )

    with lower_right:
        severity_mix = (
            iam_filtered.groupby("severity", as_index=False)
            .size()
            .rename(columns={"size": "row_count"})
            .sort_values("row_count", ascending=False)
        )
        if not severity_mix.empty:
            donut = px.pie(
                severity_mix,
                names="severity",
                values="row_count",
                hole=0.6,
                color="severity",
                color_discrete_sequence=COLOR_SEQ,
                title="IAM Severity Mix",
            )
            donut.update_traces(textinfo="percent+label")
            st.plotly_chart(format_fig(donut, 280), use_container_width=True)

        st.markdown("**IAM Summary Metrics**")
        st.dataframe(iam_summary, use_container_width=True, hide_index=True)


# ==================== PAGE 3 ====================
elif page == "Vulnerability Management":
    st.subheader("Vulnerability Management")
    st.markdown(
        "<div class='section-box'>Shows overdue high-risk findings, KEV exposure, aging concentration, and business-service impact.</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.divider()
        st.markdown("**Vulnerability filters**")
        sev_options = ["All"] + sorted(vulnerability_detail["severity"].dropna().unique().tolist())
        kev_options = ["All"] + sorted(vulnerability_detail["kev_listed"].dropna().unique().tolist())
        internet_options = ["All"] + sorted(vulnerability_detail["internet_facing"].dropna().unique().tolist())
        service_options = ["All"] + sorted(vulnerability_detail["business_service"].dropna().unique().tolist())

        vul_sev = st.selectbox("Severity", sev_options, key="vul_sev")
        vul_kev = st.selectbox("KEV Listed", kev_options, key="vul_kev")
        vul_internet = st.selectbox("Internet Facing", internet_options, key="vul_internet")
        vul_service = st.selectbox("Business Service", service_options, key="vul_service")

    vul_filtered = vulnerability_detail.copy()
    if vul_sev != "All":
        vul_filtered = vul_filtered[vul_filtered["severity"] == vul_sev]
    if vul_kev != "All":
        vul_filtered = vul_filtered[vul_filtered["kev_listed"] == vul_kev]
    if vul_internet != "All":
        vul_filtered = vul_filtered[vul_filtered["internet_facing"] == vul_internet]
    if vul_service != "All":
        vul_filtered = vul_filtered[vul_filtered["business_service"] == vul_service]

    median_overdue = int(vul_filtered["overdue_days"].median()) if not vul_filtered.empty else 0

    metric_row(
        [
            {"label": "Open High / Critical Findings", "value": int(len(vul_filtered)), "caption": "Filtered open findings"},
            {"label": "Critical Findings", "value": int((vul_filtered["severity"] == "Critical").sum()), "caption": "Rows classified as Critical"},
            {"label": "KEV-Listed Findings", "value": int((vul_filtered["kev_listed"] == "Yes").sum()), "caption": "Known Exploited Vulnerability flags"},
            {"label": "Median Overdue Days", "value": median_overdue, "caption": "Median days past SLA due date"},
        ]
    )

    upper_left, upper_right = st.columns([1.35, 1])

    with upper_left:
        if vul_filtered.empty:
            empty_message("Vulnerability")
        else:
            service_severity = (
                vul_filtered.groupby(["business_service", "severity"], as_index=False)
                .size()
                .rename(columns={"size": "finding_count"})
            )
            fig = px.bar(
                service_severity,
                x="finding_count",
                y="business_service",
                color="severity",
                orientation="h",
                barmode="stack",
                text="finding_count",
                color_discrete_sequence=COLOR_SEQ,
                title="Findings by Business Service and Severity",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(xaxis_title="Finding Count", yaxis_title="")
            st.plotly_chart(format_fig(fig, 430), use_container_width=True)

    with upper_right:
        if vul_filtered.empty:
            empty_message("Vulnerability aging")
        else:
            aging = (
                vul_filtered.groupby("aging_bucket", as_index=False)
                .size()
                .rename(columns={"size": "row_count"})
            )
            aging["aging_bucket"] = aging["aging_bucket"].astype(str)
            fig = px.bar(
                aging,
                x="aging_bucket",
                y="row_count",
                text="row_count",
                color="aging_bucket",
                color_discrete_sequence=COLOR_SEQ,
                title="Overdue Aging Buckets",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Finding Count")
            st.plotly_chart(format_fig(fig, 430), use_container_width=True)

    lower_left, lower_right = st.columns([1.35, 1])

    with lower_left:
        st.markdown("**Vulnerability Detail**")
        vul_display = vul_filtered.sort_values(
            ["severity", "kev_listed", "overdue_days", "business_service"],
            ascending=[True, False, False, True],
        ).reset_index(drop=True)
        st.dataframe(vul_display, use_container_width=True, hide_index=True)
        st.download_button(
            "Download vulnerability detail CSV",
            data=csv_bytes(vul_display),
            file_name="vulnerability_detail_filtered.csv",
            mime="text/csv",
        )

    with lower_right:
        if not vul_filtered.empty:
            crit_mix = (
                vul_filtered.groupby("business_criticality", as_index=False)
                .size()
                .rename(columns={"size": "row_count"})
            )
            donut = px.pie(
                crit_mix,
                names="business_criticality",
                values="row_count",
                hole=0.6,
                color="business_criticality",
                color_discrete_sequence=COLOR_SEQ,
                title="Business Criticality Mix",
            )
            donut.update_traces(textinfo="percent+label")
            st.plotly_chart(format_fig(donut, 290), use_container_width=True)

        st.markdown("**Vulnerability Summary Metrics**")
        st.dataframe(vulnerability_summary, use_container_width=True, hide_index=True)


# ==================== PAGE 4 ====================
elif page == "Cloud & Infrastructure":
    st.subheader("Cloud & Infrastructure Posture")
    st.markdown(
        "<div class='section-box'>Covers public cloud exposure, permissive network rules, and unsupported operating-system risk.</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.divider()
        st.markdown("**Cloud / infrastructure filters**")
        issue_options = ["All"] + sorted(cloud_detail["issue_type"].dropna().unique().tolist())
        platform_options = ["All"] + sorted(cloud_detail["platform_or_environment"].dropna().unique().tolist())
        severity_options = ["All"] + sorted(cloud_detail["severity"].dropna().unique().tolist())

        selected_issue = st.selectbox("Issue Type", issue_options, key="cloud_issue")
        selected_platform = st.selectbox("Platform / Environment", platform_options, key="cloud_platform")
        selected_severity = st.selectbox("Severity", severity_options, key="cloud_severity")

    cloud_filtered = cloud_detail.copy()
    if selected_issue != "All":
        cloud_filtered = cloud_filtered[cloud_filtered["issue_type"] == selected_issue]
    if selected_platform != "All":
        cloud_filtered = cloud_filtered[cloud_filtered["platform_or_environment"] == selected_platform]
    if selected_severity != "All":
        cloud_filtered = cloud_filtered[cloud_filtered["severity"] == selected_severity]

    metric_row(
        [
            {"label": "Cloud / Infra Issue Rows", "value": int(len(cloud_filtered)), "caption": "Filtered issue rows"},
            {"label": "High Severity Rows", "value": int((cloud_filtered["severity"] == "High").sum()), "caption": "Rows currently rated High"},
            {"label": "Distinct Issue Types", "value": int(cloud_filtered["issue_type"].nunique()) if not cloud_filtered.empty else 0, "caption": "Unique issue categories"},
            {"label": "Platforms / Environments", "value": int(cloud_filtered["platform_or_environment"].nunique()) if not cloud_filtered.empty else 0, "caption": "Distinct environments represented"},
        ]
    )

    upper_left, upper_right = st.columns([1.35, 1])

    with upper_left:
        if cloud_filtered.empty:
            empty_message("Cloud & Infrastructure")
        else:
            issue_platform = (
                cloud_filtered.groupby(["issue_type", "platform_or_environment"], as_index=False)
                .size()
                .rename(columns={"size": "issue_count"})
            )
            fig = px.bar(
                issue_platform,
                x="issue_count",
                y="issue_type",
                color="platform_or_environment",
                orientation="h",
                barmode="group",
                text="issue_count",
                color_discrete_sequence=COLOR_SEQ,
                title="Issue Type by Platform / Environment",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(xaxis_title="Issue Count", yaxis_title="")
            st.plotly_chart(format_fig(fig, 430), use_container_width=True)

    with upper_right:
        if not cloud_filtered.empty:
            sev_mix = (
                cloud_filtered.groupby("severity", as_index=False)
                .size()
                .rename(columns={"size": "row_count"})
            )
            donut = px.pie(
                sev_mix,
                names="severity",
                values="row_count",
                hole=0.6,
                color="severity",
                color_discrete_sequence=COLOR_SEQ,
                title="Severity Mix",
            )
            donut.update_traces(textinfo="percent+label")
            st.plotly_chart(format_fig(donut, 430), use_container_width=True)

    lower_left, lower_right = st.columns([1.35, 1])

    with lower_left:
        st.markdown("**Cloud / Infrastructure Detail**")
        cloud_display = cloud_filtered.sort_values(
            ["severity", "issue_type", "platform_or_environment", "resource_or_rule_id"],
            ascending=[True, True, True, True],
        ).reset_index(drop=True)
        st.dataframe(cloud_display, use_container_width=True, hide_index=True)
        st.download_button(
            "Download cloud / infra detail CSV",
            data=csv_bytes(cloud_display),
            file_name="cloud_infra_detail_filtered.csv",
            mime="text/csv",
        )

    with lower_right:
        st.markdown("**Cloud / Infrastructure Summary Metrics**")
        st.dataframe(cloud_summary, use_container_width=True, hide_index=True)

        if not cloud_filtered.empty:
            platform_mix = (
                cloud_filtered.groupby("platform_or_environment", as_index=False)
                .size()
                .rename(columns={"size": "row_count"})
            )
            fig = px.bar(
                platform_mix,
                x="platform_or_environment",
                y="row_count",
                text="row_count",
                color="platform_or_environment",
                color_discrete_sequence=COLOR_SEQ,
                title="Platform / Environment Mix",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Issue Count")
            st.plotly_chart(format_fig(fig, 290), use_container_width=True)


# ==================== PAGE 5 ====================
elif page == "Resilience":
    st.subheader("Resilience")
    st.markdown(
        "<div class='section-box'>Focuses on failed backup / disaster-recovery tests that still lack retest evidence.</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.divider()
        st.markdown("**Resilience filters**")
        crit_options = ["All"] + sorted(resilience_detail["business_criticality"].dropna().unique().tolist())
        test_options = ["All"] + sorted(resilience_detail["test_type"].dropna().unique().tolist())

        selected_crit = st.selectbox("Business Criticality", crit_options, key="res_crit")
        selected_test = st.selectbox("Test Type", test_options, key="res_test")

    res_filtered = resilience_detail.copy()
    if selected_crit != "All":
        res_filtered = res_filtered[res_filtered["business_criticality"] == selected_crit]
    if selected_test != "All":
        res_filtered = res_filtered[res_filtered["test_type"] == selected_test]

    metric_row(
        [
            {"label": "Failed Tests Without Retest", "value": int(len(res_filtered)), "caption": "Filtered failed test rows"},
            {"label": "Impacted Assets", "value": int(res_filtered["asset_id"].nunique()) if not res_filtered.empty else 0, "caption": "Distinct assets impacted"},
            {"label": "Distinct Services", "value": int(res_filtered["business_service"].nunique()) if not res_filtered.empty else 0, "caption": "Business services represented"},
            {"label": "Critical Assets", "value": int((res_filtered["business_criticality"] == "Critical").sum()) if not res_filtered.empty else 0, "caption": "Rows affecting critical assets"},
        ]
    )

    left, right = st.columns([1.35, 1])

    with left:
        if res_filtered.empty:
            empty_message("Resilience")
        else:
            service_counts = (
                res_filtered.groupby(["business_service", "business_criticality"], as_index=False)
                .size()
                .rename(columns={"size": "failed_test_count"})
            )
            fig = px.bar(
                service_counts,
                x="failed_test_count",
                y="business_service",
                color="business_criticality",
                orientation="h",
                barmode="group",
                text="failed_test_count",
                color_discrete_sequence=COLOR_SEQ,
                title="Failed Tests Without Retest by Business Service",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(xaxis_title="Failed Test Count", yaxis_title="")
            st.plotly_chart(format_fig(fig, 430), use_container_width=True)

    with right:
        if not res_filtered.empty:
            type_mix = (
                res_filtered.groupby("test_type", as_index=False)
                .size()
                .rename(columns={"size": "row_count"})
            )
            donut = px.pie(
                type_mix,
                names="test_type",
                values="row_count",
                hole=0.6,
                color="test_type",
                color_discrete_sequence=COLOR_SEQ,
                title="Test Type Mix",
            )
            donut.update_traces(textinfo="percent+label")
            st.plotly_chart(format_fig(donut, 430), use_container_width=True)

    st.markdown("**Resilience Detail**")
    res_display = res_filtered.sort_values(
        ["business_criticality", "business_service", "asset_name"],
        ascending=[True, True, True],
    ).reset_index(drop=True)
    st.dataframe(res_display, use_container_width=True, hide_index=True)
    st.download_button(
        "Download resilience detail CSV",
        data=csv_bytes(res_display),
        file_name="resilience_detail_filtered.csv",
        mime="text/csv",
    )