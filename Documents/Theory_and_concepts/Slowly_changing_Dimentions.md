In data warehousing data is deveident into fact and dimention tables, with time these dimention changes . When these dimention attributes are changeing is directly impact the fates and final anlystics.
If we do not handle them with proper strategy we either lose historical accuracy or ose tract of change in data. In case we keep all the old version data management becomes difficult with huge dimention tables overall processs slows down

- In OLTP system tables simply get updated and with update in row all the transetinal system start reflecting updated values
- Keeping all version increase and create duplicate data.
- SCD type gives startdr and well defined strategy to handle chaging dimetions and thier impact on data

Dimentions tables: Descreptive and reference data tables customer product employee tables
Surrogate key: System generated artifical key used as primary key
Natura business key: real world primary key. Remain constant throught out the history of data.
Effective date/Expirty date: Columnmarking validity of active and inactve version of dimention data
Current flag: Boolen value to reflect active or historical data
Version Number: To tract iteration of change along with date
Late-arriving data: Fat data arrive before the corresponding dimension record

SCD typ0: Never change the attribute it remain immutable once write stay forever.. Chnage is not possible
SCD type1: 
