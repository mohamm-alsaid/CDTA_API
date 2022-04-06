# CDTA API

This is an implementation of `CDTA` server that handles the aggregation of `MVoT`s from local `DTMC`s. 

## Endpoints
* `/MVoT`

## Methods

* POST `/MVoT`
    * DTMCs post their respective MVoT to `MVoT` endpoint to update the CDTA of changes to their trust calculations.
    * Body of request should be validated to contain:
        * `anon_id`:  anonymized ID of DER for that service
            * If the DTMC does not have this, it should use the default `*-*-*-*` ID (all anonymized)
        * `registration_date`: date of device registration
        * `last_timestamp`: timestamp of last message
        * `sdtt`: standard deviation of transit time
        * `RFC`: relative factor of certainty
        * `TSLC`: time since last communication
        * `tx_time`: transit time
        * `comm_freq`: communication frequency
        * `certainty`: current certainty level
        * `avg_tx_time`: average transit time
        * `trust_score`: current trust score
        * `distrust_score`: current distrust score 
        * `total_msgs`: total number of messages
        * `other_count`: count of other actions 
        * `alerts_count`: count of alerts
        * `timeout_count`: count of timeouts
        * `count_expected_msgs`: count of expected messages
        * `count_unexpected_msgs`: count of unexpected messages
    * Response: status code 
        * `200` if message validation passes and insertion was successful
        * `400` if request validation failed 
        * `500` otherwise
* GET `/MVoT`
    * Returns recent MVoT data for all DTMCs for the purposes of plotting current trust level/dashboard app
    * Body of request should be empty
    * Response: XML list of latest MVoT entries from each DTMC


## Dependencies
To install dependencies, use: `pip3 install -r requirements.txt`
## Seed the database 
To seed the DB, use `init_db.py` script. To do so, run: `python3 init_db.py`


## Run the server
To run the server, use: `python3 CDTA.py`

This runs an HTTP server on port `80`. This should be changed to port `443` when self-signed certificate support is setup.
> Might need to use `sudo` when running the server depending on the OS


## Tests
To run the tests, run: `python3 -m unittest test_api.py`
> The tests involve testing both available methods (GET/POST) for `/MVoT` endpoint.

## Example of messages
* POST `/MVoT`

The following is an example of what the XML format __expected__ for a POST request on the endpoint
```
<?xml version='1.0'?>
<MVoT>
    <anon_id>substation0:segment7:xformer2:DER 40-50</anon_id>
    <registration_date>1629393715.096357</registration_date>
    <last_timestamp>1629394315.096386</last_timestamp>
    <sdtt>0.1112444366039249</sdtt>
    <RFC>1.0</RFC>
    <TSLC>300.00001287460327</TSLC>
    <tx_time>0.17</tx_time>
    <comm_freq>0.0049999997595946</comm_freq>
    <certainty>0.0002321533514997</certainty>
    <avg_tx_time>0.131038961038961</avg_tx_time>
    <trust_score>0.0006344171455322</trust_score>
    <distrust_score>0.0</distrust_score>
    <total_msgs>3</total_msgs>
    <other_count>0</other_count>
    <alerts_count>0</alerts_count>
    <timeout_count>0</timeout_count>
    <count_expected_msgs>3</count_expected_msgs>
    <count_unexpected_msgs>0</count_unexpected_msgs>
</MVoT>
```
* GET `/MVoT`

The following is an example of what the CDTA returns of GET request on the endpoint
```
<?xml version="1.0" ?>
<MVoTs>
    <MVoT>
        <mvot_id>1302</mvot_id>
        <anon_id>*-*-*-*</anon_id>
        <registration_date>1629393715.096362</registration_date>
        <last_timestamp>1629537715.103173</last_timestamp>
        <sdtt>0.0108067067597848</sdtt>
        <RFC>1.0</RFC>
        <TSLC>300.00001192092896</TSLC>
        <tx_time>0.34</tx_time>
        <comm_freq>0.0033402776197895</comm_freq>
        <certainty>0.0011134258289796</certainty>
        <avg_tx_time>0.2538750830835711</avg_tx_time>
        <trust_score>0.5355601460814438</trust_score>
        <distrust_score>0.0</distrust_score>
        <total_msgs>481</total_msgs>
        <other_count>0</other_count>
        <alerts_count>0</alerts_count>
        <timeout_count>0</timeout_count>
        <count_expected_msgs>481</count_expected_msgs>
        <count_unexpected_msgs>0</count_unexpected_msgs>
    </MVoT>
    ....
    <MVoT>
        <mvot_id>1924</mvot_id>
        <anon_id>*-*-*-*</anon_id>
        <registration_date>1629393715.096365</registration_date>
        <last_timestamp>1629537715.103177</last_timestamp>
        <sdtt>0.0112319018613085</sdtt>
        <RFC>1.0</RFC>
        <TSLC>300.00001311302185</TSLC>
        <tx_time>0.25</tx_time>
        <comm_freq>0.0033402776197618</comm_freq>
        <certainty>0.001113425824546</certainty>
        <avg_tx_time>0.2441793344732304</avg_tx_time>
        <trust_score>0.5355601465070687</trust_score>
        <distrust_score>0.0</distrust_score>
        <total_msgs>481</total_msgs>
        <other_count>0</other_count>
        <alerts_count>0</alerts_count>
        <timeout_count>0</timeout_count>
        <count_expected_msgs>481</count_expected_msgs>
        <count_unexpected_msgs>0</count_unexpected_msgs>
    </MVoT>
</MVoTs>
```