--This code uses SQL (BigQuery) to prepare and process data from the following dataset: https://www.kaggle.com/datasets/arashnic/fitbit
--FitBit Fitness Tracker Data (CC0: Public Domain, dataset made available through Mobius)
--Six tables are used. They are imported with the following names:
--Original: minuteMETsNarrow_merged.csv     imported as minuteMET
--Original: hourlyCalories_merged.csv       imported as hourlyCalories
--Original: hourlyIntensities_merged.csv    imported as hourlyIntensities
--Original: hourlySteps_merged.csv          imported as hourlySteps
--Original: sleepDay_merged.csv             imported as dailySleep
--Original: dailyActivity_merged.csv        imported as dailyActivity
--Author: Woramon P.
--Date: 07/28/2022

--create temp table from dailyActivity table
WITH temp_dailyActivity AS (
  SELECT Id AS user_id,
    CAST(ActivityDate AS datetime) AS date_time,
    TotalSteps AS daily_steps,
    TotalDistance AS daily_distance_total,
    TrackerDistance AS daily_distance_tracker,
    VeryActiveDistance AS daily_distance_4veryactive,
    ModeratelyActiveDistance AS daily_distance_3moderatelyactive,
    LightActiveDistance AS daily_distance_2lightlyactive,
    SedentaryActiveDistance AS daily_distance_1sedentary,
    VeryActiveMinutes AS daily_minutes_4veryactive,
    FairlyActiveMinutes AS daily_minutes_3fairlyactive,
    LightlyActiveMinutes AS daily_minutes_2lightlyactive,
    SedentaryMinutes AS daily_minutes_1sedentary,
    Calories AS daily_calories
  FROM `Fitabase_160412_160512.dailyActivity`
),

--create temp table from dailySleep table
temp_dailySleep AS (
  SELECT Id AS user_id,
    parse_datetime('%m/%d/%Y %r', SleepDay) AS date_time, 
    TotalMinutesAsleep AS daily_minutes_asleep, 
    TotalTimeInBed AS daily_minutes_in_bed
  FROM (
    --there are duplicate rows in this table: Id 4388161847 on May 5, Id 4702921684 on May 7, Id 8378563200 on Apr 25
    --by performing SELECT DISTICT, duplicates are removed; the number of rows therefore reduces from 413 to 410
    SELECT DISTINCT * FROM `Fitabase_160412_160512.dailySleep`
    )
),

--create temp table from hourlyCalories table
temp_hourlyCalories AS (
  SELECT Id AS user_id,
    parse_datetime('%m/%d/%Y %r', ActivityHour) AS date_time,
    Calories AS hourly_calories
  FROM `Fitabase_160412_160512.hourlyCalories`
),

--create temp table from hourlyIntensities table
temp_hourlyIntensities AS (
  SELECT Id AS user_id,
    parse_datetime('%m/%d/%Y %r', ActivityHour) AS date_time,
    TotalIntensity AS hourly_intensity_total,
    AverageIntensity AS hourly_intensity_avg
  FROM `Fitabase_160412_160512.hourlyIntensities`
),

--create temp table from hourlySteps table
temp_hourlySteps AS (
  SELECT Id AS user_id,
    parse_datetime('%m/%d/%Y %r', ActivityHour) AS date_time,
    StepTotal AS hourly_steps
  FROM `Fitabase_160412_160512.hourlySteps`
),

--create temp table from minuteMET table
--divide MET by 10, because: All MET values exported from Fitabase are multiplied by 10. See https://www.fitabase.com/resources/knowledge-base/exporting-data/data-dictionaries/
temp_minuteMET AS (
  SELECT Id AS user_id,
    parse_datetime('%m/%d/%Y %r', ActivityMinute) AS date_time,
    METs / 10 AS minute_METs
  FROM `Fitabase_160412_160512.minuteMET`
)

--join temp tables into one large table for analysis
SELECT 
  --use IFNULL to prevent user_id and date_time (which are primary keys) from being NULL
  --DAYOFWEEK returns values in the range [1,7] with Sunday as the first day of of the week
  IFNULL(mm.user_id, IFNULL(hs.user_id, IFNULL(hi.user_id, IFNULL(hc.user_id, IFNULL(da.user_id, ds.user_id))))) AS user_id,
  EXTRACT(DATE from IFNULL(mm.date_time, IFNULL(hs.date_time, IFNULL(hi.date_time, IFNULL(hc.date_time, IFNULL(da.date_time, ds.date_time)))))) AS date_,
  EXTRACT(TIME from IFNULL(mm.date_time, IFNULL(hs.date_time, IFNULL(hi.date_time, IFNULL(hc.date_time, IFNULL(da.date_time, ds.date_time)))))) AS time_,
  EXTRACT(DAYOFWEEK from IFNULL(mm.date_time, IFNULL(hs.date_time, IFNULL(hi.date_time, IFNULL(hc.date_time, IFNULL(da.date_time, ds.date_time)))))) AS day,
  mm.minute_METs,
  hs.hourly_steps,
  hi.hourly_intensity_total,
  hi.hourly_intensity_avg,
  hc.hourly_calories,
  ds.daily_minutes_asleep,
  ds.daily_minutes_in_bed,
  da.daily_calories,
  da.daily_steps,
  da.daily_distance_total,
  da.daily_distance_tracker,
  da.daily_distance_4veryactive,
  da.daily_distance_3moderatelyactive,
  da.daily_distance_2lightlyactive,
  da.daily_distance_1sedentary,
  da.daily_minutes_4veryactive,
  da.daily_minutes_3fairlyactive,
  da.daily_minutes_2lightlyactive,
  da.daily_minutes_1sedentary
FROM temp_minuteMET AS mm
--FULL JOIN is used because there are some unique user_id + date_time combination in other tables that are not present in temp_minuteMET 
FULL JOIN temp_hourlySteps AS hs
ON mm.user_id = hs.user_id AND mm.date_time = hs.date_time
FULL JOIN temp_hourlyIntensities AS hi
ON mm.user_id = hi.user_id AND mm.date_time = hi.date_time
FULL JOIN temp_hourlyCalories AS hc
ON mm.user_id = hc.user_id AND mm.date_time = hc.date_time
FULL JOIN temp_dailyActivity AS da
ON mm.user_id = da.user_id AND mm.date_time = da.date_time
FULL JOIN temp_dailySleep AS ds
ON mm.user_id = ds.user_id AND mm.date_time = ds.date_time
ORDER BY user_id, date_, time_

--save result as "BigQuery_result.csv", then proceed with analysis and visualization in R. Refer to a separate Rmd file for the code.