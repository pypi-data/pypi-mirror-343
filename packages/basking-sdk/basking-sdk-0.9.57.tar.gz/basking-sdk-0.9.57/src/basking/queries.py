GET_ORG_VISIT_DURATION = """
            query getOrgDurationOfVisits($id: ID!, $from: DateTime!, $to: DateTime!, $floorIds: [String!], $floorAreaIds: [Int!]){
                organization: getOrganization(organizationID: $id) {
                    durationOfVisits(from: $from, to: $to, floorIds: $floorIds, floorAreaIds: $floorAreaIds) {
                        visitDuration: hPerDay,
                        visitsCount: clientCount, 
                        visitsPct: percClient,
                        countryRegion
                     }
                }
            }
        """

GET_ORG_VISIT_FREQ = """
        query getOrgFrequencyOfVisits($id: ID!, $from: DateTime!, $to: DateTime!, $floorIds: [String!], $floorAreaIds: [Int!]){
            organization: getOrganization(organizationID: $id) {
                frequencyOfVisits(from: $from, to: $to, floorIds: $floorIds, floorAreaIds: $floorAreaIds, predictedLocations: false) {
                    visitFrequency: daysPerWeek,
                    visitsCount: clientsCount,
                    visitsPerc: clientsPct,
                    countryRegion
                }
            }
        }
        """

GET_LOCATION_STATS_DAILY = """
                    query getBuildingOccupancyStatsDaily(
                        $id: ID!,
                        $from: DateTime!,
                        $to: DateTime!
                        $capacityType: String
                        $floorIds: [String!]
                        $floorAreaIds: [Int!]
                    ) {
                        location(id: $id) {
                            occupancy{
                                daily(
                                    from: $from,
                                    to: $to,
                                    capacityType: $capacityType,
                                    floorIds: $floorIds,
                                    floorAreaIds: $floorAreaIds,
                                ) {
                                    date, 
                                    peakCount,
                                    avgCount,
                                    capacity,
                                    adjustedCapacity,
                                    capacityPct,
                                    uniqueCount
                                }
                            }
                        }
                    }
                        """

GET_LOCATION = """
                    query getBuilding($buildingid: ID){
                        getBuilding(id: $buildingid)
                        {
                            id,
                            workingDays,
                            name,
                            capacity,
                            currentAdjCapacityAbs,
                            workstationsCapacity,
                            totalSeatsCapacity,
                            numberOfDesks,
                            address,
                            timeZone,
                            lat,
                            lng,
                            organizationId,
                            organization{id, name},
                            floors{id, vendorFloorId, buildingId, createdAt, number, name, capacity, workstationsCapacity, totalSeatsCapacity, sqm, floorplanURL, rotation, neCorner, swCorner},
                            rentPriceSQM,
                            currency,
                            area,
                            operationStartTime,
                            operationEndTime,
                            measurementUnits,
                            targetOccupancy,
                            country,
                            countryRegion,
                            euroPerKWH,
                            pulsePerKW,
                            co2PerSQM,
                            tags,
                            headCount,
                            preferences {
                                capacityType
                                co2TonsPerSqm
                                officeDaysMandate
                                officeDaysMandates { days, startDate }
                            }
                        }
                    }
                """

GET_LOCATION_OCCUPANCY_HOURLY = """
                query getBuildingMerakiHourlyData(
                        $id: ID!,
                        $from: DateTime!,
                        $to: DateTime!,
                        $floorIds: [String!],
                        $floorAreaIds: [Int!],
                        $capacityType: String
                    ) {
                        location(id: $id) {
                            occupancy{
                                hourly(
                                    from: $from,
                                    to: $to,
                                    floorIds: $floorIds,
                                    floorAreaIds: $floorAreaIds,
                                    capacityType: $capacityType
                                ) {
                                    hour, 
                                    occupancy: uniqueCount
                                    capacity
                                    adjustedCapacity
                                    capacityPct
                                }
                            }
                        }
                    }

                """

GET_FLOOR_HEATMAP_KPI = """
                       query getFloorHeatmapKPI($floorId: String, $startDate: String, $endDate: String)
                       {
                           getFloorHeatmapKPI(
                            floorId: $floorId,
                            startDate: $startDate,
                            endDate : $endDate,
                            resampleBy : 5
                        ){
                        floorAreaId,
                        maxDevices,
                        avgDevices,
                        maxTimeSpentMinutes,
                        avgTimeSpentMinutes,
                        minTimeSpentMinutes,
                        maxHumans,
                        avgHumans,
                        avgOcuppancy,
                        frequencyOfUse,
                        utilization
                    }}
                    """

GET_FLOOR_METADATA = """
                query readFloor($basking_floor_id: ID){
                    getFloor(id: $basking_floor_id) {
                        id, 
                        number, 
                        name, 
                        sqm, 
                        neCorner, 
                        swCorner, 
                        rotation, 
                        capacity,
                        buildingId
                    }
                }
                """

GET_FLOOR_AREAS = """
                query readFloorArea($basking_floor_id: String){
                        getFloorArea(floorId: $basking_floor_id) {
                            id, 
                            name, 
                            capacity, 
                            geometry, 
                            areaTagId, 
                            tag{id, name}
                        }
                    }
                """

GET_ADJUSTED_CAPACITY = """
                   query readCapacity($locationId: ID!){
                        getCapacity(locationId: $locationId) {
                            id,
                            capacity,
                            start,
                            end,
                            buildingId:locationId,
                            floorId,
                            areaId
                        }
                    }
        """

GET_USER_LOCATIONS = """
                    query getUserBuildings($integrated: Boolean){
                        viewer{
                            buildings (integratedOnly: $integrated) {
                                 id,
                                 name,
                                 address,
                                 timeZone,
                                 hasMeraki,
                                 isActive,
                                 lat,
                                 lng,
                                 organizationId,
                                 tags,
                                }
                            }
                        }
                """

GET_LOCATION_VISIT_DURATION = """
                    query duration(
                        $id: ID!,
                        $from: DateTime!,
                        $to: DateTime!,
                        $floorIds: [String!], 
                        $floorAreaIds: [Int!],
                        $capacityType: String
                    ) {
                        location(id: $id) {
                            occupancy{
                                duration(
                                    from: $from, 
                                    to: $to,
                                    floorIds: $floorIds, 
                                    floorAreaIds: $floorAreaIds,
                                    capacityType: $capacityType
                                ) {
                                    visitDuration: hoursCount, 
                                    visitsCount: clientsCount,
                                    visitsPerc: clientsPct
                                }
                            }
                        }
                    }       
                """

GET_LOCATION_VISIT_FREQ = """
                    query duration(
                        $id: ID!,
                        $from: DateTime!,
                        $to: DateTime!
                        $floorIds: [String!]
                        $floorAreaIds: [Int!]
                        $capacityType: String
                    ) {
                        location(id: $id) {
                            occupancy{
                                frequencyOfVisits(
                                    from: $from, 
                                    to: $to,
                                    floorIds: $floorIds
                                    floorAreaIds: $floorAreaIds
                                    capacityType: $capacityType
                                ) {
                                    visitFrequency: daysPerWeek, 
                                    visitsCount: clientsCount,
                                    visitsPct: clientsPct
                                }
                            }
                        }
                    }       
                """

GET_ORG_HOTELING = """
                   query getHotelingbyOrg(
                       $id: ID!,
                       $startDate: String!, 
                       $endDate: String!
                   ){
                       organization:getOrganization(organizationID: $id){
                           hoteling(startDate: $startDate, 
                                   endDate: $endDate) {
                               from,
                               to,
                               count,
                               country,
                               countryRegion
                           }
                       }
                   }
               """

GET_ORG_DETAILS = """
                    query getOrganization(
                        $id: ID!
                    ){
                        organization: getOrganization(organizationID: $id) {
                            id, name   
                        }  
                    }
                """

GET_USER_ORGS = """
                query getUserOrgs {
                    viewer{
                        organizationId, 
                        organizations{
                            id, 
                            name 
                        }
                    }
                }
                """

GET_LOCATION_POPULAR_VISIT_DAYS = """
             query popularDays(
                $id: ID!,
                $from: DateTime!,
                $to: DateTime!,
                $floorIds: [String!], 
                $floorAreaIds: [Int!],
                $capacityType: String
            ) {
                location(id: $id) {
                    occupancy{
                        popularDaysOfVisit(
                            from: $from, 
                            to: $to,
                            floorIds: $floorIds, 
                            floorAreaIds: $floorAreaIds,
                            capacityType: $capacityType
                        ) {
                            visitWeekday: dayOfWeek, 
                            visitsCount: clientsCount,
                            visitsPct: clientsPct
                        }
                    }
                }
            }
        """

GET_INSIGHTS = """
            query getInsights($id: ID!, $from: DateTime!, $to: DateTime!){
                getBuildingInsights(id: $id, from: $from, to: $to) {
                    buildingId,
                    monthlyRent,
                    capacity,
                    occupancyPeakMax,
                    occupancyPeakMaxPct,
                    occupancyPeakAvgPct,
                    opportunitySeats,
                    opportunitySeatsPct,
                    adjCapacityPct,
                    targetOccupancyPct,
                    opportunitySpace,  // in m2
                    opportunitySpacePct,
                    opportunityPeopleCount,
                    staffAllocationIncrease,
                    currencySymbol,
                    lengthUnits,
                    peopleImpact {
                        occupancyPeakAvgPct,
                        occupancyPeakMaxPct,
                        costSavings,
                        costSavingsStr,
                    }
                     spaceImpact {
                        occupancyPeakAvgPct,
                        occupancyPeakMaxPct,
                        costSavings,
                        costSavingsStr,
                    }
                }
            }
            """

GET_ORG_POPULAR_VISIT_DAYS = """
            query getOrgPopularDaysOfVisits($id: ID!, $from: DateTime!, $to: DateTime!, $floorIds: [String!], $floorAreaIds: [Int!]){
              organization: getOrganization(organizationID: $id) {
                    popularDaysOfVisits(from: $from, to: $to, floorIds: $floorIds, floorAreaIds: $floorAreaIds) { 
                        visitWeekday: dayOfWeek,
                        visitsCount: clientsCount,
                        visitsPct: clientsPct,
                        countryRegion
                    }
                }
            }
        """

GET_ORG_LOCATIONS = """
        query getOrgLocations($id: Int!, $integrated: Boolean) {
        locations: getBuildingsByOrganization(organizationId: $id, integratedOnly: $integrated) {
                  id,
                  name,
                  address,
                  capacity,
                  timeZone,
                  area,
                  rentPriceSQM,
                  organizationId,
                  targetOccupancy,
                  measurementUnits,
                  currency
                  country,
                  countryRegion,
                  hasMeraki,
                  isActive,
                  workingDays,
                  operationStartTime,
                  operationEndTime,
                  totalSeatsCapacity,
                  workstationsCapacity,
                  co2PerSQM,
                  tags,
                  headCount,
                  preferences {
                        capacityType
                        co2TonsPerSqm
                        officeDaysMandate
                        officeDaysMandates { days, startDate }
                    }
                }
              }
        """

GET_USER = """
                query getUser {
                    viewer{ 
                        id,
                        email,
                        name,
                        firstName,
                        lastName,
                        primaryOrgId: organizationId,
                        createdAt, 
                        measurementUnits, 
                        currency, 
                        isAdjCapacityNormalizationEnabled, 
                    }
                }
                """

GET_COMPOSITE_PREFERENCES = """
    query getCompositePreferences ($userId: String, $organizationId: Int, $locationId: String) {
    getCompositePreferences (userId: $userId, organizationId: $organizationId, locationId: $locationId) {
        capacityType
        co2TonsPerSqm
        officeDaysMandate
        officeDaysMandates { days, startDate }
    }
}
"""
