import re

def sql_to_jpa_entity(sql):
    # Extract table name
    match = re.search(r"CREATE TABLE (\w+)", sql)
    if not match:
        return "Invalid SQL"
    table_name = match.group(1)
    class_name = table_name.capitalize()

    # Extract column details
    columns = re.findall(r"(\w+) (\w+)(\(.*?\))?( UNIQUE)?( NOT NULL)?", sql)

    attributes = []
    for column in columns:
        column_name = column[0]
        column_type = column[1]
        unique = column[3]
        not_null = column[4]

        # Convert SQL types to Java types
        if column_type == "SERIAL":
            java_type = "Long"
        elif column_type == "VARCHAR":
            java_type = "String"
        elif column_type == "TIMESTAMP":
            java_type = "LocalDateTime"
        else:
            java_type = column_type  # Placeholder for other types

        attribute = f"@Column(name = \"{column_name}\""
        if unique:
            attribute += ", unique = true"
        if not_null:
            attribute += ", nullable = false"
        attribute += ")\n    private " + java_type + " " + column_name + ";"

        # Check for primary key
        if "PRIMARY KEY" in sql and column_name in sql.split("PRIMARY KEY")[1]:
            attribute = "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    " + attribute

        attributes.append(attribute)

    # Construct the entity
    entity = f"@Entity\n@Table(name = \"{table_name}\")\npublic class {class_name} {{\n\n"
    entity += "\n\n".join(attributes)
    entity += "\n\n    // Getters, setters, and other methods...\n}"
    return entity

sql_schema = """
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

print(sql_to_jpa_entity(sql_schema))

