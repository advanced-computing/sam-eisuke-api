# API Documentation

## Connecting to the API
Since we are running our API locally we will access the endpoint at ```http://127.0.0.1:5000``` (or the address the appears on your console).

## Welcome
- Method: GET
- Path: ```/```
- Query parameters: None

Friendly wecome to the API

## List
- Method: Get
- Path: ```/api/list```
-Query parameters: None

Shows Causes of Death from 2007-2021

## Record
- Method: Get
- Path: ```/api/record/<int:id>```
- Query: id

Use index to find specific row

## Covid Death
- Method: Get
- Path: ```/api/covid_death```
- Query: None

Shows results with Covid-19 Deaths

## hehe
- Method: Get
- Path: ```/api/i_want_extra_credit```
- Query: None

For laughs and giggles.

- Example query:
```
http://127.0.0.1:5000/api/i_want_extra_credit
```