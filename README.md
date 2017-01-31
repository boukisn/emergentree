# EmergenTree Risk Assessment Workflow

## BranchPi  

### Logging
- **Every minute**, log the angle (x, y, and z) & acceleration (x, y, and z) on one line.

   *If the current time is __12:00 AM to 5:59 AM__,  write to* `<CURRENT DATE>_0_data.log`  
   *If the current time is __6:00 AM  to 11:59 AM__, write to* `<CURRENT DATE>_1_data.log`  
   *If the current time is __12:00 PM to 5:59 PM__,  write to* `<CURRENT DATE>_2_data.log`  
   *If the current time is __6:00 PM  to 11:59 PM__, write to* `<CURRENT DATE>_3_data.log`  

### Processing
- At **6:00 AM**, **12:00 PM**, **6:00 PM**, and **12:00 AM** (next day):

   *If the current time is __6:00 AM__ upload* `<CURRENT DATE>_0_data.log` *to AWS S3*  
   *If the current time is __12:00 PM__ upload* `<CURRENT DATE>_1_data.log` *to AWS S3*  
   *If the current time is __6:00 PM__ upload* `<CURRENT DATE>_2_data.log` *to AWS S3*  
   *If the current time is __12:00 AM__ upload* `<CURRENT DATE - 1>_3_data.log` *to AWS S3*  

## HomePi

### Logging
- **Every hour**, log the current wind speed and a list of currrent weather advisories by code on one line:

   *If the current time is __12:00 AM to 5:59 AM__, write to* `<CURRENT DATE>_0_weather.log`  
   *If the current time is __6:00 AM  to 11:59 AM__, write to* `<CURRENT DATE>_1_weather.log`  
   *If the current time is __12:00 PM to 5:59 PM__, write to* `<CURRENT DATE>_2_weather.log`  
   *If the current time is __6:00 PM  to 11:59 PM__, write to* `<CURRENT DATE>_3_weather.log`  

### Processing
- At **6:15 AM**, **12:15 PM**, **6:15 PM**, and **12:15 AM** (next day):

   *If the current time is __6:15 AM__ retrieve* `<CURRENT DATE>_0_data.log` *from AWS S3*  
   *If the current time is __12:15 PM__ retrieve* `<CURRENT DATE>_1_data.log` *from AWS S3*  
   *If the current time is __6:15 PM__ retrieve* `<CURRENT DATE>_2_data.log` *from AWS S3*  
   *If the current time is __12:15 AM__ retrieve* `<CURRENT DATE - 1>_3_data.log` *from AWS S3*  

   For that file, calculate the average overall acceleration and the overall acceleration standard deviation. Additionally:  

   *If the current time is __6:15 AM__, read* `<CURRENT DATE>_0_weather.log`  
   *If the current time is __12:15 PM__, read* `<CURRENT DATE>_1_weather.log`  
   *If the current time is __6:15 PM__, read* `<CURRENT DATE>_2_weather.log`  
   *If the current time is __12:15 AM__, read* `<CURRENT DATE - 1>_3_weather.log`  

   For that file, calculate the average wind speed.  Write the average overall acceleration, the overall acceleration standard deviation, and the average wind speed to `branch_wind_regress.log` (this file should have an initial line of “1.00;0.00;0.00;”).  

- At **6:30 AM**, **12:30 PM**, **6:30 PM**, and **12:30 AM** (next day), run a linear regression model on `branch_wind_regress.log` for:

   *Average wind speed vs. Average overall acceleration*  
   *Average wind speed vs. Overall acceleration variance*  

   Get the slope from each regression model. Write both values to `branch_slope_regress.log` on one line.  

- At **6:45 AM**, **12:45 PM**, **6:45 PM**, and **12:45 AM** (next day), standardize the values in `branch_slope_regress.log`. Run a linear regression model on the values for:

   *Quarters since installation vs. Standardized slope of (Average wind speed vs. Average overall acceleration)*  
   *Quarters since installation vs. Standardized slope of (Average wind speed vs. Overall acceleration variance)*  

   Where each unit *quarter* represents 6 hours, or a quarter of one whole day. Depending on the number of total data points, either one or two sets of regression models should be used. If the number of data points exceeds 56 (two weeks since installation), the output slope should be the sum of 75% the slope of the last 7 days, and 25% the slope of the whole data set. Otherwise, the output slope should just be the slope of the whole data set.  

   Next, get the slope from each regression model and calculate the average of the two values. Assign a **base risk** based on the averaged slope value:  

   *__1.0__ if the averaged value is less than __0.000__ (i.e. decreasing standard deviations or maintaining mean)*  
   *__2.0__ if the averaged value is between __0.000 and 0.025__ (i.e. increasing between 0.0 and 0.1 standard deviations per day)*  
   *__3.0__ if the averaged value is between __0.025 and 0.050__ (i.e. increasing between 0.1 and 0.2 standard deviations per day)*  
   *__4.0__ if the averaged value is between __0.050 and 0.100__ (i.e. increasing between 0.2 and 0.4 standard deviations per day)*  
   *__5.0__ if the averaged value is greater than __0.100__ (i.e. increasing greater than 0.4 standard deviations per day)*  

   Multiply the base risk by the following amounts if there is *currently* an indicated National Weather Service advisory:  

   **x5.0**  
   *Hurricane Warning (HUW)*  
   *Tornado Warning (TOR)*  
   *Extreme Wind Warning (EWW)*  
   *Earthquake Warning (EQW)*  
   *Fire Warning (FRW)*  
   *Tsunami Warning (TSW)*  

   **x1.5**  
   *Hurricane Watch (HUA)*  
   *Tornado Watch (TOA)*  
   *Tsunami Watch (TSA)*  
   *Severe Thunderstorm Warning (SVR)*  
   *Tropical Storm Warning (TRW)*  
   *High Wind Warning (HWW)*  
   *Blizzard Warning (BZW)*  

   **x1.3**  
   *Severe Thunderstorm Watch (SVA)*  
   *Tropical Storm Watch (TRA)*  
   *High Wind Watch (HWA)*  

   **x1.2**  
   *Winter Storm Warning (WSW)*  
   *Coastal Flood Warning (CFW)*  
   *Flood Warning (FLW)*  

   **x1.1**  
   *Winter Storm Watch (WSA)*  
   *Coastal Flood Watch (CFA)*  
   *Flood Watch (FLA)*  

   The final risk output is determined using the following scale:  
   *__Minimal risk__ if output is between __1.0__ and __2.0__*  
   *__Low risk__ if output is between __2.0__ and __3.0__*  
   *__Medium risk__ if output is between __3.0__ and __4.0__*  
   *__High risk__ if output is between __4.0__ and __5.0__*  
   *__Severe risk__ if output is greater than __5.0__*  

