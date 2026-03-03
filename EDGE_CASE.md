# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation


## Edge case: stats when there are no students

**Scenario**

The specification does not define the expected behaviour of `GET /stats` when there are no student records in the database (e.g. after all students are deleted, or in a fresh database with an empty `students` table).

**Decision**

When there are no marks to aggregate, `GET /stats` returns the following JSON payload:

```json
{
  "count": 0,
  "average": null,
  "min": null,
  "max": null
}
```

**Rationale**

- **`count` = 0** clearly communicates that there are currently no marks contributing to the statistics.
- **`average`, `min`, and `max` = `null`** (JSON `null`, represented as `None` in Python) reflect that these values are mathematically undefined when there are zero items. Returning `0` for these fields could be misleading, as `0` is a valid mark and might be interpreted as an actual computed value rather than “no data”.
- This shape keeps the response schema stable (the same keys are always present) while making it explicit that no meaningful statistical values can be derived in this scenario.
