## Some SQL statements to conclude some metrics driven by data
this [query](extracting_candidate_job_view_apply.sql) to extract some useful fields from JSON column (data) for two types of events data 
1. candidate_applied_job_opening
2. candidate_views_job_opening

``` sql
select 
  date(DATETIME(created_at, "UTC")) created_at,
  JSON_VALUE(data,'$.candidate_uuid') candidate_uuid,
  JSON_VALUE(data,'$.job_opening_id') job_opening_id,
  JSON_VALUE(data,'$.site_id') site_id,
  case 
    when type like 'candidate_views_job_opening' 
        then 'view' 
    else 'apply' end type 
from `zeta-period-359422.bq_dataeng_assignment.yc_app_events_bq`
where 
  type in ('candidate_views_job_opening','candidate_applied_job_opening')
```

let's export the result of the query to a new bq table in **candidate_view_apply_job** in the same dataset

## Queries 

1. Average daily **apply** per **candidate** by the site :
[avg_daily_apply_per_candidate_by_site.sql](avg_daily_apply_per_candidate_by_site.sql)

``` sql

select round(avg(cnt),2) average,created_at,site_id 
    from( select count(*) cnt, created_at,candidate_uuid,site_id 
                from `zeta-period-359422.bq_dataeng_assignment.candidate_view_apply_job`
                where type like 'apply'
                group by created_at,candidate_uuid,site_id
        ) tempo
    group by created_at,site_id
    order by site_id,created_at
```

2. Average daily **apply** per **job** by the site :
[avg_daily_apply_per_job_by_site.sql](avg_daily_apply_per_job_by_site.sql)

``` sql

select round(avg(cnt),2) average,created_at,site_id 
    from( select count(*) cnt, created_at,job_opening_id,site_id 
                from `zeta-period-359422.bq_dataeng_assignment.candidate_view_apply_job`
                where type like 'apply'
                group by created_at,job_opening_id,site_id
        ) tempo
    group by created_at,site_id
    order by site_id,created_at
```

3. Average daily **view** per **candidate** by the site :
[avg_daily_view_per_candidate_by_site](avg_daily_view_per_candidate_by_site.sql)

```sql

select round(avg(cnt),2) average,created_at,site_id 
    from( select count(*) cnt, created_at,candidate_uuid,site_id 
                from `zeta-period-359422.bq_dataeng_assignment.candidate_view_apply_job`
                where type like 'view'
                group by created_at,candidate_uuid,site_id
        ) tempo
    group by created_at,site_id
    order by site_id,created_at
```

4. Average daily **view** per **job** by the site:
[avg_daily_view_per_job_by_site.sql](avg_daily_view_per_job_by_site.sql)

``` sql
select round(avg(cnt),2) average,created_at,site_id 
    from( select count(*) cnt, created_at,job_opening_id,site_id 
                from `zeta-period-359422.bq_dataeng_assignment.candidate_view_apply_job`
                where type like 'view'
                group by created_at,job_opening_id,site_id
        ) tempo
    group by created_at,site_id
    order by site_id,created_at
```
