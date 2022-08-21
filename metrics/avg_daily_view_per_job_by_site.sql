
select round(avg(cnt),2) average,created_at,site_id 
    from( select count(*) cnt, created_at,job_opening_id,site_id 
                from `zeta-period-359422.bq_dataeng_assignment.candidate_view_apply_job`
                where type like 'view'
                group by created_at,job_opening_id,site_id
        ) tempo
    group by created_at,site_id
    order by site_id,created_at