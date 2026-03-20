function processopedido(valor, quantidade, operacao) {
    return operacao(valor, quantidade);
}

function calculartota(preco, quantidade){
    return preco * quantidade;

}

let resultado =  processopedido(30, 50, calculartota);

// imprimir com template string
console.log(`total pedido: R$ ${resultado}`);
