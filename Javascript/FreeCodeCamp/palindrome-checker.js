function palindrome(str) {
  let reg = /[\W_]+/g
  str = str.replace(reg, "");
  str = str.toLowerCase();
  if(str == str.split("").reverse().join("")){
    return true;
  }
  return false
}

console.log(palindrome("_eye"));
