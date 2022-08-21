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