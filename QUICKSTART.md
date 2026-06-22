# Cangjie Skill - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/kangarooking/cangjie-skill.git
cd cangjie-skill

# Run installation script
python scripts/install.py

# Or install manually
pip install -e .
```

### 2. First-Time Setup

```bash
# Create configuration from template
cp .env.example .env

# Create necessary directories
mkdir -p data/books_raw data/books_txt data/books_txt_ocr data/library data/output logs

# Check system status
cangjie status
```

### 3. Your First Book Distillation

```bash
# Place your PDF book in the books_raw directory
cp your-book.pdf data/books_raw/

# Distill the book into skills
cangjie distill data/books_raw/your-book.pdf

# Or use the full path
cangjie distill /path/to/your/book.pdf
```

## 📚 What Happens During Distillation

The distillation process follows the **RIA-TV++** methodology:

1. **Stage 0**: Whole book understanding (Adler analysis)
2. **Stage 1**: Parallel extraction (5 specialized agents)
3. **Stage 1.5**: Triple verification screening
4. **Stage 2**: RIA++ construction (6-segment skills)
5. **Stage 3**: Zettelkasten linking (skill relationships)
6. **Stage 4**: Pressure testing (quality assurance)

## 🎯 Key Commands

### Basic Operations
```bash
# Show help
cangjie --help

# Check system status
cangjie status

# Validate system consistency
cangjie validate

# Update global indices
cangjie index-update
```

### Book Processing
```bash
# Extract text from PDFs (non-scanned)
python scripts/extract_pdfs.py

# OCR scanned PDFs
python scripts/ocr_processor.py

# Or use the CLI
cangjie ocr path/to/scanned.pdf
```

### Skill Management
```bash
# List all distilled skills
find library -name "SKILL.md" | wc -l

# View a specific skill
cat library/chaogu-zhihui/shunshi-jiaoyi/SKILL.md

# Test a skill
cangjie test --skill-id "chaogu-zhihui::shunshi-jiaoyi"
```

## 🧪 Testing & Validation

```bash
# Run all validation checks
cangjie validate

# Run specific checks
cangjie validate --check ria --check test

# Attempt to fix issues
cangjie validate --fix

# Run strict validation (warnings as errors)
cangjie validate --strict

# Run basic tests
pytest tests/test_basic.py
```

## 🔧 Configuration

Edit `.env` file to customize:

```bash
# Enable GPU for OCR (if available)
OCR_USE_GPU=true

# Adjust parallel processing
MAX_WORKERS=8

# Change logging level
LOG_LEVEL=DEBUG

# Enable fast mode (skip some checks)
FAST_MODE=true
```

## 🚨 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **OCR Fails**
   ```bash
   # Check PaddleOCR installation
   python -c "from paddleocr import PaddleOCR; print('OK')"
   
   # Try CPU mode
   export OCR_USE_GPU=false
   ```

3. **Memory Issues**
   ```bash
   # Reduce parallel workers
   export MAX_WORKERS=2
   
   # Increase memory limit
   export MAX_MEMORY_USAGE="4GB"
   ```

4. **Validation Errors**
   ```bash
   # Show detailed error messages
   cangjie validate --check ria
   
   # Check specific skill
   cangjie validate --check source --check test
   ```

### Getting Help

```bash
# View detailed logs
tail -f logs/cangjie.log

# Check system resources
cangjie status

# Run diagnostics
python scripts/install.py --skip-tests
```

## 📖 Example Workflow

### Complete Example: Distill "The Intelligent Investor"

```bash
# 1. Prepare the book
cp intelligent-investor.pdf data/books_raw/

# 2. Extract text (if not scanned)
python scripts/extract_pdfs.py

# 3. Distill into skills
cangjie distill data/books_raw/intelligent-investor.pdf

# 4. Check results
ls -la output/intelligent-investor/

# 5. Validate quality
cangjie validate

# 6. Update global index
cangjie index-update

# 7. Use the skills
cangjie orchestrate "Should I invest in this company?"
```

### Multi-Book Orchestration Example

```bash
# After distilling multiple books...

# Ask a complex question
cangjie orchestrate "How should I manage investment risk?"

# Get detailed reasoning
cangjie orchestrate "When should I sell a stock?" --detailed

# Export results
cangjie orchestrate "Investment strategy for retirement" --output-format both
```

## 🎓 Learning Resources

- **Methodology**: Read `methodology/00-overview.md` for RIA-TV++ details
- **Skill Format**: See `templates/SKILL.md.template` for skill structure
- **Validation**: Check `cangjie/validation/` for quality rules
- **Examples**: Review `library/` for distilled skill examples

## ⚡ Performance Tips

1. **For large books**: Use `--fast` mode for initial distillation
2. **For scanned books**: Enable GPU OCR with `OCR_USE_GPU=true`
3. **For batch processing**: Use `MAX_WORKERS` to control parallelism
4. **For development**: Set `DEBUG=true` for detailed logging

## 🔄 Updating

```bash
# Update from git
git pull origin main

# Reinstall dependencies
pip install -e . --upgrade

# Update indices
cangjie index-update --force
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `cangjie validate --strict`
5. Submit a pull request

## 📞 Support

- **Issues**: https://github.com/kangarooking/cangjie-skill/issues
- **Documentation**: See `README.md` and `SKILL.md`
- **Examples**: Check `library/` directory

---

**Next Steps:**
1. ✅ Install Cangjie Skill
2. ✅ Configure your environment  
3. 🎯 Distill your first book
4. 🔍 Explore the created skills
5. 🚀 Use multi-book orchestration

Happy distilling! 📚→🤖
```

## Quick Reference Card

```bash
# Essential Commands
cangjie --help                    # Show all commands
cangjie status                    # System status
cangjie distill <book.pdf>        # Distill a book
cangjie validate                  # Validate system
cangjie orchestrate <intent>      # Multi-book query

# Development
make install                      # Install dependencies
make test                         # Run tests
make format                       # Format code
make lint                         # Check code quality

# Processing
python scripts/extract_pdfs.py    # Extract PDF text
python scripts/ocr_processor.py   # OCR scanned PDFs
cangjie ocr <pdf>                 # OCR via CLI
```

**Tip**: Bookmark this guide or save it as `QUICKSTART.md` in your project!
