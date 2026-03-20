/*
atalho comentario de varias linhas:
*\
alt + shift + a

desafio: criar uma função que receba preco e desconto em %,
e mostre o valor final com desconto.
criar outra função que receba preço e quantidade
e mostre o valor total da compra.
*/

function calculardesconto(){
    const valorfinal = preco - (preco * desconto / 100);
    return valorfinal
    console.log(`o desconto foi de: ${valorfinal}`);
}
calculardesconto(1000, 5);

function calculartotal(preco, quantidade){
    const valorfinal = preco * quantidade;    
    console.log(`o valor total e de: ${valortotal}`);


}

calculartotal(100, 12);