# Restrict All Field Edits in Odoo

## Overview
This module modifies all models in Odoo so that normal users cannot **update** or **create** records from the UI.  
Only the **superuser** (`admin`) can perform these actions.  
It works by overriding the `write` and `create` methods of every model.

---

## How It Works

### 1. Patching All Models
The function `_patch_all_models(env)` loops through all registered models and:
- Skips **abstract** and **transient** models.
- Applies the `restrict_write_create` function to the rest.

---

### 2. Restricting `write()`
```python
if not self.env.su:
    vals.clear()
