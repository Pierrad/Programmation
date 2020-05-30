/*
Service Parser, il permet de prendre un String et pour chaque '\n' présent, il saute à la ligne et enfin return un Array
*/
export default function StringToArray(string) {
    let arr = string.split(/\\n/);
    const resultArr = [];
    arr.forEach((item, i) => {
        if(i%2===0){
            resultArr.push('\n');
        }
        resultArr.push(item);
    });
    return resultArr;
}
