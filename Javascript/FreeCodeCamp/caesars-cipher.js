function rot13(str) {
  let space = [];
  for(let l = 0; l<str.length; l++){
    if(str[l] == " "){
      space.push(str.indexOf(str[l], l));
    }
  }
  let strArr = str.split(" ");
  let newArr = [];
  for(let i = 0; i < strArr.length; i++){
    for(let j = 0; j < strArr[i].length; j++){
      if(strArr[i][j] == "?" || strArr[i][j] == "!" || strArr[i][j] == "."){
        newArr.push(strArr[i][j]);
        break;
      } else {
        let num = strArr[i][j].charCodeAt(0)+12;
        if(num >= 90){
          newArr.push(String.fromCharCode(65+(num-90)));
        } else {
          newArr.push(String.fromCharCode(num+1));
        }
      }
    }
  }
  for(let k = 0; k < space.length; k++){
    newArr.splice(space[k], 0, " ");
  }
  return newArr.join("");
}

rot13("SERR PBQR PNZC");
