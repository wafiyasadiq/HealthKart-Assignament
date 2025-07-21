#engagement metrics
engagement_metric = """SELECT 
  influencer_id,
  platform,
  COUNT(*) AS total_posts,
  SUM(reach) AS total_reach,
  SUM(likes) AS total_likes,
  SUM(comments) AS total_comments
FROM posts
GROUP BY influencer_id, platform;"""

#conversion metrics
conversion_metric="""SELECT 
  influencer_id,
  COUNT(DISTINCT user_id) AS unique_buyers,
  SUM(orders) AS total_orders,
  SUM(revenue) AS total_revenue
FROM tracking_data
GROUP BY influencer_id;"""

#ROAS Calculation
roas_calculation="""SELECT 
  p.influencer_id,
  SUM(t.revenue) / SUM(p.total_payout) AS roas
FROM payouts p
JOIN tracking_data t ON p.influencer_id = t.influencer_id
GROUP BY p.influencer_id;"""

#Incremental ROAS Calculation
#Formula = (Revenue_with_campaign - Baseline_Revenue) / Spend
incremental_roas = """SELECT    
  t.influencer_id,   
  (SUM(t.revenue) - 0.5 * AVG(t.revenue)) / SUM(p.total_payout) AS incremental_roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
GROUP BY t.influencer_id;"""

#Filtering 
filter = """SELECT t.*, i.category, i.platform
FROM tracking_data t
JOIN influencers i ON t.influencer_id = i.id
WHERE t.product = 'HKVitals'
  AND i.category = 'Fitness'
  AND i.platform = 'Instagram';"""
  
#Top performing influencers by revenue
revenue_performer="""SELECT influencer_id, SUM(revenue) AS total_revenue
FROM tracking_data
GROUP BY influencer_id
ORDER BY total_revenue DESC
LIMIT 5;"""

#Top performing influencers by ROAS
top_roas_performer ="""SELECT 
    p.influencer_id,
    i.name AS influencer_name,
    SUM(t.revenue) AS total_revenue,
    SUM(p.total_payout) AS total_spend,
    ROUND(SUM(t.revenue) / SUM(p.total_payout), 2) AS roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
JOIN influencers i ON t.influencer_id = i.id
GROUP BY p.influencer_id, i.name
HAVING total_spend > 0
ORDER BY roas DESC
LIMIT 10;"""
  
#Best performing Influencers by Gender/Category
best_performer = """SELECT i.category, i.gender, SUM(t.revenue) AS total_revenue
FROM influencers i
JOIN tracking_data t ON i.id = t.influencer_id
GROUP BY i.category, i.gender
ORDER BY total_revenue DESC;"""
  
#Poor ROI giving influencers  
poor_roi= """SELECT p.influencer_id, SUM(t.revenue) / SUM(p.total_payout) AS roas
FROM payouts p
JOIN tracking_data t ON p.influencer_id = t.influencer_id
GROUP BY p.influencer_id
HAVING roas < 1;"""
 
 #ROAS based on platforms
roas_platform= """SELECT 
    t.source,
    p.influencer_id,
    i.name AS influencer_name,
    ROUND(SUM(t.revenue) / NULLIF(SUM(p.total_payout), 0), 2) AS roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
JOIN influencers i ON t.influencer_id = i.id
GROUP BY t.source, p.influencer_id, i.name
ORDER BY t.source, roas DESC;"""
 
 #ROAS Based on Months
roas_month = """SELECT 
    DATE_FORMAT(t.date, '%%Y-%%m') AS month,
    ROUND(SUM(t.revenue) / NULLIF(SUM(p.total_payout), 0), 2) AS monthly_roas
FROM 
    tracking_data t
JOIN 
    payouts p ON t.influencer_id = p.influencer_id
GROUP BY 
    DATE_FORMAT(t.date, '%%Y-%%m')
ORDER BY 
    month ASC;
"""

#Total Reach in terms of orders
total_reach = """SELECT SUM(reach) AS total_reach
FROM posts;"""

#total reach by influencers
total_influencer_reach = """SELECT 
    p.influencer_id,
    i.name AS influencer_name,
    SUM(p.reach) AS total_reach
FROM posts p
JOIN influencers i ON p.influencer_id = i.id
GROUP BY p.influencer_id, i.name
ORDER BY total_reach DESC;"""

#total reach by platform
total_platform_reach = """SELECT 
    p.platform,
    SUM(p.reach) AS total_reach
FROM posts p
GROUP BY p.platform
ORDER BY total_reach DESC;"""

import pandas as pd

def get_total_reach(engine):
    return pd.read_sql(total_reach, engine)

def get_top_influencers_by_roas(engine):
    return pd.read_sql(top_roas_performer, engine)

def get_monthly_trend(engine):
    return pd.read_sql(roas_month, engine)

def get_influencer_table(engine):
    return pd.read_sql(roas_calculation, engine)

def get_total_spend(engine):
    df = pd.read_sql("SELECT SUM(total_payout) AS total_spend FROM payouts;", engine)
    return df.iloc[0]["total_spend"] or 0

def get_total_revenue(engine):
    df = pd.read_sql("SELECT SUM(revenue) AS total_revenue FROM tracking_data;", engine)
    return df.iloc[0]["total_revenue"] or 0

def get_roi(engine):
    revenue = get_total_revenue(engine)
    spend = get_total_spend(engine)
    return revenue / spend if spend else 0

def get_incremental_roas(engine):
    df = pd.read_sql(incremental_roas, engine)
    return df["incremental_roas"].mean()

def get_brand_list(engine):
    df = pd.read_sql("SELECT DISTINCT product FROM tracking_data;", engine)
    return df["product"].dropna().tolist()

def get_platform_list(engine):
    df = pd.read_sql("SELECT DISTINCT platform FROM posts;", engine)
    return df["platform"].dropna().tolist()

def get_influencer_type_list(engine):
    df = pd.read_sql("SELECT DISTINCT category FROM influencers;", engine)
    return df["category"].dropna().tolist()

def get_main_data(engine, brand=None, platforms=None, types=None, dates=None):
    query = """
    SELECT 
        t.*, 
        i.name AS influencer_name, 
        i.category, 
        i.platform, 
        p.total_payout,
        po.reach
    FROM 
        tracking_data t
    JOIN 
        influencers i ON t.influencer_id = i.id
    LEFT JOIN 
        payouts p ON t.influencer_id = p.influencer_id
    LEFT JOIN 
        posts po ON t.influencer_id = po.influencer_id
    WHERE 
        1=1
    """

    if brand:
        query += f" AND t.product = '{brand}'"

    if platforms:
        platform_str = ",".join([f"'{p}'" for p in platforms])
        query += f" AND i.platform IN ({platform_str})"

    if types:
        type_str = ",".join([f"'{t}'" for t in types])
        query += f" AND i.category IN ({type_str})"

    if dates and len(dates) == 2:
        query += f" AND t.date BETWEEN '{dates[0]}' AND '{dates[1]}'"

    return pd.read_sql(query, engine)


def generate_text_insights(engine):
    df_top = get_top_influencers_by_roas(engine).head(1)
    df_low = pd.read_sql(poor_roi, engine).head(1)
    if not df_top.empty and not df_low.empty:
        return (f"**Top Performer:** {df_top.iloc[0]['influencer_name']} with ROAS {df_top.iloc[0]['roas']:.2f}\n\n"
                f"**Poor Performer:** Influencer ID {df_low.iloc[0]['influencer_id']} with ROAS < 1. Consider review.")
    return "No strong insights found."



