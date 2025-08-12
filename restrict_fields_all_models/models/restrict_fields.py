from odoo import models, api

def restrict_write_create(model_cls):
    """Patch write/create to prevent editing all fields from UI."""
    def write(self, vals):
        # Remove all field changes unless superuser
        if not self.env.su:
            vals.clear()
        return super(model_cls, self).write(vals)

    def create(self, vals_list):
        # Optional: Restrict creation too
        if not self.env.su:
            if isinstance(vals_list, dict):
                vals_list = [vals_list]
            for vals in vals_list:
                vals.clear()
        return super(model_cls, self).create(vals_list)

    model_cls.write = write
    model_cls.create = create
    return model_cls


def _patch_all_models(env):
    for model_name, model_cls in env.registry.items():
        if getattr(model_cls, '_abstract', False) or getattr(model_cls, '_transient', False):
            continue
        if not hasattr(model_cls, '_table') or not model_cls._table:
            continue
        restrict_write_create(model_cls)


class BaseModelHook(models.AbstractModel):
    _name = 'restrict.fields.hook'
    _description = 'Hook to Restrict Fields'
    _abstract = True

    @api.model
    def _register_hook(self):
        _patch_all_models(self.env)
