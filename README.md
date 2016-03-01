# nocql

Simple abstraction for CQL queries
##

```python
import nocql
n = nocql.NoRM(session)

n.select(keyspace="testkeyspace", table="testtable")
'SELECT * FROM "testkeyspace"."testtable"'
n.select(keyspace="testkeyspace", table="testtable", fields=["test", "test2"])
'SELECT "test", "test2" FROM "testkeyspace"."testtable"'
n.select(keyspace="testkeyspace", table="testtable", where={"test": "test2", "test2":"test3"})
'SELECT * FROM "testkeyspace"."testtable" WHERE "test" = %(test)s AND "test2" = %(test2)s'
n.insert(keyspace="testkeyspace", table="testtable", data={"who": "dat"})
'INSERT INTO "testkeyspace"."testtable" ("who") VALUES (%(who)s)'

```

