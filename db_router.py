class DumpDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'scheme':  # example app using dump DB
            return 'dump_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'scheme':
            return 'dump_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'scheme':
            return db == 'dump_db'
        return db == 'default'
