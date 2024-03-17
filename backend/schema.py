from marshmallow import Schema, fields, ValidationError

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    due_date = fields.Date(required=True)
    status = fields.Str(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)