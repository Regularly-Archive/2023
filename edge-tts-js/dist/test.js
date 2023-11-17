const lockAddress = function(value) {
    let s1 = value.split('');
    for (let index = 2; index < s1.length; index += 3) {
        s1.splice(index, 0, ',')
    }
    
    let s2 = s1.join('').split(",").slice(0,3).reverse();
    return s2.join('') + '00'
}

let ret = lockAddress('6E49CABB')
let value = BigInt(`0x${ret}`).toString();
console.log(value)