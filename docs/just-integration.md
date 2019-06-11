# Installing just the UMC extensions

(Feature contributed by linudata.de)

When just requiring the UMC extension and the LDAP schema (used for managing users are Kopano server objects) the following packages can be installed:

| Package                    | Purpose                                     |
|----------------------------|---------------------------------------------|
| kopano4ucs-schema          | Kopano ldap schema                          |
| kopano4ucs-udm             | UMC integration for managing users          |
|                            | (depends on kopano4ucs-schema)              |
| kopano4ucs-udm-multiserver | Kopano multiserver specific UMC integration |
|                            | (depends on kopano4ucs-udm)                 |
| kopano4ucs-udm-archiver    | Kopano archiver specific UMC integration    |
|                            | (depends on kopano4ucs-multiserver)         |

When managing Kopano installations on non-UCS systems the "computer" object needs to be assigned the "Kopano" service (selectable below "Advanced settings").