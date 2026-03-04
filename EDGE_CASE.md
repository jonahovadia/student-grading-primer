# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation


## Edge case: stats when there are no students

The specification does not define the expected behaviour of `GET /stats` when there are no student records in the database (e.g. after all students are deleted, or in a fresh database with an empty `students` table).

When there are no marks to aggregate, `GET /stats` returns the following JSON payload:

```json
{
  "count": 0,
  "average": null,
  "min": null,
  "max": null
}
```