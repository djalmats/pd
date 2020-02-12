--${ETL_ROOT_PATH}/
--${ETL_FILE_JSON_PATH_A}/

--########## SCHEMAS ##########
create schema dw;
create schema stg;

--########## STAGE TABLES ##########
drop table if exists stg.courses;
drop table if exists stg.sessions;
drop table if exists stg.student_follow_subject;
drop table if exists stg.students;
drop table if exists stg.subjects;
drop table if exists stg.subscriptions;
drop table if exists stg.universities;

create table stg.courses (id varchar(500) not null,name varchar(100));
create table stg.sessions (studentid varchar(500) not null,sessionstarttime timestamp,studentclient varchar(100));
create table stg.student_follow_subject (studentid varchar(500) not null,subjectid bigint,followdate timestamp);
create table stg.students (id varchar(500) not null,registeredDate timestamp,state varchar(100),city varchar(100),universityID bigint,courseId bigint,signupSource varchar(500));
create table stg.subjects (id bigint not null,name varchar(10000));
create table stg.subscriptions (studentid varchar(500) not null,paymentdate timestamp,plantype varchar(100));
create table stg.universities (id bigint not null,name varchar(500));

--########## DW TABLES ##########

drop table if exists dw.dm_state;
drop table if exists dw.dm_platform;
drop table if exists dw.dm_university;
drop table if exists dw.dm_course;

drop table if exists dw.ft_user_info;
drop table if exists dw.ft_user_activity;

create table dw.dm_state (state_id bigint not null,state_name varchar(100));
create table dw.dm_platform (platform_id bigint not null,platform_name varchar(100),platform_main_name varchar(100));
create table dw.dm_university (university_id bigint not null,university_name varchar(100));
create table dw.dm_course (course_id bigint not null,course_name varchar(100));

create table dw.ft_user_info
(
 platform_id bigint 
,state_id bigint 
,university_id bigint 
,course_id bigint 
,n_students_total bigint 
,n_students_subscribers bigint 
,n_students_subscribers_monthly bigint 
,n_students_subscribers_yearly bigint 
,n_days_to_premium_conversion bigint 
);

create table dw.ft_user_activity
(
 platform_id bigint 
,state_id bigint 
,n_session_time numeric 
,n_session_time_subscribers numeric  
);