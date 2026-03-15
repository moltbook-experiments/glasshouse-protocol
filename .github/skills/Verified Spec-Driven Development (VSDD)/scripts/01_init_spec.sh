#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <feature_name>"
    echo "Example: $0 user_auth"
    exit 1
fi

FEATURE_NAME="$1"
VSDD_DIR=".vsdd/specs"
SPEC_FILE="$VSDD_DIR/${FEATURE_NAME}.md"

mkdir -p "$VSDD_DIR"

if [ -f "$SPEC_FILE" ]; then
    echo "Error: Specification $SPEC_FILE already exists."
    exit 1
fi

cat << 'EOF' > "$SPEC_FILE"
# VSDD Specification: __FEATURE_NAME__

## Phase 1a: Behavioral Specification

### Behavioral Contract
- **Preconditions:**
  - 
- **Postconditions:**
  - 
- **Invariants:**
  - 

### Interface Definition
- **Input Types:**
- **Output Types:**
- **Error Types:**

### Edge Case Catalog
1. 
2. 
3. 

### Non-Functional Requirements
- **Performance:**
- **Memory/Resources:**
- **Security:**

---

## Phase 1b: Verification Architecture

### Provable Properties Catalog
- [ ] Properties that MUST be formally verified:
  - 
- [ ] Properties that ONLY require test coverage:
  - 

### Purity Boundary Map
- **Deterministic Pure Core:**
- **Effectful Shell:**

### Verification Tooling Selection
- Selected Stack (e.g., Kani, pytest, mutmut):

EOF

sed -i "s/__FEATURE_NAME__/$FEATURE_NAME/g" "$SPEC_FILE"

echo "✅ VSDD Spec for '$FEATURE_NAME' created at $SPEC_FILE"
echo "Next step: Review the spec with the Adversary (Phase 1c) before writing tests."
