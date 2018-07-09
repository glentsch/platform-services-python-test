
class Validator:
    @staticmethod
    def validate(schema, obj):
        #TODO: It is possible obj has more fields than in the schema
        #TODO: No support for some additional data types that would be handy (e-mail validation)
        for k,v in schema.items():
            try:
                obj_field = obj[k]
            except KeyError:
                return False
            if type(obj_field).__name__ != v:
                return False
        return True