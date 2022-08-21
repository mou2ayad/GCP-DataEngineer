function transform(input) {
  try {  
     jsonObject = JSON.parse(input); 
     output={}
     output.uuid=jsonObject.uuid
     output.created_at=jsonObject.created_at
     output.data=JSON.stringify(jsonObject.data)
     output.meta=JSON.stringify(jsonObject.meta)
     output.type=jsonObject.type
    return JSON.stringify(output);
  } catch (e) {  }
}