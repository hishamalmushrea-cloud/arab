# UAE pilot additive Schema v1.0.0 change

## Problem

The former UAE vocabulary supplied only `ae_municipal_region`, `ae_sector`, and `ae_district`. Those generic labels cannot preserve the different official meanings used by Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah, and Fujairah. The claim vocabulary also could not express an emirate-scoped cultural claim without incorrectly using either national or local scope. Finally, entity status had no explicit values for a renamed, merged, or abolished former unit.

## Reason for change

The UAE pilot is a transferability test of contextual local semantics, not a volume test. Reusing a single generic lower hierarchy would erase distinctions among municipality jurisdictions, planning sectors and communities, mixed-wording constituents, municipality authorities, and numbered administrative areas. Notes alone are not an executable semantic contract.

## Additive change

Schema v1.0.0 adds these controlled `entity_type` values:

- `ae_abu_dhabi_municipality_jurisdiction`
- `ae_dubai_planning_sector`
- `ae_dubai_planning_community`
- `ae_sharjah_municipality_jurisdiction`
- `ae_ajman_constituent`
- `ae_uaq_municipal_authority`
- `ae_rak_administrative_area`
- `ae_fujairah_municipal_authority`

It also adds claim classification `emirate_specific`, entity statuses `renamed`, `merged`, and `abolished`, and the optional manifest property `emirate_profiles`. The latter is a structured list of emirate-specific authorities, contextual lower layers, semantics, denominators, source IDs, entity IDs, and special cases. `emirate_specific` means that evidence is scoped to one emirate; it does not imply exclusivity.

## Backward compatibility and version decision

This is an additive vocabulary and optional manifest extension. It does not remove a property, change a required field, reinterpret an existing value, or invalidate an existing record. The legacy UAE values `ae_municipal_region`, `ae_sector`, and `ae_district` remain in the shared vocabulary for old Schema v1.0.0 data. They are deprecated for new UAE pilot local entities, and the UAE semantic validator rejects their use in this pilot.

Because all changes only enlarge previously enumerated accepted values, the schema remains at `1.0.0`. No repository policy requires a version change for additive enum values, and a breaking change has not occurred.

## Temporal semantics

A historical name for the same parent-scoped identity is an Alias with historical/ former status. A former unit whose distinct identity ended through an official rename, merger, or abolition is an Entity with the corresponding new status and temporal evidence. Such entities cannot appear as current administrative children. The pilot does not invent examples where its bounded sources do not establish one.

## Tests

The UAE test suite verifies:

1. every new contextual type is in the executable vocabulary;
2. generic UAE lower types are rejected by the UAE validator;
3. `emirate_specific` is accepted by both JSON Schema and the executable vocabulary;
4. `renamed`, `merged`, and `abolished` are accepted by Entity JSON Schema and the executable vocabulary;
5. the eight required UAE semantic mutations are all detected;
6. the repository-wide validator still accepts all previous-country records under Schema v1.0.0.

## Superseded version disposition

This document records why the UAE-only vocabulary delta was additive at the time. The later cumulative migration review found earlier required-field and Coverage semantic changes to be breaking and released the complete contract as Schema 2.0.0. No UAE vocabulary value was removed.
