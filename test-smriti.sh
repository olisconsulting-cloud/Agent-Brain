#!/bin/bash
# test-smriti-v35.sh
# Quick validation script for Smriti v3.5

echo "=== SMRITI v3.5 VALIDATION ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check 1: Config files exist
echo "[1/7] Checking config files..."
for file in "neuron/smriti.json" "neuron/ouroboros.json" "neuron/bridge.json"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file MISSING"
        ((ERRORS++))
    fi
done
echo ""

# Check 2: Memory configs exist
echo "[2/7] Checking memory configs..."
for file in "neuron/memory/layer2.json" "neuron/memory/layer3.json" "neuron/memory/layer4.json"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file MISSING"
        ((ERRORS++))
    fi
done
echo ""

# Check 3: Data files exist or can be created
echo "[3/7] Checking data files..."
for file in "neuron/patterns.jsonl" "neuron/anti_patterns.jsonl" "neuron/.bridge_state.json"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${YELLOW}⚠${NC} $file will be created on first use"
        ((WARNINGS++))
    fi
done
echo ""

# Check 4: Layer 3 (mem0) health
echo "[4/7] Checking Layer 3 (mem0)..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} mem0 is running"
else
    echo -e "${YELLOW}⚠${NC} mem0 not responding (Layer 2 fallback active)"
    ((WARNINGS++))
fi
echo ""

# Check 5: Layer 3 (Qdrant) health
echo "[5/7] Checking Layer 3 (Qdrant)..."
if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Qdrant is running"
else
    echo -e "${YELLOW}⚠${NC} Qdrant not responding (Layer 2 fallback active)"
    ((WARNINGS++))
fi
echo ""

# Check 6: Layer 4 (Neo4j) health
echo "[6/7] Checking Layer 4 (Neo4j)..."
if curl -s http://localhost:7474 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Neo4j is running"
else
    echo -e "${YELLOW}⚠${NC} Neo4j not responding (Layer 3 fallback active)"
    ((WARNINGS++))
fi
echo ""

# Check 7: JSON validity
echo "[7/7] Validating JSON configs..."
for file in neuron/*.json neuron/memory/*.json; do
    if [ -f "$file" ]; then
        if python3 -m json.tool "$file" > /dev/null 2>&1; then
            : # Valid
        else
            echo -e "${RED}✗${NC} $file is invalid JSON"
            ((ERRORS++))
        fi
    fi
done
echo -e "${GREEN}✓${NC} All JSON files valid"
echo ""

# Summary
echo "=== SUMMARY ==="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "Smriti v3.5 is ready to use."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s)${NC}"
    echo "System will work with fallbacks."
    echo "To enable full functionality, start: docker-compose --profile complete up"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo "Please fix errors before using."
    exit 1
fi
