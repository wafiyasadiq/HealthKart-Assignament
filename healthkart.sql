use influencer_db;
show tables;
select * from influencers;
select * from tracking_data;
select * from payouts;
select * from posts;

#cleaning the data
DELETE FROM influencers
WHERE id NOT IN (
  SELECT * FROM (
    SELECT MIN(id)
    FROM influencers
    GROUP BY name
  ) AS keep_ids
);

DELETE FROM tracking_data
WHERE (influencer_id, campaign, user_id) NOT IN (
  SELECT * FROM (
    SELECT MIN(influencer_id), campaign, user_id
    FROM tracking_data
    GROUP BY influencer_id, campaign, user_id
  ) AS keep_ids
);

#replacing the null values
UPDATE payouts p
JOIN (
  SELECT influencer_id, COUNT(*) AS order_count
  FROM tracking_data
  GROUP BY influencer_id
) t ON p.influencer_id = t.influencer_id
SET p.orders = t.order_count
WHERE p.orders IS NULL;

#engagement metrics
SELECT 
  influencer_id,
  platform,
  COUNT(*) AS total_posts,
  SUM(reach) AS total_reach,
  SUM(likes) AS total_likes,
  SUM(comments) AS total_comments
FROM posts
GROUP BY influencer_id, platform;

#conversion metrics
SELECT 
  influencer_id,
  COUNT(DISTINCT user_id) AS unique_buyers,
  SUM(orders) AS total_orders,
  SUM(revenue) AS total_revenue
FROM tracking_data
GROUP BY influencer_id;

#ROAS Calculation
SELECT 
  p.influencer_id,
  SUM(t.revenue) / SUM(p.total_payout) AS roas
FROM payouts p
JOIN tracking_data t ON p.influencer_id = t.influencer_id
GROUP BY p.influencer_id;

#Incremental ROAS Calculation
#Formula = (Revenue_with_campaign - Baseline_Revenue) / Spend
SELECT    
  t.influencer_id,   
  (SUM(t.revenue) - 0.5 * AVG(t.revenue)) / SUM(p.total_payout) AS incremental_roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
GROUP BY t.influencer_id;

#Filtering 
SELECT t.*, i.category, i.platform
FROM tracking_data t
JOIN influencers i ON t.influencer_id = i.id
WHERE t.product = 'HKVitals'
  AND i.category = 'Fitness'
  AND i.platform = 'Instagram';
  
#Top performing influencers by revenue
SELECT influencer_id, SUM(revenue) AS total_revenue
FROM tracking_data
GROUP BY influencer_id
ORDER BY total_revenue DESC
LIMIT 5;

#Top performing influencers by ROAS
SELECT 
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
LIMIT 10;
  
#Best performing Influencers by Gender/Category
SELECT i.category, i.gender, SUM(t.revenue) AS total_revenue
FROM influencers i
JOIN tracking_data t ON i.id = t.influencer_id
GROUP BY i.category, i.gender
ORDER BY total_revenue DESC;
  
#Poor ROI giving influencers  
SELECT p.influencer_id, SUM(t.revenue) / SUM(p.total_payout) AS roas
FROM payouts p
JOIN tracking_data t ON p.influencer_id = t.influencer_id
GROUP BY p.influencer_id
HAVING roas < 1;
 
 #ROAS based on platforms
 SELECT 
    t.source,
    p.influencer_id,
    i.name AS influencer_name,
    ROUND(SUM(t.revenue) / NULLIF(SUM(p.total_payout), 0), 2) AS roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
JOIN influencers i ON t.influencer_id = i.id
GROUP BY t.source, p.influencer_id, i.name
ORDER BY t.source, roas DESC;
 
 #ROAS Based on Months
SELECT 
    DATE_FORMAT(t.date, '%Y-%m') AS month,
    ROUND(SUM(t.revenue) / NULLIF(SUM(p.total_payout), 0), 2) AS monthly_roas
FROM tracking_data t
JOIN payouts p ON t.influencer_id = p.influencer_id
GROUP BY DATE_FORMAT(t.date, '%Y-%m')
ORDER BY month ASC;

#Total Reach in terms of orders
SELECT SUM(reach) AS total_reach
FROM posts;

#total reach by influencers
SELECT 
    p.influencer_id,
    i.name AS influencer_name,
    SUM(p.reach) AS total_reach
FROM posts p
JOIN influencers i ON p.influencer_id = i.id
GROUP BY p.influencer_id, i.name
ORDER BY total_reach DESC;

#total reach by platform
SELECT 
    p.platform,
    SUM(p.reach) AS total_reach
FROM posts p
GROUP BY p.platform
ORDER BY total_reach DESC;



