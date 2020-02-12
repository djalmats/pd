import sys
import os
import boto3
import tempfile
import json
import io

from pyspark import SparkContext, SparkConf
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import *

conf = SparkConf()
sc = SparkContext.getOrCreate(conf=conf)
sc.setLogLevel('ERROR')
spark = (SparkSession.builder.appName("Load_Files").enableHiveSupport().getOrCreate())

bucket_name = sys.argv[1]
base_a_path = 's3://'+bucket_name+'/teste/base_a/'
base_b_path = 's3://'+bucket_name+'/teste/base_b/'
output_path = 's3://'+bucket_name+'/teste/'
object_name = 'teste/'
ext_json = '.json'
page_code = 'utf-8'
codec = 'snappy'

df_pageviews = spark.read.json(base_b_path)
df_pageviews.registerTempTable("df_pageviews")
#z.show(df_pageviews)

df_students = spark.read.json(base_a_path + 'students' + ext_json )
df_students.registerTempTable("df_students")
#z.show(df_students)

df_sessions = spark.read.json(base_a_path + 'sessions' + ext_json )
df_sessions.registerTempTable("df_sessions")
#z.show(df_sessions)

df_subscriptions = spark.read.json(base_a_path + 'subscriptions' + ext_json )
df_subscriptions.registerTempTable("df_subscriptions")
#z.show(df_subscriptions)

df_universities = spark.read.json(base_a_path + 'universities' + ext_json )
df_universities.registerTempTable("df_universities")
#z.show(df_universities)

df_courses = spark.read.json(base_a_path + 'courses' + ext_json )
df_courses.registerTempTable("df_courses")
#z.show(df_courses)

df_subjects = spark.read.json(base_a_path + 'subjects' + ext_json )
df_subjects.registerTempTable("df_subjects")
#z.show(df_subjects)

df_student_follow_subject = spark.read.json(base_a_path + 'student_follow_subject' + ext_json )
df_student_follow_subject.registerTempTable("df_student_follow_subject")
#z.show(df_student_follow_subject)

df_marketing_campaign = spark.sql("""
select a.marketing_campaign, count(*) qtd
from   df_pageviews a
left   join df_subscriptions b 
on b.studentid = replace(replace(replace(replace(a.studentId_clientType,'@Website',''),'@Android',''),'@Webapp',''),'@iOS','')
where  a.studentId_clientType <> 'null' and a.marketing_campaign <> 'null'
group  by 1 order by 2 desc
""")
df_marketing_campaign.registerTempTable("df_marketing_campaign")
#z.show(df_marketing_campaign)

########## OUTPUT --##########
df_marketing_campaign.printSchema()
df_marketing_campaign.repartition(100).write.mode('append').orc(output_path,compression=codec)
