function telephoneCheck(str) {
  let reg = /^(1\s|1|)?((\(\d{3}\))|\d{3})(\-|\s)?(\d{3})(\-|\s)?(\d{4})$/;
  if(reg.test(str)){
    return true;
  }
  return false;
}

console.log(telephoneCheck("555-555-5555"));
