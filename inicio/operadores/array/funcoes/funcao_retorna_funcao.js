function criarcalculadordesconto(){
    return function(preco){
        return preco - (preco * desconto);

    }
}

const desconto10 = criarcalculadordesconto(0.10);
const desconto50 = criarcalculadordesconto(0.50);

console.log(desconto10(200));
console.log(desconto50(1230));