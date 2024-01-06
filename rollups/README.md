# rollup fields

The FAC, under Census, disseminated data in CSVs. There were fields in their database/CSVs that were duplicative or otherwise derived.

In the FAC API, there are no derived or duplicative fields. We do not (for example) combine the agency number and program number into an ALN. They exist as two fields, and a programmer can make use of those two fields as they like. The FAC will not, at this time, provide an API field that combines these.

This directory documents those redundant fields from the previous data dissemination, and demonstrates how to compute them using the API.
