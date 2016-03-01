from copy import deepcopy



operator_map = {
    "eq": "=",
    "neq": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
}


def quote(field):
    # Skip functions and asterisk
    if field.endswith(")") or (field == "*"):
        return field
    # UDT Fields and keyspace/table
    elif "." in field:
        split_field = field.split(".")
        return ".".join(map(quote, split_field))
    # Regular fields
    else:
        return "\"{0}\"".format(field)


def prepare_where(where):
    where_text = []
    value_dict = {}
    for column, value in deepcopy(where).iteritems():
        # Check if an operator was specified in the key
        if "__" in column:
            column_name, text_operator = column.split("__")
        # If not, assume its equality
        else:
            column_name = column
            text_operator = "eq"

        if text_operator not in operator_map:
            raise Exception("Unknown where clause operator")

        operator = operator_map[text_operator]

        string = "{0} {1} %({2})s".format(quote(column_name), operator, column_name.replace(".", "_"))

        where_text.append(string)
        value_dict[column_name.replace(".", "_")] = value
    return where_text, value_dict


class NoRM(object):

    def __init__(self, session, keyspace=None):
        self.session = session
        self.keyspace = keyspace


    def use(self, keyspace):
        self.session.execute("""
            USE %(keyspace)s
        """, {
            "keyspace": keyspace
        })
        self.keyspace = keyspace


    def select(self, table, where=None, fields=None, keyspace=None):
        query = []
        # Construct fields
        if not fields:
            fields = ["*"]

        cql_fields = ", ".join(map(quote, fields))
        query.append("SELECT {0}".format(cql_fields))

        # Construct keyspace/table name
        if not keyspace:
            if not self.keyspace:
                raise Exception("No keyspace specified")
            keyspace = self.keyspace

        cql_table = quote(".".join([keyspace, table]))
        query.append("FROM {0}".format(cql_table))

        # Construct WHERE clause
        if where:
            query.append("WHERE")
            where_text, value_dict = prepare_where(where)
            query.append(" AND ".join(where_text))

        return " ".join(query)


    def insert(self, table, data, keyspace=None):
        query = []

        # Construct keyspace/table name
        if not keyspace:
            if not self.keyspace:
                raise Exception("No keyspace specified")
            keyspace = self.keyspace

        cql_table = quote(".".join([keyspace, table]))
        query.append("INSERT INTO {0}".format(cql_table))

        cql_fields = map(quote, data.keys())
        query.append("({0})".format(", ".join(cql_fields)))

        cql_values = ", ".join(map(lambda k: "%({0})s".format(k), data.keys()))
        query.append("VALUES ({0})".format(cql_values))

        return " ".join(query)
