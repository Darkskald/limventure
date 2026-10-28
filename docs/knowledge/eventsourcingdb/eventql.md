---
title: EventQL query language
summary: Syntax, sources, fields, operators, types, functions and aggregations of EventQL, EventSourcingDB's query language.
tags: [eventsourcingdb, eventql, query]
status: draft
sources:
  - https://docs.eventsourcingdb.io/reference/eventql/
  - https://docs.eventsourcingdb.io/getting-started/running-eventql-queries/
  - https://docs.eventsourcingdb.io/about-eventsourcingdb/changelog/
updated: 2026-10-28
---

# EventQL query language

Endpoint: `POST /api/v1/run-eventql-query` with `{"query": "..."}`; NDJSON
rows `{"type":"row","payload":...}` (verified on 1.2.0). Case-insensitive.

## Shape

```
FROM <alias> IN <source>
[FROM <alias> IN <source>] ...      // multiple FROM = cartesian product
[WHERE <condition>]
[ORDER BY <field> [ASC|DESC]]
[GROUP BY <field> [HAVING <condition>]]
[SKIP <n>] [TOP <n>]
PROJECT INTO [DISTINCT] <expression>   // mandatory
```

Comments: `//` and `/* */`.

## Sources and fields

- Sources: `events`, `subjects` (strings), `eventtypes` (strings), subqueries
  in parentheses.
- Event fields: `specversion`, `id`, `time`, `source`, `subject`, `type`,
  `datacontenttype`, `data` (dot access, missing → `null`),
  `predecessorhash`, `hash`, `traceparent`, `tracestate`, `signature`
  (`hash`/`signature` since 1.2.0).
- `id` is a string but compares numerically with numbers; from subqueries
  cast with `AS INT`.

## Operators and types

- `==, !=, <, >, <=, >=`, `AND, OR, XOR, NOT`, `array CONTAINS value`.
- No implicit boolean conversion (non-boolean in `WHERE` = error).
- Casts with `AS`: `STRING, INT, FLOAT64, BOOLEAN, DATE, TIME, DATETIME`
  (RFC 3339 nano). Integers exact up to 1,000 digits; decimals = float64.
- Literals: numbers, strings, booleans, null, objects `{k: v}`, arrays.

## Functions

- Math: `ABS CEIL FLOOR ROUND COS SIN TAN EXP POW SQRT RAND PI`.
- String: `LOWER UPPER TRIM LTRIM RTRIM LEN INSTR SUBSTRING REPLACE
  STARTSWITH ENDSWITH`.
- Date/time: `NOW YEAR MONTH DAY HOUR MINUTE SECOND WEEKDAY`; `IF(c,a,b)`.
- Aggregates: `COUNT() COUNT(x) SUM AVG MIN MAX MEDIAN STDDEV VARIANCE UNIQUE`.
  Projection may mix aggregates only with constants, not with row fields.
  `GROUP BY` is for aggregation only (no member enumeration).

## Example

```
FROM e IN events
WHERE e.type == "io.limventure.sample.sample-registered"
GROUP BY e.data.matrix
PROJECT INTO { matrix: UNIQUE(e.data.matrix), n: COUNT() }
```

## Relevance for the LIMS (own conclusions)

- Good for ad-hoc audit questions ("all events by user X on instrument Y in
  period Z") and for `isEventQlQueryTrue` preconditions; **not** a substitute
  for read models — queries scan the log.
- No joins beyond cartesian products/subqueries; reporting belongs in
  projections (e.g. PostgreSQL / DuckDB read models).
- Can select `hash` and `signature`, useful for audit export tooling.
