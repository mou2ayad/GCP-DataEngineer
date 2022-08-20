function transform(inJson) {
    var input = JSON.parse(inJson);
    var output = {};
    output.uuid=input.uuid
    output.created_at=input.created_at
    output.data=input.data
    output.meta=input.data
    output.type=input.type
    return JSON.stringify(output);
   }