# What Does XML Have to Do with Apache Avro?

## Q: What does XML have to do with Apache Avro?

Avro schemas can be defined in XML, in addition to the more common JSON format. That is the extent of the relationship.

### Key Points

- **Schema definition only:** XML is an optional syntax for writing Avro schemas (field names, types, namespaces). It has no role in how Avro actually stores or transmits data.
- **Binary serialization:** Avro's data encoding is compact binary — not XML, not JSON. This is one of Avro's main advantages over XML-based formats.
- **JSON dominates in practice:** XML schema definitions are rarely used. The JSON schema format is the standard across the Avro ecosystem.

### Comparison

| Aspect | XML | Avro |
|---|---|---|
| Schema format | XML itself | JSON (XML optionally supported) |
| Data encoding | Verbose text | Compact binary |
| Schema required? | Optional (DTD/XSD) | Always required |
| Typical use case | Config, web/enterprise services | Big data pipelines (Hadoop, Kafka) |

### Summary

XML can be used to *write* an Avro schema, but it has nothing to do with how Avro stores or moves data. In practice, you will almost never encounter XML in an Avro workflow.
