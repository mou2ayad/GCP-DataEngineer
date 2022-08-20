function validate_json(inJson) {
    try {  
      const json = JSON.parse(inJson); 
      return json 
    } catch (e) {  
    // console.log('invalid json',inJson); 
  }
  return ''
}