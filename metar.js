// Conteúdo do arquivo /api/metar.js

export default async function handler(request, response) {
  // Pega a localidade (ex: SBIZ) que o front-end enviou na URL
  const { localidade } = request.query;
  
  // Pega a chave secreta das Variáveis de Ambiente do servidor (NUNCA fica no código)
  const apiKey = process.env.REDEMET_API_KEY;

  if (!apiKey) {
    return response.status(500).json({ message: 'Chave da API não configurada no servidor.' });
  }
  
  if (!localidade) {
    return response.status(400).json({ message: 'Localidade não fornecida.' });
  }

  const redemetUrl = `https://api-redemet.decea.mil.br/mensagens/metar/${localidade}?api_key=${apiKey}`;

  try {
    const apiResponse = await fetch(redemetUrl);
    const data = await apiResponse.json();
    
    // Retorna os dados da REDEMET para o navegador do usuário
    // Adiciona um header para permitir caching por 60 segundos
    response.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate');
    response.status(200).json(data);

  } catch (error) {
    response.status(502).json({ message: 'Erro ao contatar o servidor da REDEMET.' });
  }
}