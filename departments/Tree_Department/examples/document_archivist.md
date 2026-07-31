## document_archivist
**Task:** Develop a document lifecycle management system for AI-generated trade documents, contracts, and reports. Include metadata tagging, versioning, retention policies, and secure archival procedures.

## Document Lifecycle Management System for AI-Generated Trade Documents

### 1. System Overview & Architectural Context

This system manages the complete lifecycle of AI-generated trade documents (contracts, bills of lading, customs declarations, compliance reports) from creation through archival or destruction. It operates as a distributed document store with immutable versioning, policy-driven retention, and cryptographic integrity verification.

**Core Design Principles:**
- **Immutability**: Once committed, document versions cannot be altered
- **Provenance**: Full lineage from AI generation prompt → output → human review → finalization
- **Compliance**: Automated retention scheduling aligned with regional trade regulations (UCC, Incoterms 2020, GDPR, SOX)
- **Quarantine**: AI-generated drafts isolated until validated by authorized reviewers

---

### 2. Data Schema Design

#### 2.1 Document Entity (MongoDB Collection: `trade_documents`)

```json
{
  "_id": "UUIDv7",
  "doc_type": "ENUM[contract, bill_of_lading, customs_declaration, compliance_report, invoice]",
  "trade_correlation_id": "UUID",  // links to trade transaction
  "status": "ENUM[draft, ai_generated, in_review, approved, active, superseded, archived, destroyed]",
  "content_hash": "SHA-256",
  "content_uri": "s3://bucket/path/{doc_id}/{version}.pdf",
  "metadata": {
    "parties": ["legal_entity_ids"],
    "jurisdiction": "ISO_3166-1_alpha-2",
    "trade_terms": ["Incoterms2020"],
    "currency": "ISO_4217",
    "amount": "decimal128",
    "ai_generation": {
      "model_id": "string",
      "prompt_hash": "SHA-256",
      "temperature": "float",
      "generated_at": "ISODate"
    }
  },
  "versioning": {
    "current_version": 3,
    "versions": [
      {
        "version": 1,
        "created_at": "ISODate",
        "created_by": "user_id | system_ai_id",
        "change_type": "ENUM[initial, ai_revision, human_edit, legal_review]",
        "content_hash": "SHA-256",
        "storage_ref": "s3://bucket/.../v1.pdf",
        "signature": "digital_signature_ref"
      }
    ]
  },
  "retention": {
    "policy_id": "UUID",
    "retention_start": "ISODate",
    "retention_end": "ISODate",
    "legal_hold": "boolean",
    "hold_reason": "string?"
  },
  "access_control": {
    "owner_org": "UUID",
    "read_roles": ["role_ids"],
    "write_roles": ["role_ids"],
    "classifications": ["ENUM[public, internal, confidential, restricted]"]
  },
  "audit_trail": [
    {
      "action": "ENUM[create, update, approve, archive, destroy, access]",
      "actor": "user_id | system_id",
      "timestamp": "ISODate",
      "metadata": "object"
    }
  ],
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

#### 2.2 Retention Policy Store (PostgreSQL: `retention_policies`)

```sql
CREATE TABLE retention_policies (
    policy_id UUID PRIMARY KEY,
    doc_type VARCHAR(50),
    jurisdiction VARCHAR(10),
    retention_period_days INTEGER,
    action_after_expiry ENUM('archive', 'destroy', 'indefinite'),
    requires_legal_hold BOOLEAN DEFAULT FALSE,
    version VARCHAR(10),
    effective_from DATE,
    effective_to DATE,
    created_by VARCHAR(100),
    created_at TIMESTAMPTZ
);

CREATE INDEX idx_retention_doc_juris ON retention_policies(doc_type, jurisdiction);
```

---

### 3. Metadata Tagging Strategy

#### 3.1 Hierarchical Tag Taxonomy

- **Level 1 – Functional**: `contract`, `invoice`, `shipping_manifest`
- **Level 2 – Legal**: `governing_law`, `dispute_clause`, `termination_terms`
- **Level 3 – Operational**: `trade_route`, `incoterm`, `payment_terms`
- **Level 4 – Compliance**: `export_control`, `sanctions_check`, `customs_value`

#### 3.