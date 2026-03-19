const cores = ["vermelho", "azul", "verde", "amarelo"];
const numeros = ["0","1","2","3","4","5","6","7","8","9"];

function criarBaralho() {
  let baralho = [];
  
  for (let cor of cores) {
    for (let numero of numeros) {
      baralho.push({ cor, numero });
    }
  }

  return baralho;
}

function embaralhar(baralho) {
  return baralho.sort(() => Math.random() - 0.5);
}

function comprarCarta(baralho) {
  return baralho.pop();
}

// iniciar jogo
let baralho = embaralhar(criarBaralho());

let jogador = [comprarCarta(baralho), comprarCarta(baralho)];
let computador = [comprarCarta(baralho), comprarCarta(baralho)];

let mesa = [comprarCarta(baralho)];

console.log("Carta na mesa:", mesa[0]);

console.log("Suas cartas:");
jogador.forEach((carta, i) => {
  console.log(`${i}: ${carta.cor} ${carta.numero}`);
});