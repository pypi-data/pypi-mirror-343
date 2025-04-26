# Basking.io SDK

Integrate your data with the Basking API, customize the reports & experience,
and join the community of developers building with workplace software apps together with Basking.

Basking.io is a cloud based workplace occupancy platform.
More Information about Basking can be found here: https://basking.io

Basking uses a GraphQL API. The following Python SDK is a wrapper around the production API
designed for our customers that require to access to data programmatically.

## Requirements

* python >=3.7 (current tested version: 3.9)
* pipenv
* A [basking.io account](https://app.basking.io)

## Getting started

#### set the following environment variables:
* `BASKING_USERNAME`: Your username (usually your email)
* `BASKING_USER_PASSWORD`: Your password for Basking. 
* _Optional_: `BASKING_AWS_REGION`: the aws region where your Basking.io instance is hosted. (Defaults to `eu-central-1`)
* _Optional_: `BASKING_API_URL`: the url of the Basking API you would like to query. (Defaults to `api.basking.io`)

```
from basking.basking_sdk import Basking

logger.info('initialize the SDK. See constructor documentation for parameter overrides')
basking = Basking()

logger.info('List sites the current user has access to')
sites = basking.location.get_user_buildings(pandify=False)

logger.info('Select a site from the list of sites')
site_id = sites[0]['id']
organization_id = sites[0]['organizationId']
start_date_obj = date(2025, 1, 1)
end_date_obj = date(2025, 1, 14)

logger.info('get site meta data')
site_meta_data = basking.location.get_building(
    building_id=site_id
)

logger.info('get building daily occupancy statistics')
df_daily = basking.occupancy.get_building_occupancy_stats_daily(
    building_id=site_id,
    start_date=start_date_obj,
    end_date=end_date_obj,
    pandify=True,
    # floor_ids=[site_meta_data['data']['getBuilding']['floors'][0]['id']]
)

logger.info('metadata for all site areas')
areas_meta_data = basking.location.get_floor_areas_for_building(
    building_id=site_id
)

logger.info('get the density of the last 7 days')
density_last_week = basking.occupancy.get_density_for_building_last_days(
    building_id=site_id,
    days=7
)

logger.info('Frequency of Visits at Site Level')
df_freq_of_visits = basking.occupancy.get_location_frequency_of_visits(
    building_id=site_id,
    start_date=start_date_obj,
    end_date=end_date_obj,
    pandify=True
)

logger.info('Duration of Visits at Site Level')
df_duration_of_visits = basking.occupancy.get_location_duration_of_visits(
    building_id=site_id,
    start_date=start_date_obj,
    end_date=end_date_obj,
    pandify=True
)

logger.info('Popular Visitation days at Site Level')
df_preferred_visit_day = basking.occupancy.get_location_popular_days_of_visits(
    building_id=site_id,
    start_date=start_date_obj,
    end_date=end_date_obj,
    pandify=True
)
```


For more examples, see `basking.api_usage_example`, or [contact us](https://basking.io/contact-us/)
