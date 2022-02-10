# Ahmedabad Real-Data Provenance

This project now includes published Ahmedabad freight and industrial-logistics observations. These are not fabricated company records.

## Primary sources

1. Swamy, S. H. M., & Baindur, D. (2014). *Managing urban freight transport in an expanding city — Case study of Ahmedabad*. Research in Transportation Business & Management, 11. DOI: 10.1016/j.rtbm.2014.06.010.
   - Cordon classified-volume-count survey at eight entry/exit points.
   - Approximately 34,182 freight vehicles/day entered or exited Ahmedabad in the survey baseline (2006).
   - 48,485 vehicles/day was estimated for 2012 using 6% compounded annual growth.
   - The study reports 55,000 factory properties and 29,000 transport/warehouse properties from AMC property-tax data for 2011.
   - Vatva, Naroda and Odhav together had 4,550 manufacturing units over about 992 ha and attracted more than 1,500 trucks/day; Vatva and Naroda were reported at about 600 trucks/day each.
   - Aslali, Sarkhej and Narol were reported at 2,180, 1,133 and 755 freight vehicles/day respectively.

2. *Planning Framework for Low Emission Zone (LEZ) In Core Areas of Indian Cities* (2025 report using 2021 Ahmedabad property-tax data).
   - Around 135,025 industrial units were identified within Ahmedabad in 2021.
   - Vatva, Odhav and Naroda collectively accounted for 8,700 units.
   - Around 39,000 properties were occupied by transporters and warehouses in 2021.

## Data-status convention

- `evidence_based`: directly reported in the cited source or a direct arithmetic total explicitly reported by the source.
- Blank cells are intentionally left blank when the cited source does not provide the individual figure.
- No unpublished company records, proprietary freight costs, route-level monetary costs, or fabricated observations are represented as real data.

## Important modeling note

The original `transportation_costs.csv` remains a reproducible demonstration cost matrix because the published Ahmedabad studies do not provide a complete route-by-route monetary transportation-cost matrix. It must not be described as observed Ahmedabad company cost data.
